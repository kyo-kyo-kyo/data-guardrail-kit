from __future__ import annotations

from typing import Any

import pandas as pd


def audit_quality(df: pd.DataFrame, id_columns: list[str]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    row_count = len(df)

    for column in df.columns:
        text = df[column].fillna("").astype(str).str.strip()
        missing = int(text.eq("").sum())
        rate = float(missing / row_count) if row_count else 0.0
        checks.append(
            {
                "check": "missing_rate",
                "column": column,
                "status": "PASS" if rate <= 0.2 else "WARN",
                "value": round(rate, 4),
            }
        )

    for column in id_columns:
        if column not in df.columns:
            checks.append(
                {
                    "check": "id_column_present",
                    "column": column,
                    "status": "FAIL",
                    "value": "missing",
                }
            )
            continue
        normalized = df[column].fillna("").astype(str).str.strip()
        duplicate_count = int(normalized[normalized != ""].duplicated().sum())
        unique_count = int(normalized[normalized != ""].nunique())
        checks.extend(
            [
                {
                    "check": "duplicate_id",
                    "column": column,
                    "status": "PASS" if duplicate_count == 0 else "FAIL",
                    "value": duplicate_count,
                },
                {
                    "check": "unique_values",
                    "column": column,
                    "status": "INFO",
                    "value": unique_count,
                },
            ]
        )

    return checks
