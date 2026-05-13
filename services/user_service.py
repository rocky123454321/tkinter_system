"""User service: business rules for regular user flow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from  repositories.user_repository import UserRepository
from  utils.validation_utils import is_digits, require_non_empty


@dataclass(frozen=True)
class LoginResult:
    """Result returned by the login use-case."""

    user: dict[str, Any] | None


class UserService:
    """Business logic for user authentication and signup."""

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

        UserRepository.create_user_table()
        UserRepository.ensure_admin_user(
            email=admin_email,
            password=admin_password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

    @staticmethod
    def login(*, email: str, password: str) -> LoginResult:
        """Authenticate a user."""

        require_non_empty(email, "Email")
        require_non_empty(password, "Password")

        user = UserRepository.verify_user(email, password)
        if user is None:
            return LoginResult(user=None)
        return LoginResult(user=user)

    @staticmethod
    def signup(
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
        confirm_password: str,
        role: str,
    ) -> bool:
        """Create a new user with the same validations as before."""

        for field_value, field_name in [
            (first_name, "First Name"),
            (last_name, "Last Name"),
            (email, "Email"),
            (phone, "Phone"),
            (password, "Password"),
            (confirm_password, "Confirm Password"),
        ]:
            require_non_empty(field_value, field_name)

        if len(phone) != 11:
            return False
        if not is_digits(phone):
            return False
        if not phone.startswith("0"):
            return False

        if password != confirm_password:
            return False

        return UserRepository.add_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            role=role,
        )

    @staticmethod
    def list_all_guests() -> list[dict[str, Any]]:
        """Return all guest users."""

        return UserRepository.get_all_guests()

    @staticmethod
    def get_profile(user_id: int, *, role: str | None = None) -> dict[str, Any] | None:
        """Return a user profile by id."""

        return UserRepository.get_user_by_id(user_id, role=role)

    @staticmethod
    def update_profile(
        user_id: int,
        *,
        first_name: str,
        last_name: str,
        phone: str,
        role: str | None = None,
    ) -> bool:
        """Update a user profile."""

        require_non_empty(first_name, "First Name")
        require_non_empty(last_name, "Last Name")
        return UserRepository.update_user_profile(
            user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )

    @staticmethod
    def change_password(
        user_id: int,
        *,
        current_password: str,
        new_password: str,
        role: str | None = None,
    ) -> tuple[bool, str]:
        """Change a user's password."""

        require_non_empty(current_password, "Current Password")
        require_non_empty(new_password, "New Password")
        return UserRepository.change_user_password(
            user_id,
            current_password=current_password,
            new_password=new_password,
            role=role,
        )

