#!/usr/bin/env python3
"""Load payment CSV files into the SQLite schema supplied with this project."""

import csv
import os
import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent / "data"
SCHEMA_DIR = PROJECT_DIR / "schema"
DATABASE_PATH = PROJECT_DIR / "database" / "paytm_payments.db"

SCHEMA_FILES = (
    SCHEMA_DIR / "create_merchants.sql",
    SCHEMA_DIR / "create_users.sql",
    SCHEMA_DIR / "create_ledger.sql",
)

CSV_TABLES = (
    ("merchants", DATA_DIR / "merchants.csv"),
    ("users", DATA_DIR / "users.csv"),
    ("ledger", DATA_DIR / "ledger.csv"),
)


def load_csv(connection: sqlite3.Connection, table: str, csv_path: Path) -> int:
    """Insert every row from one CSV file and return the inserted row count."""
    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {csv_path}")

        columns = reader.fieldnames
        quoted_columns = ", ".join(f'"{column}"' for column in columns)
        placeholders = ", ".join("?" for _ in columns)
        sql = f'INSERT INTO "{table}" ({quoted_columns}) VALUES ({placeholders})'

        rows = [[row[column] for column in columns] for row in reader]
        connection.executemany(sql, rows)
        return len(rows)


def build_database() -> dict[str, int]:
    """Build and validate a fresh database, then atomically replace the output."""
    temporary_path = DATABASE_PATH.with_suffix(".db.tmp")
    temporary_path.unlink(missing_ok=True)
    counts: dict[str, int] = {}

    connection = sqlite3.connect(temporary_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:
            for schema_path in SCHEMA_FILES:
                connection.executescript(schema_path.read_text(encoding="utf-8"))

            for table, csv_path in CSV_TABLES:
                counts[table] = load_csv(connection, table, csv_path)

        foreign_key_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()
        integrity_result = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        if foreign_key_errors:
            raise RuntimeError(f"Foreign-key violations: {foreign_key_errors}")
        if integrity_result != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity_result}")
    except Exception:
        connection.close()
        temporary_path.unlink(missing_ok=True)
        raise
    else:
        connection.close()

    os.replace(temporary_path, DATABASE_PATH)
    return counts


def main() -> None:
    counts = build_database()
    print(f"Created: {DATABASE_PATH}")
    for table, count in counts.items():
        print(f"{table}: {count} rows")
    print("Foreign-key and integrity checks passed.")


if __name__ == "__main__":
    main()
