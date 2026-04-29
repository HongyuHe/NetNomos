#include <algorithm>
#include <chrono>
#include <cstdint>
#include <functional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace {

std::size_t popcount64(std::uint64_t value) {
#if defined(__GNUC__) || defined(__clang__)
    return static_cast<std::size_t>(__builtin_popcountll(value));
#else
    std::size_t count = 0;
    while (value != 0U) {
        value &= (value - 1U);
        ++count;
    }
    return count;
#endif
}

class DynamicBitset {
  public:
    explicit DynamicBitset(std::size_t size)
        : size_(size), words_((size + 63U) / 64U, 0U) {}

    void set(std::size_t index) {
        words_[index / 64U] |= (std::uint64_t{1} << (index % 64U));
    }

    bool test(std::size_t index) const {
        return (words_[index / 64U] & (std::uint64_t{1} << (index % 64U))) != 0U;
    }

    std::size_t union_inplace_count_new(const DynamicBitset& other) {
        std::size_t added = 0;
        for (std::size_t idx = 0; idx < words_.size(); ++idx) {
            const auto before = words_[idx];
            const auto after = before | other.words_[idx];
            added += popcount64(after ^ before);
            words_[idx] = after;
        }
        return added;
    }

    std::size_t count_uncovered_hits(const DynamicBitset& covered) const {
        std::size_t total = 0;
        for (std::size_t idx = 0; idx < words_.size(); ++idx) {
            total += popcount64(words_[idx] & ~covered.words_[idx]);
        }
        return total;
    }

  private:
    std::size_t size_;
    std::vector<std::uint64_t> words_;
};

bool is_subset(const std::vector<int>& lhs, const std::vector<int>& rhs) {
    std::size_t left_index = 0;
    std::size_t right_index = 0;
    while (left_index < lhs.size() && right_index < rhs.size()) {
        if (lhs[left_index] == rhs[right_index]) {
            ++left_index;
            ++right_index;
            continue;
        }
        if (lhs[left_index] > rhs[right_index]) {
            ++right_index;
            continue;
        }
        return false;
    }
    return left_index == lhs.size();
}

std::vector<int> insert_sorted(const std::vector<int>& items, int value) {
    std::vector<int> result;
    result.reserve(items.size() + 1U);
    auto insert_it = std::lower_bound(items.begin(), items.end(), value);
    result.insert(result.end(), items.begin(), insert_it);
    if (insert_it == items.end() || *insert_it != value) {
        result.push_back(value);
    }
    result.insert(result.end(), insert_it, items.end());
    return result;
}

