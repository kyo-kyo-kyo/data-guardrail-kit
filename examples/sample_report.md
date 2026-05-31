# Data Guardrail Report

- generated_at: 2026-06-01T00:00:00+00:00
- input: `examples/sample_input.csv`
- rows: 4
- columns: 6
- encoding: `utf-8-sig`
- delimiter: `,`

## Status Summary

| status | count |
| --- | --- |
| FAIL | 2 |
| INFO | 1 |
| PASS | 13 |
| WARN | 4 |

## Checks

| check | column | status | expected | value |
| --- | --- | --- | --- | --- |
| duplicate_columns |  | PASS |  |  |
| required_column | customer_id | PASS |  | present |
| type_check | customer_id | PASS | string | 0 |
| schema_uniqueness | customer_id | FAIL |  | 1 |
| required_column | signup_date | PASS |  | present |
| type_check | signup_date | PASS | date | 0 |
| required_column | monthly_spend | PASS |  | present |
| type_check | monthly_spend | WARN | number | 1 |
| required_column | is_active | PASS |  | present |
| type_check | is_active | PASS | boolean | 0 |
| missing_rate | customer_id | PASS |  | 0.0 |
| missing_rate | signup_date | WARN |  | 0.25 |
| missing_rate | monthly_spend | PASS |  | 0.0 |
| missing_rate | is_active | PASS |  | 0.0 |
| missing_rate | future_discount | PASS |  | 0.0 |
| missing_rate | outcome_status | PASS |  | 0.0 |
| duplicate_id | customer_id | FAIL |  | 1 |
| unique_values | customer_id | INFO |  | 3 |
| feature_leakage_token | future_discount | WARN |  | future |
| feature_leakage_token | outcome_status | WARN |  | outcome |
