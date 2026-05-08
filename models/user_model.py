import sqlite3
from database.database_config import get_db_connection


class UserModel:

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
        """Verify user login credentials."""
        UserModel.create_user_table()
        conn = get_db_connection()
        if conn is None:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password),
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
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

