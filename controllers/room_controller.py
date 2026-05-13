"""Room controller: GUI adapter for room inventory actions."""

from __future__ import annotations

from typing import Any

from services.room_service import RoomService


class RoomController:
    """Thin controller that translates GUI events into room service calls."""

    @staticmethod
    def initialize_room_table() -> None:
        """Ensure the rooms table exists."""

        RoomService.initialize_room_table()

    @staticmethod
    def seed_default_rooms() -> None:
        """Seed default room inventory."""

        RoomService.seed_default_rooms()

    @staticmethod
    def handle_list_rooms() -> list[dict[str, Any]]:
        """List all rooms."""

        return RoomService.list_rooms()

    @staticmethod
    def handle_list_available_rooms() -> list[dict[str, Any]]:
        """List only available rooms."""

        return RoomService.list_available_rooms()

    @staticmethod
    def handle_room_counts() -> dict[str, int]:
        """Return room counts grouped by status."""

        return RoomService.get_room_counts()

    @staticmethod
    def handle_update_room_status(*, room_number: str, new_status: str) -> bool:
        """Update a room status."""

        return RoomService.update_room_status(room_number, new_status)
