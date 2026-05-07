

import sqlite3
from database.database_config import get_db_connection


class UserModel:

    @staticmethod
    def create_user_table():
        # Gagawa ng users table kung wala pa
        conn = get_db_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name  TEXT NOT NULL,
                    email      TEXT UNIQUE NOT NULL,
                    phone      TEXT,
                    password   TEXT NOT NULL,
                    role       TEXT DEFAULT 'user'
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

    @staticmethod
    def add_user(first_name, last_name, email, phone, password, role):
        UserModel.create_user_table()

        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, phone, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, password, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Mangyayari ito kung may same email na sa database
            return False
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def verify_user(email, password):
        # Naghahanap ng user na may matching email at password
        # Returns ang user row kung nahanap None kung hindi
        UserModel.create_user_table()

        conn = get_db_connection()
        if conn is None:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_guest():
        conn = get_db_connection()
        if conn is None: return []

        try:
            cursor = conn.cursor()
            # Siguraduhin na 5 columns ang sineselect mo para gumana ang guest[4]
            cursor.execute("""
                SELECT id, first_name, last_name, email, phone 
                FROM users 
                WHERE role = 'user'
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()


