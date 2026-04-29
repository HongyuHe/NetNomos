from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from rich import print as rich_print
from rich.json import JSON

from netnomos.api import NetNomosMiner
from netnomos.dsl import parse_formula
from netnomos.logging_utils import configure_logging
from netnomos.specs import GrammarSpec, HittingSetBackend, LearnerKind, load_dataset_spec, load_grammar_spec


class CliFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


CLI_DESCRIPTION = (
    "Inspect specs, prepare datasets, mine rules, validate rule sets, interpret saved artifacts, "
    "and run entailment queries."
)

CLI_EPILOG = """Examples:
  netn mine --dataset-spec examples/datasets/cidds.json --grammar-spec examples/grammars/network_flow.json --input data/cidds_wk2_normal_10k.csv
  netn mine --dataset-spec examples/datasets/pcap_tcp.json --grammar-spec examples/grammars/pcap_window.json --input data/netflix.pcap
  netn entails --dataset-spec examples/datasets/cidds.json --grammar-spec examples/grammars/network_flow.json --rules runs/<run>/rules.json --query "Packets * 65535 >= Bytes"
"""


def add_dataset_spec_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--dataset-spec",
        required=True,
        help="Path to a dataset schema JSON file.",
    )


def add_grammar_spec_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--grammar-spec",
        required=True,
        help="Path to a grammar JSON file.",
    )


def add_input_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--input",
        help="Override the dataset spec source path for this command.",
    )


def add_limit_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of raw input rows or packets to load before preprocessing.",
    )


def add_learner_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--learner",
        choices=[item.value for item in LearnerKind],
        default=LearnerKind.HITTING_SET.value,
        help="Rule-learning backend to use when mining rules.",
    )


def add_stall_timeout_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--stall-timeout",
        type=float,
        help=(
            "Stop the hitting-set search after this many seconds without discovering a new rule. "
            "Ignored by the tree learner."
        ),
    )


def add_hittingset_backend_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--hittingset-backend",
        choices=[item.value for item in HittingSetBackend],
        default=HittingSetBackend.AUTO.value,
        help=(
            "Implementation for the hitting-set learner: native uses the pybind11 C++ core, python "
            "keeps the pure Python search, and auto prefers native when available."
        ),
    )


def add_runs_dir_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Directory where mining runs and artifacts are written.",
    )


def add_rules_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--rules",
        help=(
            "Path to an existing rules.json artifact. When provided, the command skips mining and "
            "operates on those saved rules."
        ),
    )


def add_query_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--query",
        required=True,
        help="Formula string to check for entailment.",
    )


