from __future__ import annotations

import argparse
from pathlib import Path

from .csv_reader import read_csv_auto
from .feature_audit import DEFAULT_LEAKAGE_TOKENS, audit_feature_names
from .quality import audit_quality
from .report import build_markdown_report, write_report
from .schema import audit_schema, load_schema


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="data-guardrail-kit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a CSV file against a schema.")
    audit.add_argument("--input", required=True, help="Path to the CSV file.")
    audit.add_argument("--schema", required=True, help="Path to the schema file.")
    audit.add_argument(
        "--output",
        default="data_guardrail_report.md",
        help="Markdown report path. Defaults to data_guardrail_report.md.",
    )
    return parser


def run_audit(input_path: str, schema_path: str, output_path: str) -> int:
    loaded = read_csv_auto(input_path)
    schema = load_schema(schema_path)
    leakage_tokens = schema.leakage_tokens or list(DEFAULT_LEAKAGE_TOKENS)

    checks = []
    checks.extend(audit_schema(loaded.dataframe, schema, loaded.duplicate_columns))
    checks.extend(audit_quality(loaded.dataframe, schema.id_columns))
    checks.extend(audit_feature_names(loaded.dataframe.columns, leakage_tokens))

    report = build_markdown_report(
        input_path=Path(input_path),
        encoding=loaded.encoding,
        delimiter=loaded.delimiter,
        row_count=len(loaded.dataframe),
        column_count=len(loaded.dataframe.columns),
        checks=checks,
    )
    report_path = write_report(output_path, report)
    fail_count = sum(1 for check in checks if check.get("status") == "FAIL")
    warn_count = sum(1 for check in checks if check.get("status") == "WARN")
    print(f"report: {report_path}")
    print(f"fails: {fail_count} warnings: {warn_count}")
    return 1 if fail_count else 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "audit":
        return run_audit(args.input, args.schema, args.output)
    parser.error(f"unknown command: {args.command}")
    return 2
