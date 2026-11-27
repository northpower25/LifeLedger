"""SQLite schema and transaction helpers. Sensitive payloads are AEAD encrypted."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = "1"
SCHEMA = (Path(__file__).with_name("schema.sql")).read_text(encoding="utf-8")


def connect(path: str | Path) -> sqlite3.Connection:
    database_path = Path(path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.executescript(SCHEMA)
    connection.execute(
        "INSERT OR IGNORE INTO metadata(key, value) VALUES('schema_version', ?)",
        (SCHEMA_VERSION,),
    )
    connection.commit()
    return connection


@contextmanager
def connection(path: str | Path) -> Iterator[sqlite3.Connection]:
    opened = connect(path)
    try:
        yield opened
    finally:
        opened.close()


@contextmanager
def transaction(path: str | Path) -> Iterator[sqlite3.Connection]:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
