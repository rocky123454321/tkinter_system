"""Room controller: GUI adapter for room inventory actions."""

from __future__ import annotations

from typing import Any

from models.RoomModel import RoomModel


class RoomController:
    """Thin controller that translates GUI events into room service calls."""

    @staticmethod
    def initialize_room_table() -> None:
        """Ensure the rooms table exists."""

        RoomModel.create_room_table()

    @staticmethod
    def seed_default_rooms() -> None:
        """Seed default room inventory."""

        RoomModel.seed_rooms()

    @staticmethod
    def handle_list_rooms() -> list[dict[str, Any]]:
        """List all rooms."""

        return RoomModel.get_all_rooms()

    @staticmethod
    def handle_list_available_rooms() -> list[dict[str, Any]]:
        """List only available rooms."""

        return RoomModel.get_available_rooms()

    @staticmethod
    def handle_room_counts() -> dict[str, int]:
        """Return room counts grouped by status."""

        return RoomModel.get_room_counts()

    @staticmethod
    def handle_update_room_status(*, room_number: str, new_status: str) -> bool:
        """Update a room status."""

        return RoomModel.update_room_status(room_number, new_status)
