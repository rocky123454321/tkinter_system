"""Room service: business rules for room inventory."""

from __future__ import annotations

from typing import Any

from  repositories.room_repository import RoomRepository


class RoomService:
    """Business logic for room inventory."""

    @staticmethod
    def initialize_room_table() -> None:
        """Ensure the rooms table exists."""

        RoomRepository.create_room_table()

    @staticmethod
    def seed_default_rooms() -> None:
        """Seed the default room set."""

        RoomRepository.seed_rooms()

    @staticmethod
    def list_rooms() -> list[dict[str, Any]]:
        """Return all rooms."""

        return RoomRepository.get_all_rooms()

    @staticmethod
    def list_available_rooms() -> list[dict[str, Any]]:
        """Return only available rooms."""

        return RoomRepository.get_available_rooms()

    @staticmethod
    def get_room_counts() -> dict[str, int]:
        """Return room status counts."""

        return RoomRepository.get_room_counts()

    @staticmethod
    def update_room_status(room_number: str, new_status: str) -> bool:
        """Update a room status."""

        return RoomRepository.update_room_status(room_number, new_status)
