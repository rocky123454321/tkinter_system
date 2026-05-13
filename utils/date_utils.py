"""Date/time helper functions (stateless)."""

from __future__ import annotations

from datetime import date, datetime


def current_date_str() -> str:
    """Return current date as ISO string (YYYY-MM-DD)."""

    return date.today().strftime("%Y-%m-%d")


def now_datetime() -> datetime:
    """Return current datetime."""

    return datetime.now()


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse a datetime from date and time strings.

    Args:
        date_str: Date in YYYY-MM-DD.
        time_str: Time in HH:MM.

    Returns:
        Parsed datetime.

    Raises:
        ValueError: If parsing fails.
    """

    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

