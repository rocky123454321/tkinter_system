"""Environment config and app settings.

This project is a Tkinter application; config is kept minimal and pure.

NOTE:
This module also hosts app-wide constants that were previously in
`constants/app_constants.py`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration values."""

    log_level: str = "INFO"


def get_config() -> AppConfig:
    """Return application configuration."""

    return AppConfig()


class Role:
    """User roles."""

    ADMIN = "admin"
    USER = "user"


class UserStatus:
    """User status values."""

    ACTIVE = "active"


class RoomStatus:
    """Room availability/status values."""

    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"


class RentalStatus:
    """Rental lifecycle status."""

    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus:
    """Payment status values."""

    UNPAID = "unpaid"
    PAID = "paid"
    APPROVED = "approved"

