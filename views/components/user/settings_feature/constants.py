"""Styling constants for the user settings helpers."""

from __future__ import annotations

from pathlib import Path

BACKGROUND_COLOR = "#f5f5f7"
BORDER_COLOR = "#d2d2d7"
CARD_COLOR = "#ffffff"
FOCUS_COLOR = "#0071e3"
PRIMARY_TEXT_COLOR = "#1d1d1f"
SECONDARY_TEXT_COLOR = "#86868b"

LABEL_FONT = ("SF Pro Text", 10, "bold")
CAPTION_FONT = ("SF Pro Text", 10)
ENTRY_FONT = ("SF Pro Text", 11)
ENTRY_WIDTH = 30
PASSWORD_MASK = "*"
PROFILE_IMAGE_SIZE = (90, 90)

PROFILE_IMAGE_PATH = Path(__file__).resolve().parents[4] / "assets" / "userProfile.png"
