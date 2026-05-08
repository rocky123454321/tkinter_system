import sqlite3
from database.database_config import get_db_connection


class RentalModel:
    """Rental / Reservation model.

    rentals.status values:
    - active: checked-in / currently occupying room
    - completed: checked-out (finished booking)
    - cancelled: cancelled reservation
    """

    @staticmethod


    def create_rentals_table():
        conn = get_db_connection()
        if conn is None: return

        try:
            # Gagawa lang ng table kung wala pa. Hindi nito buburahin ang existing data.
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rentals (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER NOT NULL,
                    room_id     INTEGER,
                    checkin     TEXT NOT NULL,
                    checkout    TEXT NOT NULL,
                    status      TEXT DEFAULT 'active',
                    created_at  TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )
            conn.commit()
            # Palitan ang message para hindi nakakalito
            print("Database check: Rentals table is ready.") 
        except sqlite3.Error as e:
            print(f"Error creating rentals table: {e}")
        finally:
            conn.close()
        conn = get_db_connection()
        if conn is None: return

        try:
            # NOTE: Do NOT DROP the rentals table on app startup.
            # Dropping it causes all saved bookings to disappear after closing/reopening the app.


            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rentals (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER NOT NULL,
                    room_id     INTEGER,
                    checkin     TEXT NOT NULL,
                    checkout    TEXT NOT NULL,
                    status      TEXT DEFAULT 'active',
                    created_at  TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )
            conn.commit()
            print("Table rentals recreated successfully!")
        except sqlite3.Error as e:
            print(f"Error creating rentals table: {e}")
        finally:
            conn.close()
    @staticmethod
    def get_available_room_for_booking():
        """Deprecated/unused helper (kept for future)."""
        return

    @staticmethod
    def _get_room_id_by_number(room_number: str):
        conn = get_db_connection()
        if conn is None:
            return None
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM rooms WHERE room_number = ?", (room_number,))
            row = cur.fetchone()
            return row["id"] if row else None
        except sqlite3.Error as e:
            print(f"Error getting room id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def _ensure_room_available(room_number: str):
        """Returns True if room exists and is Available."""
        from models.RoomModel import RoomModel

        room_list = RoomModel.get_all_rooms()
        for r in room_list:
            if str(r.get("room_number")) == str(room_number):
                return r.get("status") == "Available"
        return False


    @staticmethod
    def create_reservation(user_id: int, room_number: str, status: str = "active", start_date: str = "",
                           end_date: str = "") -> bool:
        """Create a reservation with check-in and check-out dates."""
        from models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        room_id = RentalModel._get_room_id_by_number(room_number)
        if room_id is None:
            return False

        if status == "active":
            if not RentalModel._ensure_room_available(room_number):
                return False

        try:
            # DAGDAGAN NG checkin AT checkout SA INSERT QUERY
            conn.execute(
                """
                INSERT INTO rentals (user_id, room_id, status, checkin, checkout)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, room_id, status, start_date, end_date),
            )
            conn.commit()

            if status == "active":
                RoomModel.update_room_status(room_number, "Occupied")

            return True
        except sqlite3.Error as e:
            print(f"Error creating reservation: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def get_latest_rental_for_user(user_id: int):
        conn = get_db_connection()
        if conn is None:
            return None
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM rentals
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching latest rental: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    @staticmethod
    def get_rentals_joined():
        """Return rentals with guest + room details kasama ang dates."""
        conn = get_db_connection()
        if conn is None: return []
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    r.id,
                    r.user_id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.phone,
                    r.room_id,
                    rm.room_number,
                    rm.room_type,
                    r.checkin,    -- ISAMA ITO
                    r.checkout,   -- ISAMA ITO
                    r.status,
                    r.created_at
                FROM rentals r
                JOIN users u ON u.id = r.user_id
                LEFT JOIN rooms rm ON rm.id = r.room_id
                ORDER BY r.id DESC
                """
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching rentals: {e}")
            return []
        finally:
            conn.close()
    @staticmethod
    def get_rentals_joined_by_user(user_id: int):
        conn = get_db_connection()
        if conn is None:
            return []
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    r.id,
                    r.user_id,
                    u.first_name,
                    u.last_name,
                    r.room_id,
                    rm.room_number,
                    rm.room_type,
                    r.checkin,    -- DAGDAGAN ITONG LINE
                    r.checkout,   -- DAGDAGAN ITONG LINE
                    r.status,
                    r.created_at
                FROM rentals r
                JOIN users u ON u.id = r.user_id
                LEFT JOIN rooms rm ON rm.id = r.room_id
                WHERE r.user_id = ?
                ORDER BY r.id DESC
                """,
                (user_id,),
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching rentals: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def check_in(rental_id: int) -> bool:
        """Set rental status to active and set room Occupied."""
        from models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cur = conn.cursor()
            cur.execute("SELECT room_id FROM rentals WHERE id = ?", (rental_id,))
            row = cur.fetchone()
            if not row:
                return False
            room_id = row["room_id"]

            cur.execute("SELECT room_number, status FROM rooms WHERE id = ?", (room_id,))
            room_row = cur.fetchone()
            if not room_row:
                return False
            room_number = room_row["room_number"]
            if room_row["status"] != "Available":
                return False

            cur.execute("UPDATE rentals SET status = ? WHERE id = ?", ("active", rental_id))
            conn.commit()

            RoomModel.update_room_status(room_number, "Occupied")
            return True
        except sqlite3.Error as e:
            print(f"Error check-in: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def check_out(rental_id: int) -> bool:
        """Set rental status to completed and set room Available."""
        from models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cur = conn.cursor()
            cur.execute("SELECT room_id FROM rentals WHERE id = ?", (rental_id,))
            row = cur.fetchone()
            if not row:
                return False
            room_id = row["room_id"]

            cur.execute("SELECT room_number FROM rooms WHERE id = ?", (room_id,))
            room_row = cur.fetchone()
            if not room_row:
                return False
            room_number = room_row["room_number"]

            # Debug: verify current status before update
            try:
                cur.execute("SELECT status FROM rentals WHERE id = ?", (rental_id,))
                old_row = cur.fetchone()
                old_status = old_row["status"] if old_row else None
                print(f"[DEBUG] check_out rental_id={rental_id} old_status={old_status} -> completed")
            except Exception as dbg_e:
                print(f"[DEBUG] check_out debug failed: {dbg_e}")

            cur.execute("UPDATE rentals SET status = ? WHERE id = ?", ("completed", rental_id))
            conn.commit()

            # Debug: verify new status
            try:
                cur.execute("SELECT status FROM rentals WHERE id = ?", (rental_id,))
                new_row = cur.fetchone()
                new_status = new_row["status"] if new_row else None
                print(f"[DEBUG] check_out rental_id={rental_id} new_status={new_status}")
            except Exception as dbg_e:
                print(f"[DEBUG] check_out verify failed: {dbg_e}")

            RoomModel.update_room_status(room_number, "Available")
            return True
        except sqlite3.Error as e:
            print(f"Error check-out: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def cancel_rental(rental_id: int) -> bool:
        """Cancel a rental. If room is occupied, release it."""
        from models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False
        try:
            cur = conn.cursor()
            cur.execute("SELECT room_id FROM rentals WHERE id = ?", (rental_id,))
            row = cur.fetchone()
            if not row:
                return False
            room_id = row["room_id"]

            cur.execute("SELECT room_number, status FROM rooms WHERE id = ?", (room_id,))
            room_row = cur.fetchone()
            if not room_row:
                return False
            room_number = room_row["room_number"]

            cur.execute("UPDATE rentals SET status = ? WHERE id = ?", ("cancelled", rental_id))
            conn.commit()

            # if room currently occupied, set back to available
            if room_row["status"] == "Occupied":
                RoomModel.update_room_status(room_number, "Available")

            return True
        except sqlite3.Error as e:
            print(f"Error cancel rental: {e}")
            return False
        finally:
            conn.close()


