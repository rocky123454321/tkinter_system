

from __future__ import annotations

from typing import Any

from models.RentalModel import RentalModel


class RentalController:
    @staticmethod
    def initialize_rentals_table() -> None:

        RentalModel.create_rentals_table()

    @staticmethod
    def handle_list_all_bookings() -> list[dict[str, Any]]:

        return RentalModel.get_rentals_joined()

    @staticmethod
    def handle_list_user_bookings(*, user_id: int) -> list[dict[str, Any]]:

        return RentalModel.get_rentals_joined_by_user(user_id)

    @staticmethod
    def handle_confirm_booking(
        *,
        user_id: int,
        room_number: str,
        start_date: str,
        end_date: str,
        checkin_time: str,
        checkout_time: str,
        payment_status: str,
    ) -> bool:

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
    def handle_approve_booking(*, rental_id: int) -> bool:
        return RentalModel.approve_booking(rental_id)

    @staticmethod
    def handle_check_in(*, rental_id: int) -> bool:
        return RentalModel.check_in(rental_id)

    @staticmethod
    def handle_check_out(*, rental_id: int) -> bool:
        return RentalModel.check_out(rental_id)

    @staticmethod
    def handle_cancel_booking(*, rental_id: int) -> bool:
        return RentalModel.cancel_rental(rental_id)

