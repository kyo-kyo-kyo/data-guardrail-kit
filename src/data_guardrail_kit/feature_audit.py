from __future__ import annotations

from typing import Any, Iterable


DEFAULT_LEAKAGE_TOKENS = (
    "target",
    "label",
    "outcome",
    "result",
    "payout",
    "future",
)


def audit_feature_names(
    feature_names: Iterable[str],
    leakage_tokens: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    tokens = [token.lower() for token in (leakage_tokens or DEFAULT_LEAKAGE_TOKENS)]
    checks: list[dict[str, Any]] = []
    for feature in feature_names:
        lower = str(feature).lower()
        hits = [token for token in tokens if token in lower]
        if hits:
            checks.append(
                {
                    "check": "feature_leakage_token",
                    "column": str(feature),
                    "status": "WARN",
                    "value": ",".join(hits),
                }
            )
    if not checks:
        checks.append(
            {
                "check": "feature_leakage_token",
                "status": "PASS",
                "value": "no suspicious feature names",
            }
        )
    return checks
