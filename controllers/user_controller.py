"""User controller: GUI adapter for request/response logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config import Role, UserStatus
from models.user_model import UserModel
from utils.validation_utils import is_digits, require_non_empty


@dataclass(frozen=True)
class LoginResult:
    """Result returned by the login use-case."""

    user: dict[str, Any] | None


class UserController:
    """User business + data logic (inlined from services/repositories)."""

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

        UserModel.create_user_table()
        UserModel.ensure_admin_user(
            email=admin_email,
            password=admin_password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

    @staticmethod
    def handle_login(*, email: str, password: str) -> LoginResult:
        require_non_empty(email, "Email")
        require_non_empty(password, "Password")

        user = UserModel.verify_user(email, password)
        return LoginResult(user=user)

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

        return UserModel.add_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            role=role,
            status=UserStatus.ACTIVE,
        )

    @staticmethod
    def handle_list_guests() -> list[dict[str, Any]]:
        rows = UserModel.get_all_guest()
        if not rows:
            return []

        first = rows[0]
        if isinstance(first, dict):
            return rows 

        keys = ["id", "first_name", "last_name", "email", "phone", "purchase_status"]
        return [dict(zip(keys, r)) for r in rows]  

    @staticmethod
    def handle_get_profile(*, user_id: int, role: str | None = None) -> dict[str, Any] | None:
      
        return UserModel.get_user_by_id(user_id=user_id, role=role)


    @staticmethod
    def handle_update_profile(
        *,
        user_id: int,
        first_name: str,
        last_name: str,
        phone: str,
        role: str | None = None,
    ) -> bool:
        require_non_empty(first_name, "First Name")
        require_non_empty(last_name, "Last Name")

        return UserModel.update_user_profile(
            user_id=user_id,
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
        require_non_empty(current_password, "Current Password")
        require_non_empty(new_password, "New Password")

        return UserModel.change_user_password(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password,
            role=role,
        )

