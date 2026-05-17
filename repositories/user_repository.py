"""User repository: database access for regular user flow."""

from __future__ import annotations

import logging
import sqlite3
from typing import Any

from config import Role, UserStatus
from  database.database_config import get_db_connection
from utils import DatabaseError

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user-related database operations."""

    @staticmethod
    def create_user_table() -> None:
        """Create the users table if it does not exist."""

        conn = get_db_connection()
        if conn is None:
            return

        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name  TEXT NOT NULL,
                    email      TEXT UNIQUE NOT NULL,
                    phone      TEXT,
                    password   TEXT NOT NULL,
                    status     TEXT NOT NULL DEFAULT 'active',
                    role       TEXT DEFAULT 'user'
                )
                """
            )
            conn.commit()
        except sqlite3.Error as exc:
            logger.error("Error creating users table: %s", exc)
            raise DatabaseError("Failed to create users table") from exc
        finally:
            conn.close()

    @staticmethod
    def ensure_admin_user(
        *,
        email: str,
        password: str,
        first_name: str = "Admin",
        last_name: str = "Temp",
        phone: str = "",
    ) -> bool:
        """Ensure an admin user exists.

        Returns:
            True if admin already existed or was created; False otherwise.
        """

        UserRepository.create_user_table()
        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE email = ? AND role = ?",
                (email, Role.ADMIN),
            )
            existing = cursor.fetchone()
            if existing:
                return True

            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, email, phone, password, role, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, email, phone, password, Role.ADMIN, UserStatus.ACTIVE),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:

            return False
        except sqlite3.Error as exc:
            logger.error("Error ensuring admin user: %s", exc)
            return False
        finally:
            conn.close()

    @staticmethod
    def add_user(
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
        role: str = Role.USER,
        status: str = UserStatus.ACTIVE,
    ) -> bool:
        """Insert a new user."""

        UserRepository.create_user_table()
        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, email, phone, password, role, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, email, phone, password, role, status),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as exc:
            logger.error("Error adding user: %s", exc)
            return False
        finally:
            conn.close()

    @staticmethod
    def verify_user(email: str, password: str) -> dict[str, Any] | None:
        """Verify user login credentials."""

        UserRepository.create_user_table()
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, first_name, last_name, email, phone, password, status, role
                FROM users
                WHERE email = ? AND password = ?
                """,
                (email, password),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            keys = ["id", "first_name", "last_name", "email", "phone", "password", "status", "role"]
            return dict(zip(keys, row))
        except sqlite3.Error as exc:
            logger.error("Error verifying user: %s", exc)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_guests() -> list[dict[str, Any]]:
        """Return all users with guest role and their latest booking status."""

        conn = get_db_connection()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.phone,
                    COALESCE(r.status, 'No Booking') AS purchase_status
                FROM users u
                LEFT JOIN (
                    SELECT user_id, status
                    FROM rentals
                    WHERE id IN (SELECT MAX(id) FROM rentals GROUP BY user_id)
                ) r ON u.id = r.user_id
                WHERE u.role = ?
                """,
                (Role.USER,),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as exc:
            logger.error("Error fetching guests: %s", exc)
            return []
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id: int, *, role: str | None = None) -> dict[str, Any] | None:
        """Return one user profile by id, optionally constrained by role."""

        conn = get_db_connection()
        if conn is None:
            return None

        query = """
            SELECT id, first_name, last_name, email, phone, role
            FROM users
            WHERE id = ?
        """
        params: tuple[Any, ...] = (user_id,)
        if role:
            query += " AND role = ?"
            params = (user_id, role)

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as exc:
            logger.error("Error fetching user profile: %s", exc)
            return None
        finally:
            conn.close()

    @staticmethod
    def update_user_profile(
        user_id: int,
        *,
        first_name: str,
        last_name: str,
        phone: str,
        role: str | None = None,
    ) -> bool:
        """Update a user's editable profile fields."""

        conn = get_db_connection()
        if conn is None:
            return False

        query = """
            UPDATE users
            SET first_name = ?, last_name = ?, phone = ?
            WHERE id = ?
        """
        params: tuple[Any, ...] = (first_name, last_name, phone, user_id)
        if role:
            query += " AND role = ?"
            params = (first_name, last_name, phone, user_id, role)

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as exc:
            logger.error("Error updating user profile: %s", exc)
            return False
        finally:
            conn.close()

    @staticmethod
    def change_user_password(
        user_id: int,
        *,
        current_password: str,
        new_password: str,
        role: str | None = None,
    ) -> tuple[bool, str]:
        """Change a user's password after checking the current password."""

        conn = get_db_connection()
        if conn is None:
            return False, "Database error"

        query = "SELECT password FROM users WHERE id = ?"
        params: tuple[Any, ...] = (user_id,)
        if role:
            query += " AND role = ?"
            params = (user_id, role)

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return False, "User not found"
            if row["password"] != current_password:
                return False, "Current password is incorrect"

            update_query = "UPDATE users SET password = ? WHERE id = ?"
            update_params: tuple[Any, ...] = (new_password, user_id)
            if role:
                update_query += " AND role = ?"
                update_params = (new_password, user_id, role)

            cursor.execute(update_query, update_params)
            conn.commit()
            if cursor.rowcount <= 0:
                return False, "Failed to change password."
            return True, ""
        except sqlite3.Error as exc:
            logger.error("Error changing user password: %s", exc)
            return False, "Database error"
        finally:
            conn.close()

