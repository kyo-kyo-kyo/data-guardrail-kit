# Usage

Install the package from a cloned repository:

```bash
python -m pip install -e .
```

Run the audit command with a CSV file and a schema file:

```bash
data-guardrail-kit audit \
  --input examples/sample_input.csv \
  --schema examples/simple_schema.yaml \
  --output data_guardrail_report.md
```

The report includes:

- detected encoding and delimiter
- row and column counts
- schema check results
- missing-rate results
- ID duplication results
- suspicious feature-name matches

The command returns exit code `1` when any check has status `FAIL`. Warnings do not fail the command.

The sample data intentionally contains failures so users can see how the report behaves. For a passing dataset, the command exits with status `0`.
