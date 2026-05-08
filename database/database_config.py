from __future__ import annotations
from pathlib import Path
import sqlite3
from typing import Optional



DB_PATH = Path(__file__).resolve().parent / "_db.sqlite"
def get_db_connection() -> Optional[sqlite3.Connection]:
    try:
        connection = sqlite3.connect(str(DB_PATH.absolute()) , timeout=10)
        connection.execute("PRAGMA journal_mode=WAL;")
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as exc:
        print(f"Database connection error: {exc}")
        return None

