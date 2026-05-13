"""Rental repository: database access for rental flow.

This module remains a thin wrapper around the existing ``models.RentalModel``
to avoid behavior changes while moving app code behind the project package.
"""

from __future__ import annotations

from typing import Any

from models.RentalModel import RentalModel


class RentalRepository:
    """Repository for rental queries and mutations."""

    @staticmethod
    def create_rentals_table() -> None:
        """Create the rentals table if it does not exist."""

        RentalModel.create_rentals_table()

    @staticmethod
    def get_all_rentals_joined() -> list[dict[str, Any]]:
        """Fetch joined rental rows for all users."""

        return RentalModel.get_rentals_joined()

    @staticmethod
    def get_user_rentals_joined(user_id: int) -> list[dict[str, Any]]:
        """Fetch joined rentals for a specific user."""

        rentals = RentalModel.get_rentals_joined_by_user(user_id)
        return rentals

    @staticmethod
    def create_reservation(
        *,
        user_id: int,
        room_number: str,
        start_date: str,
        end_date: str,
        checkin_time: str,
        checkout_time: str,
        payment_status: str,
    ) -> bool:
        """Create an active reservation (keeps existing behavior)."""

        return RentalModel.create_reservation(
            user_id=user_id,
            room_number=room_number,
            status="active",
            start_date=start_date,
            end_date=end_date,
            checkin_time=checkin_time,
            checkout_time=checkout_time,
            payment_status=payment_status,
        )

    @staticmethod
    def approve_booking(rental_id: int) -> bool:
        """Approve/time-gate booking (keeps existing behavior)."""

        return RentalModel.approve_booking(rental_id)

    @staticmethod
    def check_in(rental_id: int) -> bool:
        """Check in a rental."""

        return RentalModel.check_in(rental_id)

    @staticmethod
    def check_out(rental_id: int) -> bool:
        """Check out a rental."""

        return RentalModel.check_out(rental_id)

    @staticmethod
    def cancel_booking(rental_id: int) -> bool:
        """Cancel a rental."""

        return RentalModel.cancel_rental(rental_id)

