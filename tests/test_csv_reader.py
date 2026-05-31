from pathlib import Path

from data_guardrail_kit.csv_reader import detect_delimiter, duplicate_column_names, read_csv_auto


def test_detect_delimiter_semicolon() -> None:
    assert detect_delimiter("a;b;c\n1;2;3\n") == ";"


def test_duplicate_column_names() -> None:
    assert duplicate_column_names(["id", "name", "id"]) == ["id"]


def test_read_csv_auto(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    path.write_text("id|value\nA|1\n", encoding="utf-8")

    loaded = read_csv_auto(path)

    assert loaded.encoding in {"utf-8", "utf-8-sig"}
    assert loaded.delimiter == "|"
    assert loaded.dataframe.shape == (1, 2)
