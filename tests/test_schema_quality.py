import pandas as pd

from data_guardrail_kit.quality import audit_quality
from data_guardrail_kit.schema import Schema, ColumnRule, audit_schema


def test_schema_required_type_and_unique_checks() -> None:
    df = pd.DataFrame(
        {
            "customer_id": ["A", "B", "B"],
            "amount": ["1.5", "bad", "3.0"],
        }
    )
    schema = Schema(
        columns={
            "customer_id": ColumnRule("customer_id", required=True, unique=True),
            "amount": ColumnRule("amount", type_name="number"),
            "created_at": ColumnRule("created_at", type_name="date", required=True),
        }
    )

    checks = audit_schema(df, schema)
    failing = [check for check in checks if check["status"] == "FAIL"]
    warnings = [check for check in checks if check["status"] == "WARN"]

    assert any(check["column"] == "customer_id" for check in failing)
    assert any(check["column"] == "created_at" for check in failing)
    assert any(check["column"] == "amount" for check in warnings)


def test_quality_duplicate_id() -> None:
    df = pd.DataFrame({"customer_id": ["A", "A", "B"], "score": [1, None, 3]})

    checks = audit_quality(df, ["customer_id"])

    assert any(
        check["check"] == "duplicate_id"
        and check["column"] == "customer_id"
        and check["value"] == 1
        for check in checks
    )
