"""User controller: GUI adapter for request/response logic."""

from __future__ import annotations

from typing import Any

from services.user_service import LoginResult, UserService


class UserController:
    """Thin controller that translates GUI input/output to services."""

    @staticmethod
    def initialize_users(
        *,
        admin_email: str,
        admin_password: str,
        first_name: str = "Admin",
        last_name: str = "Temp",
        phone: str = "",
    ) -> None:
        """Ensure the users table and default admin account exist."""

        UserService.initialize_users(
            admin_email=admin_email,
            admin_password=admin_password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

    @staticmethod
    def handle_login(*, email: str, password: str) -> LoginResult:
        """Handle login action."""

        return UserService.login(email=email, password=password)

    @staticmethod
    def handle_signup(
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
        confirm_password: str,
        role: str,
    ) -> bool:
        """Handle signup action."""

        return UserService.signup(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            confirm_password=confirm_password,
            role=role,
        )

    @staticmethod
    def handle_list_guests() -> list[dict[str, Any]]:
        """Handle the list guests request."""

        return UserService.list_all_guests()

    @staticmethod
    def handle_get_profile(*, user_id: int, role: str | None = None) -> dict[str, Any] | None:
        """Handle profile lookup."""

        return UserService.get_profile(user_id, role=role)

    @staticmethod
    def handle_update_profile(
        *,
        user_id: int,
        first_name: str,
        last_name: str,
        phone: str,
        role: str | None = None,
    ) -> bool:
        """Handle profile update."""

        return UserService.update_profile(
            user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )

    @staticmethod
    def handle_change_password(
        *,
        user_id: int,
        current_password: str,
        new_password: str,
        role: str | None = None,
    ) -> tuple[bool, str]:
        """Handle password change."""

        return UserService.change_password(
            user_id,
            current_password=current_password,
            new_password=new_password,
            role=role,
        )

