"""Utility helpers for the user settings feature."""

import logging
import tkinter as tk
from pathlib import Path
from typing import Any

from .constants import (
    BACKGROUND_COLOR,
    BORDER_COLOR,
    CAPTION_FONT,
    CARD_COLOR,
    ENTRY_FONT,
    ENTRY_WIDTH,
    FOCUS_COLOR,
    LABEL_FONT,
    PASSWORD_MASK,
    PRIMARY_TEXT_COLOR,
    PROFILE_IMAGE_PATH,
    PROFILE_IMAGE_SIZE,
    SECONDARY_TEXT_COLOR,
)

logger = logging.getLogger(__name__)


def normalize_text(value: str) -> str:
    """
    Normalize text input by trimming surrounding whitespace.

    Args:
        value: The raw text input.

    Returns:
        The trimmed text.
    """
    return value.strip()


def clear_variables(*variables: tk.StringVar) -> None:
    """
    Reset one or more Tkinter string variables to empty strings.

    Args:
        *variables: The variables to clear.

    Returns:
        None.
    """
    for variable in variables:
        variable.set("")


def create_labeled_entry(
    parent: tk.Widget,
    label_text: str,
    variable: tk.StringVar,
    *,
    is_password: bool = False,
    state: str = tk.NORMAL,
) -> tk.Entry:
    """
    Create a labeled entry field with the settings styling.

    Args:
        parent: The parent widget.
        label_text: The label to show above the entry.
        variable: The Tkinter variable bound to the entry.
        is_password: Whether the value should be masked.
        state: The Tkinter entry state.

    Returns:
        The created entry widget.
    """
    row = tk.Frame(parent, bg=CARD_COLOR)
    row.pack(fill="x", pady=8)

    tk.Label(
        row,
        text=label_text,
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT_COLOR,
        font=LABEL_FONT,
    ).pack(anchor="w")

    entry = tk.Entry(
        row,
        textvariable=variable,
        state=state,
        font=ENTRY_FONT,
        bg=BACKGROUND_COLOR,
        fg=PRIMARY_TEXT_COLOR,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=FOCUS_COLOR,
        width=ENTRY_WIDTH,
        show=PASSWORD_MASK if is_password else "",
    )
    entry.pack(fill="x", ipady=6, pady=(4, 0))
    return entry


def load_profile_image() -> Any | None:
    """
    Load the profile image for display in the settings page.

    Args:
        None.

    Returns:
        A Tk-compatible image object when the asset loads successfully,
        otherwise None.
    """
    try:
        from PIL import Image, ImageTk

        image = Image.open(_get_profile_image_path())
        resized_image = image.resize(PROFILE_IMAGE_SIZE)
        return ImageTk.PhotoImage(resized_image)
    except (ImportError, OSError, tk.TclError) as exc:
        logger.warning("Failed to load profile image: %s", exc)
        return None


def _get_profile_image_path() -> Path:
    """
    Return the configured profile image path.

    Args:
        None.

    Returns:
        The absolute path to the profile image asset.
    """
    return PROFILE_IMAGE_PATH

