# Contributing

Thank you for considering a contribution to Data Guardrail Kit.

This project is intentionally small. Contributions should keep the CLI easy to install, easy to run, and focused on tabular data audits.

## Development Setup

```bash
git clone <repository-url>
cd data-guardrail-kit
python -m pip install -e ".[dev]"
python -m pytest
```

## Contribution Guidelines

- Keep examples synthetic. Do not include private, customer, production, or proprietary data.
- Prefer small, focused pull requests.
- Add or update tests for behavior changes.
- Update README or docs when user-facing behavior changes.
- Do not commit generated reports, caches, virtual environments, or build artifacts.

## Running The Sample Audit

```bash
data-guardrail-kit audit \
  --input examples/sample_input.csv \
  --schema examples/simple_schema.yaml \
  --output data_guardrail_report.md
```

The sample data intentionally contains audit findings. The command may exit with status `1` when failing checks are present.

## Reporting Issues

When reporting a bug, include:

- Python version
- operating system
- command used
- minimal synthetic CSV/schema input
- expected and actual behavior
