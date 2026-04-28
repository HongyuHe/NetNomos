from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from tqdm.auto import tqdm

from netnomos.ast import BoolAnd, BoolNot, Compare, Formula, Implies, formula_to_string
from netnomos.dataset import PreparedDataset
from netnomos.learners.hittingset import LearnedRule
from netnomos.projection import GroundedPredicate
from netnomos.theory import evaluate_formula_df


class EntropyTreeLearner:
    def __init__(
        self,
        max_depth: int = 4,
        min_samples_leaf: int = 2,
        min_positive_purity: float = 0.95,
        max_rules: int = 250,
    ):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_positive_purity = min_positive_purity
        self.max_rules = max_rules
        self.last_fit_metadata: dict[str, float | int] = {}

    def fit(self, predicates: list[GroundedPredicate], prepared: PreparedDataset) -> list[LearnedRule]:
        try:
            from sklearn.tree import DecisionTreeClassifier
        except ModuleNotFoundError as exc:
            raise RuntimeError("EntropyTreeLearner requires scikit-learn to be installed") from exc

        matrix = np.column_stack([
            evaluate_formula_df(predicate.formula, prepared).astype(int).to_numpy()
            for predicate in tqdm(predicates, desc="Evaluating tree features", unit=" predicate", disable=None)
        ])
        rules: list[LearnedRule] = []
        for target_index, target in enumerate(tqdm(predicates, desc="Learning tree rules", unit=" target", disable=None)):
            if len(rules) >= self.max_rules:
                break
            y = matrix[:, target_index]
            if y.min() == y.max():
                continue
            feature_indices = [index for index in range(len(predicates)) if index != target_index]
            X = matrix[:, feature_indices]
            clf = DecisionTreeClassifier(
                criterion="entropy",
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                random_state=42,
            )
            clf.fit(X, y)
            tree = clf.tree_

            def walk(node_id: int, conditions: list[tuple[int, bool]]) -> None:
                if len(rules) >= self.max_rules:
                    return
                left = tree.children_left[node_id]
                right = tree.children_right[node_id]
                if left == right:
                    probs = tree.value[node_id][0]
                    if clf.classes_[int(np.argmax(probs))] != 1:
                        return
                    total = float(np.sum(probs))
                    purity = float(np.max(probs) / total) if total else 0.0
                    if purity < self.min_positive_purity:
                        return
                    premise_formula = build_path_formula(conditions, predicates, feature_indices)
                    if premise_formula is None:
                        return
                    formula = Implies(premise_formula, target.formula)
                    support = float(evaluate_formula_df(formula, prepared).mean())
                    rules.append(LearnedRule(
                        rule_id=f"tree{len(rules):05d}",
                        formula=formula,
                        display=formula_to_string(formula),
                        support=support,
                        source={
                            "learner": "tree",
                            "target_predicate_id": target.predicate_id,
                            "target_display": target.display,
                            "purity": purity,
                        },
                    ))
                    return
                feature_index = int(tree.feature[node_id])
                walk(left, [*conditions, (feature_index, False)])
                walk(right, [*conditions, (feature_index, True)])

            walk(0, [])
        self.last_fit_metadata = {
            "rule_count": len(rules),
            "predicate_count": len(predicates),
        }
        return rules


def build_path_formula(
    conditions: list[tuple[int, bool]],
    predicates: list[GroundedPredicate],
    feature_indices: list[int],
) -> Formula | None:
    literals: list[Formula] = []
    for local_index, positive in conditions:
        predicate = predicates[feature_indices[local_index]].formula
        literals.append(predicate if positive else BoolNot(predicate))
    if not literals:
        return None
    if len(literals) == 1:
        return literals[0]
    return BoolAnd(tuple(literals))
