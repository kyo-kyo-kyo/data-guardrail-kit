"""Utilities for auditing tabular data files."""

from .csv_reader import LoadedCsv, read_csv_auto
from .feature_audit import audit_feature_names
from .quality import audit_quality
from .schema import Schema, audit_schema, load_schema

__all__ = [
    "LoadedCsv",
    "Schema",
    "audit_feature_names",
    "audit_quality",
    "audit_schema",
    "load_schema",
    "read_csv_auto",
]

__version__ = "0.1.0"
