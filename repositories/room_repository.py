"""Room repository: database access for room inventory."""

from __future__ import annotations

from typing import Any

from  models.RoomModel import RoomModel


class RoomRepository:
    """Repository for room-related queries and mutations."""

    @staticmethod
    def create_room_table() -> None:
        """Create the rooms table if it does not exist."""

        RoomModel.create_room_table()

    @staticmethod
    def seed_rooms() -> None:
        """Seed default room inventory."""

        RoomModel.seed_rooms()

    @staticmethod
    def get_all_rooms() -> list[dict[str, Any]]:
        """Fetch all rooms."""

        return RoomModel.get_all_rooms()

    @staticmethod
    def get_available_rooms() -> list[dict[str, Any]]:
        """Fetch only available rooms."""

        return RoomModel.get_available_rooms()

    @staticmethod
    def get_room_counts() -> dict[str, int]:
        """Fetch aggregated room status counts."""

        return RoomModel.get_room_counts()

    @staticmethod
    def update_room_status(room_number: str, new_status: str) -> bool:
        """Update a room's availability status."""

        return RoomModel.update_room_status(room_number, new_status)
