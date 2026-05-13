"""Hardcoded values used across the application.

Keep UI/business-relevant strings centralized here.
"""

from __future__ import annotations


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

