"""Custom exception types for the application.

This module was moved from `exceptions/app_exceptions.py`.
"""

from __future__ import annotations

__all__ = [
    "AppError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "DatabaseError",
]


class AppError(Exception):
    """Base class for all application exceptions."""


class AuthenticationError(AppError):
    """Raised when authentication fails."""


class AuthorizationError(AppError):
    """Raised when a user is not authorized to perform an action."""


class ValidationError(AppError):
    """Raised when input validation fails."""


class DatabaseError(AppError):
    """Raised when database operations fail."""

