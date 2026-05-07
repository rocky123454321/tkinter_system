"""Database connection utilities.

This module provides a single entry-point, :func:`get_db_connection`, for
creating SQLite connections used across the application.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Optional


# DB file lives next to this module (database/_db.sqlite)
DB_PATH = Path(__file__).resolve().parent / "_db.sqlite"


def get_db_connection() -> Optional[sqlite3.Connection]:
    """Create a SQLite connection.

    Returns:
        A configured sqlite3 connection (with ``row_factory`` set to
        ``sqlite3.Row``), or ``None`` if the connection fails.
    """

    try:
        connection = sqlite3.connect(str(DB_PATH))
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as exc:
        # Basic robustness: return None so callers can handle the failure.
        print(f"Database connection error: {exc}")
        return None

