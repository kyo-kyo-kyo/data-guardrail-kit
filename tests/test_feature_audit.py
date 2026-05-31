from data_guardrail_kit.feature_audit import audit_feature_names


def test_feature_audit_flags_leakage_tokens() -> None:
    checks = audit_feature_names(["customer_id", "future_discount", "score_label"])

    flagged = [check["column"] for check in checks if check["status"] == "WARN"]

    assert "future_discount" in flagged
    assert "score_label" in flagged


def test_feature_audit_passes_clean_names() -> None:
    checks = audit_feature_names(["customer_id", "signup_month"])

    assert checks == [
        {
            "check": "feature_leakage_token",
            "status": "PASS",
            "value": "no suspicious feature names",
        }
    ]
