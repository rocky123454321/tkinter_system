"""Global reusable utilities.

This package also re-exports app-wide exception types.
"""

from .app_exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    DatabaseError,
)

__all__ = [
    "AppError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "DatabaseError",
]