def add_output_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output",
        help="Write the command output to this file instead of stdout when supported.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="netn",
        description=CLI_DESCRIPTION,
        epilog=CLI_EPILOG,
        formatter_class=CliFormatter,
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging verbosity for diagnostic messages written to stderr.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="COMMAND", help="Subcommand to run")

    show_dataset = subparsers.add_parser(
        "show-dataset",
        help="Print a dataset schema JSON file.",
        description="Load and print a dataset schema exactly as NetNomos sees it.",
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(show_dataset)

    show_grammar = subparsers.add_parser(
        "show-grammar",
        help="Print a grammar JSON file.",
        description="Load and print a grammar exactly as NetNomos sees it.",
        formatter_class=CliFormatter,
    )
    add_grammar_spec_arg(show_grammar)

    prepare = subparsers.add_parser(
        "prepare",
        help="Load and materialize a dataset.",
        description=(
            "Load a dataset, apply preprocessing, build context windows and derived variables, "
            "and print the resulting schema summary."
        ),
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(prepare)
    add_input_arg(prepare)
    add_limit_arg(prepare)

    mine = subparsers.add_parser(
        "mine",
        help="Generate predicates and learn rules.",
        description="Mine predicates and rules from a dataset using a grammar and a selected learner.",
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(mine)
    add_grammar_spec_arg(mine)
    add_input_arg(mine)
    add_limit_arg(mine)
    add_learner_arg(mine)
    add_stall_timeout_arg(mine)
    add_hittingset_backend_arg(mine)
    add_runs_dir_arg(mine)

    validate = subparsers.add_parser(
        "validate",
        help="Validate a mined or saved rule set against data.",
        description=(
            "Validate saved rules.json artifacts, or mine a fresh rule set first and then validate it "
            "against the prepared dataset."
        ),
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(validate)
    add_grammar_spec_arg(validate)
    add_input_arg(validate)
    add_limit_arg(validate)
    add_rules_arg(validate)
    add_learner_arg(validate)
    add_stall_timeout_arg(validate)
    add_hittingset_backend_arg(validate)
    add_runs_dir_arg(validate)

    interpret = subparsers.add_parser(
        "interpret",
        help="Render rules into human-readable formulas.",
        description=(
            "Interpret saved rules.json artifacts, or mine a fresh rule set first and then print the "
            "interpreted formulas."
        ),
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(interpret)
    add_grammar_spec_arg(interpret)
    add_input_arg(interpret)
    add_limit_arg(interpret)
    add_rules_arg(interpret)
    add_learner_arg(interpret)
    add_stall_timeout_arg(interpret)
    add_hittingset_backend_arg(interpret)
    add_runs_dir_arg(interpret)
    add_output_arg(interpret)

    entails = subparsers.add_parser(
        "entails",
        help="Check whether a query is entailed by a rule set.",
        description=(
            "Run a theory-level entailment query against saved rules.json artifacts, or mine a fresh "
            "rule set first and then ask the query."
        ),
        formatter_class=CliFormatter,
    )
    add_dataset_spec_arg(entails)
    add_grammar_spec_arg(entails)
    add_input_arg(entails)
    add_limit_arg(entails)
    add_rules_arg(entails)
    add_query_arg(entails)
    add_learner_arg(entails)
    add_stall_timeout_arg(entails)
    add_hittingset_backend_arg(entails)
    add_runs_dir_arg(entails)

    return parser


def write_stdout(text: str) -> None:
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


def write_json(data: object) -> None:
    write_stdout(json.dumps(data, indent=2))


def write_rich_json(data: object) -> None:
    rich_print(JSON.from_data(data, indent=2))


def write_text_file(path: str | Path, text: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text if text.endswith("\n") else f"{text}\n")


def build_fit_kwargs(args: argparse.Namespace) -> dict[str, object]:
    return {
        "input_path": getattr(args, "input", None),
        "learner": getattr(args, "learner", LearnerKind.HITTING_SET.value),
        "limit": getattr(args, "limit", None),
        "stall_timeout": getattr(args, "stall_timeout", None),
        "hitting_set_backend": getattr(args, "hittingset_backend", HittingSetBackend.AUTO.value),
    }


def build_miner(args: argparse.Namespace) -> NetNomosMiner:
    return NetNomosMiner.from_files(
        dataset_spec=args.dataset_spec,
        grammar_spec=args.grammar_spec,
        runs_dir=getattr(args, "runs_dir", "runs"),
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(getattr(args, "log_level", "INFO"))
    if args.command == "show-dataset":
        spec = load_dataset_spec(args.dataset_spec)
        write_stdout(spec.model_dump_json(indent=2))
        return 0
    if args.command == "show-grammar":
        spec = load_grammar_spec(args.grammar_spec)
        write_stdout(spec.model_dump_json(indent=2))
        return 0
    if args.command == "prepare":
        spec = load_dataset_spec(args.dataset_spec)
        miner = NetNomosMiner(spec, GrammarSpec(name="prepare-only"))
        prepared = miner.prepare(input_path=args.input, limit=args.limit)
        write_json({
            "rows": len(prepared.dataframe),
            "columns": list(prepared.dataframe.columns),
            "context_families": prepared.context_families,
            "source_type": prepared.source_type.value,
            "configured_exclude_fields": prepared.configured_exclude_fields,
            "auto_excluded_fields": prepared.excluded_fields,
            "excluded_fields": prepared.effective_excluded_fields,
        })
        return 0

    miner = build_miner(args)

    if args.command == "mine":
        result = miner.fit(**build_fit_kwargs(args))
        write_rich_json({
            "run_dir": str(result.run_dir),
            "rules": len(result.rules),
            "predicates": len(result.predicates),
            "fit_metadata": result.fit_metadata,
            "configured_exclude_fields": result.prepared.configured_exclude_fields,
            "auto_excluded_fields": result.prepared.excluded_fields,
            "excluded_fields": result.prepared.effective_excluded_fields,
        })
        return 0

    if args.command == "validate":
        if args.rules:
            rules = miner.load_rules(args.rules)
            write_json(miner.validate_rules(rules, input_path=args.input, limit=args.limit))
            return 0
        miner.fit(**build_fit_kwargs(args))
        write_json(miner.validate())
        return 0

    if args.command == "interpret":
        if args.rules:
            rules = miner.load_rules(args.rules)
            semantic_values = miner.load_semantic_values_for_rules(args.rules)
            lines = miner.interpret_rules(rules, input_path=args.input, limit=args.limit, semantic_values=semantic_values)
            text = "\n".join(lines)
            if args.output:
                write_text_file(args.output, text)
                write_json({
                    "output": str(Path(args.output)),
                    "rules": len(lines),
                })
                return 0
            write_stdout(text)
            return 0
        miner.fit(**build_fit_kwargs(args))
        lines = miner.interpret()
        text = "\n".join(lines)
        if args.output:
            write_text_file(args.output, text)
            write_json({
                "output": str(Path(args.output)),
                "rules": len(lines),
            })
            return 0
        write_stdout(text)
        return 0

    if args.command == "entails":
        if args.rules:
            rules = miner.load_rules(args.rules)
            entailed = miner.entails_with_rules(args.query, rules, input_path=args.input, limit=args.limit)
        else:
            miner.fit(**build_fit_kwargs(args))
            entailed = miner.entails(parse_formula(args.query))
        write_json({
            "entailed": entailed,
        })
        return 0

    return 1
