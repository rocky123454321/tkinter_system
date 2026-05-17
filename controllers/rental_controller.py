

from __future__ import annotations

from typing import Any

from services.rental_service import RentalService


class RentalController:
    @staticmethod
    def initialize_rentals_table() -> None:

        RentalService.initialize_rentals_table()

    @staticmethod
    def handle_list_all_bookings() -> list[dict[str, Any]]:

        return RentalService.list_all_bookings()

    @staticmethod
    def handle_list_user_bookings(*, user_id: int) -> list[dict[str, Any]]:

        return RentalService.list_user_bookings(user_id=user_id)

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

        return RentalService.confirm_booking(
            user_id=user_id,
            room_number=room_number,
            start_date=start_date,
            end_date=end_date,
            checkin_time=checkin_time,
            checkout_time=checkout_time,
            payment_status=payment_status,
        )

    @staticmethod
    def handle_approve_booking(*, rental_id: int) -> bool:
        return RentalService.approve_user_booking(rental_id=rental_id)

    @staticmethod
    def handle_check_in(*, rental_id: int) -> bool:
        return RentalService.check_in_booking(rental_id)

    @staticmethod
    def handle_check_out(*, rental_id: int) -> bool:
        return RentalService.check_out_booking(rental_id)

    @staticmethod
    def handle_cancel_booking(*, rental_id: int) -> bool:
      return RentalService.cancel_booking(rental_id)

