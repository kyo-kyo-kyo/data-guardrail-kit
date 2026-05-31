from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_ENCODINGS = ("utf-8-sig", "utf-8", "cp932", "shift_jis", "latin-1")
DEFAULT_DELIMITERS = ",;\t|"


@dataclass(frozen=True)
class LoadedCsv:
    path: Path
    dataframe: pd.DataFrame
    encoding: str
    delimiter: str
    duplicate_columns: list[str]


def _read_text(path: Path, encodings: Iterable[str]) -> tuple[str, str]:
    last_error: Exception | None = None
    raw = path.read_bytes()
    for encoding in encodings:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError as exc:
            last_error = exc
    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"could not decode {path} with configured encodings: {last_error}",
    )


def detect_delimiter(sample: str, delimiters: str = DEFAULT_DELIMITERS) -> str:
    try:
        dialect = csv.Sniffer().sniff(sample[:8192], delimiters=delimiters)
        return dialect.delimiter
    except csv.Error:
        first_line = sample.splitlines()[0] if sample.splitlines() else ""
        counts = {delimiter: first_line.count(delimiter) for delimiter in delimiters}
        return max(counts, key=counts.get) if any(counts.values()) else ","


def duplicate_column_names(header: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for name in header:
        clean = name.strip()
        if clean in seen:
            duplicates.add(clean)
        seen.add(clean)
    return sorted(duplicates)


def read_csv_auto(path: str | Path, encodings: Iterable[str] = DEFAULT_ENCODINGS) -> LoadedCsv:
    csv_path = Path(path)
    text, encoding = _read_text(csv_path, encodings)
    delimiter = detect_delimiter(text)
    header = next(csv.reader(text.splitlines()[:1], delimiter=delimiter), [])
    duplicates = duplicate_column_names(header)
    dataframe = pd.read_csv(csv_path, encoding=encoding, sep=delimiter, dtype="object")
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    return LoadedCsv(
        path=csv_path,
        dataframe=dataframe,
        encoding=encoding,
        delimiter=delimiter,
        duplicate_columns=duplicates,
    )
