# Data Guardrail Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Data Guardrail Kit is a small Python CLI for auditing CSV files before they enter analytics or machine learning workflows.

It checks whether a CSV can be read reliably, whether it matches a schema, whether ID fields are consistent, and whether feature names look suspiciously close to downstream labels or future information.

## Why Use It?

Small data issues often become expensive model or dashboard issues later:

- a required column disappears
- an ID field contains duplicates
- a numeric field silently becomes text
- a feature list includes columns such as `target`, `label`, `outcome`, `result`, `payout`, or `future`
- a generated report is needed for review before data is used downstream

Data Guardrail Kit turns those checks into a repeatable CLI step.

## Features

- CSV encoding auto-detection
- CSV delimiter detection
- Required column checks
- Basic type checks
- Duplicate column detection
- Missing-rate checks
- Duplicate ID checks
- Uniqueness checks
- Feature-name audit for configurable leakage tokens
- Markdown report generation

## Installation

For local development from a cloned repository:

```bash
python -m pip install -e ".[dev]"
```

For normal local use without development tools:

```bash
python -m pip install -e .
```

## Quick Start

```bash
data-guardrail-kit audit \
  --input examples/sample_input.csv \
  --schema examples/simple_schema.yaml \
  --output data_guardrail_report.md
```

The command writes a Markdown report. It exits with status `1` when failing checks are found, which makes it suitable for CI pipelines.

The included sample data intentionally contains findings, so it demonstrates both warnings and failures.

Example terminal output:

```text
report: data_guardrail_report.md
fails: 2 warnings: 4
```

See [examples/sample_report.md](examples/sample_report.md) for an example Markdown report.

## Schema Example

```yaml
columns:
  customer_id:
    type: string
    required: true
    unique: true
  signup_date:
    type: date
    required: true
  monthly_spend:
    type: number
    required: false

id_columns:
  - customer_id

leakage_tokens:
  - target
  - label
  - outcome
  - result
  - payout
  - future
```

Supported types are `string`, `integer`, `number`, `boolean`, and `date`.

The schema parser supports this simple YAML-like structure and JSON files. For complex YAML features, prefer JSON or keep the schema format close to the example above.

## Example Files

- [examples/sample_input.csv](examples/sample_input.csv): synthetic input data
- [examples/simple_schema.yaml](examples/simple_schema.yaml): schema for the sample data
- [examples/sample_report.md](examples/sample_report.md): example audit report

## Project Layout

```text
src/data_guardrail_kit/       package source
examples/                     fully synthetic sample data and report
tests/                        unit tests
docs/                         usage notes
.github/workflows/ci.yml      GitHub Actions test workflow
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Documentation

- [docs/usage.md](docs/usage.md)
- [docs/checks.md](docs/checks.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [CHANGELOG.md](CHANGELOG.md)

## Data Safety

Examples in this repository are synthetic. Do not commit private datasets, credentials, generated local reports, or production files.

## License

MIT
