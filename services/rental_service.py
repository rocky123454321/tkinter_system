"""Rental service: business rules for regular user rental flow.

This service currently delegates to the existing RentalModel logic to
avoid behavior changes, while keeping controllers free of database calls.
"""

from __future__ import annotations

from typing import Any

from  repositories.rental_repository import RentalRepository


class RentalService:
    @staticmethod
    def initialize_rentals_table() -> None:
        RentalRepository.create_rentals_table()

    @staticmethod
    def list_all_bookings() -> list[dict[str, Any]]:
        return RentalRepository.get_all_rentals_joined()

    @staticmethod
    def list_user_bookings(user_id: int) -> list[dict[str, Any]]:
        return RentalRepository.get_user_rentals_joined(user_id)

    @staticmethod
    def confirm_booking(
        *,
        user_id: int,
        room_number: str,
        start_date: str,
        end_date: str,
        checkin_time: str,
        checkout_time: str,
        payment_status: str,
    ) -> bool:
        """Create an active reservation and return whether it succeeded."""

        return RentalRepository.create_reservation(
            user_id=user_id,
            room_number=room_number,
            start_date=start_date,
            end_date=end_date,
            checkin_time=checkin_time,
            checkout_time=checkout_time,
            payment_status=payment_status,
        )

    @staticmethod
    def approve_user_booking(rental_id: int) -> bool:

        return RentalRepository.approve_booking(rental_id)

    @staticmethod
    def check_in_booking(rental_id: int) -> bool:

        return RentalRepository.check_in(rental_id)

    @staticmethod
    def check_out_booking(rental_id: int) -> bool:

        return RentalRepository.check_out(rental_id)

    @staticmethod
    def cancel_booking(rental_id: int) -> bool:
        return RentalRepository.cancel_booking(rental_id)

