"""Environment config and app settings.

This project is a Tkinter application; config is kept minimal and pure.
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

