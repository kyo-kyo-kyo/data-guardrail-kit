from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


SCHEMA_TYPES = {"string", "integer", "number", "boolean", "date"}


@dataclass(frozen=True)
class ColumnRule:
    name: str
    type_name: str = "string"
    required: bool = False
    unique: bool = False


@dataclass(frozen=True)
class Schema:
    columns: dict[str, ColumnRule] = field(default_factory=dict)
    id_columns: list[str] = field(default_factory=list)
    leakage_tokens: list[str] = field(default_factory=list)


def _parse_scalar(value: str) -> Any:
    text = value.strip().strip('"').strip("'")
    lower = text.lower()
    if lower in {"true", "yes"}:
        return True
    if lower in {"false", "no"}:
        return False
    if lower in {"null", "none", "~"}:
        return None
    return text


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_column: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0 and stripped.endswith(":"):
            current_section = stripped[:-1]
            current_column = None
            result[current_section] = {} if current_section == "columns" else []
            continue

        if stripped.startswith("- ") and current_section:
            item = _parse_scalar(stripped[2:])
            result.setdefault(current_section, []).append(item)
            continue

        if current_section == "columns" and indent == 2 and stripped.endswith(":"):
            current_column = stripped[:-1]
            result["columns"][current_column] = {}
            continue

        if current_section == "columns" and current_column and indent >= 4 and ":" in stripped:
            key, value = stripped.split(":", 1)
            result["columns"][current_column][key.strip()] = _parse_scalar(value)

    return result


def load_schema(path: str | Path) -> Schema:
    schema_path = Path(path)
    text = schema_path.read_text(encoding="utf-8")
    if schema_path.suffix.lower() == ".json":
        raw = json.loads(text)
    else:
        raw = _parse_simple_yaml(text)

    columns: dict[str, ColumnRule] = {}
    for name, spec in raw.get("columns", {}).items():
        if not isinstance(spec, dict):
            spec = {}
        type_name = str(spec.get("type", "string")).lower()
        if type_name not in SCHEMA_TYPES:
            raise ValueError(f"unsupported schema type for {name}: {type_name}")
        columns[name] = ColumnRule(
            name=name,
            type_name=type_name,
            required=bool(spec.get("required", False)),
            unique=bool(spec.get("unique", False)),
        )

    return Schema(
        columns=columns,
        id_columns=[str(value) for value in raw.get("id_columns", [])],
        leakage_tokens=[str(value).lower() for value in raw.get("leakage_tokens", [])],
    )


def _type_failures(series: pd.Series, type_name: str) -> int:
    non_empty = series.dropna()
    non_empty = non_empty[non_empty.astype(str).str.strip() != ""]
    if non_empty.empty or type_name == "string":
        return 0
    if type_name == "integer":
        parsed = pd.to_numeric(non_empty, errors="coerce")
        return int((parsed.isna() | parsed.mod(1).ne(0)).sum())
    if type_name == "number":
        return int(pd.to_numeric(non_empty, errors="coerce").isna().sum())
    if type_name == "boolean":
        allowed = {"true", "false", "1", "0", "yes", "no", "y", "n"}
        return int((~non_empty.astype(str).str.strip().str.lower().isin(allowed)).sum())
    if type_name == "date":
        return int(pd.to_datetime(non_empty, errors="coerce").isna().sum())
    return 0


def audit_schema(df: pd.DataFrame, schema: Schema, duplicate_columns: list[str] | None = None) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    duplicate_columns = duplicate_columns or []
    checks.append(
        {
            "check": "duplicate_columns",
            "status": "PASS" if not duplicate_columns else "FAIL",
            "value": ",".join(duplicate_columns),
        }
    )

    for name, rule in schema.columns.items():
        present = name in df.columns
        required_missing = rule.required and not present
        checks.append(
            {
                "check": "required_column",
                "column": name,
                "status": "FAIL" if required_missing else "PASS",
                "value": "present" if present else "missing",
            }
        )
        if not present:
            continue

        failures = _type_failures(df[name], rule.type_name)
        checks.append(
            {
                "check": "type_check",
                "column": name,
                "expected": rule.type_name,
                "status": "PASS" if failures == 0 else "WARN",
                "value": failures,
            }
        )

        if rule.unique:
            duplicate_count = int(df[name].dropna().astype(str).duplicated().sum())
            checks.append(
                {
                    "check": "schema_uniqueness",
                    "column": name,
                    "status": "PASS" if duplicate_count == 0 else "FAIL",
                    "value": duplicate_count,
                }
            )

    return checks
