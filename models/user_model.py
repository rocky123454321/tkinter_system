import sqlite3

from  database.database_config import get_db_connection


class UserModel:

    @staticmethod
    def ensure_admin_user(email: str, password: str, first_name: str = "Admin", last_name: str = "Temp", phone: str = ""):
        """Create a temporary admin user if it doesn't exist yet."""
        UserModel.create_user_table()
        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE email = ? AND role = 'admin'",
                (email,),
            )
            existing = cursor.fetchone()
            if existing:
                return True

            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, email, phone, password, role, status)
                VALUES (?, ?, ?, ?, ?, 'admin', 'active')
                """,
                (first_name, last_name, email, phone, password),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:

            return False
        except sqlite3.Error as e:
            print(f"Error ensuring admin user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def create_user_table():
        """Create users table if it doesn't exist."""
        conn = get_db_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
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
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

    @staticmethod
    def add_user(first_name, last_name, email, phone, password, role="user", status="active"):
        """Insert a new user."""
        UserModel.create_user_table()
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
            print("Email already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def verify_user(email, password):
        """Verify user login credentials.

        Returns a dict-like row so views can use: user["role"], user["first_name"].
        """
        UserModel.create_user_table()
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
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id: int, *, role: str | None = None):
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            query = "SELECT id, first_name, last_name, email, phone, role FROM users WHERE id = ?"
            params: tuple[object, ...] = (user_id,)
            if role:
                query += " AND role = ?"
                params = (user_id, role)

            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_guest():
        """Get all guests with their latest booking status."""
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
                    COALESCE(r.status, 'No Booking') as purchase_status
                FROM users u
                LEFT JOIN (
                    SELECT user_id, status
                    FROM rentals
                    WHERE id IN (SELECT MAX(id) FROM rentals GROUP BY user_id)
                ) r ON u.id = r.user_id
                WHERE u.role = 'user'
                """
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database Error in get_all_guest: {e}")
            return []
        finally:
            conn.close()

