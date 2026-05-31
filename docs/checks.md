# Checks

## CSV Loading

The reader tries common encodings and uses `csv.Sniffer` to detect the delimiter. If sniffing fails, it falls back to counting common delimiter characters in the header line.

## Schema Checks

Schema checks cover required columns, duplicate columns, basic type conversion, and per-column uniqueness rules.

## Quality Checks

Quality checks calculate missing rates for every column and duplicate counts for configured ID columns.

## Feature Audit

Feature audit scans column names for configurable leakage tokens. The default list is:

- `target`
- `label`
- `outcome`
- `result`
- `payout`
- `future`

These matches are warnings, not automatic proof of leakage. They are meant to prompt review.
