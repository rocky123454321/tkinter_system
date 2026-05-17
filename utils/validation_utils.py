"""Input validation helpers (stateless)."""

from __future__ import annotations

from utils import ValidationError


def require_non_empty(value: str, field_name: str) -> None:
    """Raise ValidationError if a string is empty/blank."""

    if not value or not value.strip():
        raise ValidationError(f"{field_name} is required.")


def is_digits(value: str) -> bool:
    """Return True if the given string contains only digits and is non-empty."""

    return bool(value) and value.isdigit()

