from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def build_markdown_report(
    *,
    input_path: Path,
    encoding: str,
    delimiter: str,
    row_count: int,
    column_count: int,
    checks: list[dict[str, Any]],
) -> str:
    statuses = Counter(str(check.get("status", "INFO")) for check in checks)
    delimiter_label = "\\t" if delimiter == "\t" else delimiter
    lines = [
        "# Data Guardrail Report",
        "",
        f"- generated_at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- input: `{input_path}`",
        f"- rows: {row_count}",
        f"- columns: {column_count}",
        f"- encoding: `{encoding}`",
        f"- delimiter: `{delimiter_label}`",
        "",
        "## Status Summary",
        "",
        _table(
            [{"status": key, "count": value} for key, value in sorted(statuses.items())],
            ["status", "count"],
        ),
        "",
        "## Checks",
        "",
        _table(checks, ["check", "column", "status", "expected", "value"]),
        "",
    ]
    return "\n".join(lines)


def write_report(path: str | Path, content: str) -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    return report_path