py::dict enumerate_hitting_sets(
    const std::vector<std::vector<int>>& raw_evidence_sets,
    int max_clause_size,
    int max_rules,
    double stall_timeout_seconds,
    py::object progress_callback
) {
    if (max_clause_size < 0) {
        throw std::invalid_argument("max_clause_size must be non-negative");
    }
    if (max_rules < 0) {
        throw std::invalid_argument("max_rules must be non-negative");
    }

    std::vector<std::vector<int>> evidence_sets;
    evidence_sets.reserve(raw_evidence_sets.size());
    int max_predicate_index = -1;
    for (auto evidence : raw_evidence_sets) {
        std::sort(evidence.begin(), evidence.end());
        evidence.erase(std::unique(evidence.begin(), evidence.end()), evidence.end());
        if (!evidence.empty()) {
            max_predicate_index = std::max(max_predicate_index, evidence.back());
        }
        evidence_sets.push_back(std::move(evidence));
    }

    const auto evidence_count = evidence_sets.size();
    std::vector<DynamicBitset> predicate_coverages;
    if (max_predicate_index >= 0) {
        predicate_coverages.reserve(static_cast<std::size_t>(max_predicate_index) + 1U);
        for (int index = 0; index <= max_predicate_index; ++index) {
            predicate_coverages.emplace_back(evidence_count);
        }
        for (std::size_t evidence_index = 0; evidence_index < evidence_sets.size(); ++evidence_index) {
            for (int predicate_index : evidence_sets[evidence_index]) {
                predicate_coverages[static_cast<std::size_t>(predicate_index)].set(evidence_index);
            }
        }
    }

    std::vector<std::vector<int>> solutions;
    solutions.reserve(static_cast<std::size_t>(std::max(max_rules, 0)));
    const auto start_time = std::chrono::steady_clock::now();
    auto last_solution_time = start_time;
    bool stopped_early = false;
    bool hit_max_rules = false;

    const auto is_stalled = [&]() -> bool {
        if (stall_timeout_seconds < 0.0) {
            return false;
        }
        const auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - last_solution_time).count();
        return elapsed >= stall_timeout_seconds;
    };

    const auto has_subset = [&](const std::vector<int>& candidate) -> bool {
        for (const auto& solution : solutions) {
            if (is_subset(solution, candidate)) {
                return true;
            }
        }
        return false;
    };

    std::function<void(const std::vector<int>&, const DynamicBitset&, std::size_t)> branch;
    branch = [&](const std::vector<int>& chosen, const DynamicBitset& covered, std::size_t covered_count) {
        if (hit_max_rules || stopped_early) {
            return;
        }
        if (is_stalled()) {
            stopped_early = true;
            return;
        }
        if (solutions.size() >= static_cast<std::size_t>(max_rules)) {
            hit_max_rules = true;
            return;
        }
        if (covered_count == evidence_count) {
            if (!has_subset(chosen)) {
                std::vector<std::vector<int>> kept;
                kept.reserve(solutions.size());
                for (const auto& solution : solutions) {
                    if (!is_subset(chosen, solution) || chosen == solution) {
                        kept.push_back(solution);
                    }
                }
                solutions.swap(kept);
                solutions.push_back(chosen);
                last_solution_time = std::chrono::steady_clock::now();
                if (!progress_callback.is_none()) {
                    progress_callback(static_cast<int>(solutions.size()));
                }
            }
            return;
        }
        if (chosen.size() >= static_cast<std::size_t>(max_clause_size)) {
            return;
        }

        std::size_t pivot = evidence_count;
        std::size_t pivot_size = 0;
        bool have_pivot = false;
        for (std::size_t evidence_index = 0; evidence_index < evidence_count; ++evidence_index) {
            if (covered.test(evidence_index)) {
                continue;
            }
            const auto size = evidence_sets[evidence_index].size();
            if (!have_pivot || size < pivot_size) {
                pivot = evidence_index;
                pivot_size = size;
                have_pivot = true;
            }
        }
        if (!have_pivot) {
            return;
        }

        auto candidates = evidence_sets[pivot];
        std::sort(
            candidates.begin(),
            candidates.end(),
            [&](int lhs, int rhs) {
                const auto lhs_gain = predicate_coverages[static_cast<std::size_t>(lhs)].count_uncovered_hits(covered);
                const auto rhs_gain = predicate_coverages[static_cast<std::size_t>(rhs)].count_uncovered_hits(covered);
                if (lhs_gain != rhs_gain) {
                    return lhs_gain > rhs_gain;
                }
                return lhs < rhs;
            }
        );

        for (int predicate_index : candidates) {
            if (hit_max_rules || stopped_early) {
                return;
            }
            if (is_stalled()) {
                stopped_early = true;
                return;
            }
            if (std::binary_search(chosen.begin(), chosen.end(), predicate_index)) {
                continue;
            }
            const auto next_chosen = insert_sorted(chosen, predicate_index);
            if (has_subset(next_chosen)) {
                continue;
            }
            auto next_covered = covered;
            const auto added = next_covered.union_inplace_count_new(
                predicate_coverages[static_cast<std::size_t>(predicate_index)]
            );
            branch(next_chosen, next_covered, covered_count + added);
        }
    };

    branch({}, DynamicBitset(evidence_count), 0U);

    const auto end_time = std::chrono::steady_clock::now();
    py::list covers;
    for (const auto& solution : solutions) {
        covers.append(solution);
    }

    py::dict result;
    result["covers"] = std::move(covers);
    result["search_stopped_early"] = stopped_early;
    result["stop_reason"] = stopped_early ? "stall-timeout" : (hit_max_rules ? "max-rules" : "complete");
    if (stall_timeout_seconds < 0.0) {
        result["stall_timeout_seconds"] = py::none();
    } else {
        result["stall_timeout_seconds"] = stall_timeout_seconds;
    }
    result["stall_elapsed_seconds"] = std::chrono::duration<double>(end_time - last_solution_time).count();
    result["search_elapsed_seconds"] = std::chrono::duration<double>(end_time - start_time).count();
    return result;
}

}  // namespace

PYBIND11_MODULE(_hittingset_native, module) {
    module.doc() = "Native hitting-set enumeration for NetNomos.";
    module.def(
        "enumerate_hitting_sets",
        &enumerate_hitting_sets,
        py::arg("evidence_sets"),
        py::arg("max_clause_size"),
        py::arg("max_rules"),
        py::arg("stall_timeout_seconds") = -1.0,
        py::arg("progress_callback") = py::none()
    );
}
