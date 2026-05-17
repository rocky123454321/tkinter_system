import sqlite3

from  database.database_config import get_db_connection


class RentalModel:
    """Rental / Reservation model.

    rentals.status values:
    - active: checked-in / currently occupying room
    - completed: checked-out (finished booking)
    - cancelled: cancelled reservation

    payment_status values:
    - unpaid: hindi pa bayad
    - paid: bayad na sa counter
    - approved: admin-approved na, pero future checkin pa
    """

    @staticmethod
    def create_rentals_table():
        conn = get_db_connection()
        if conn is None:
            return

        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rentals (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id          INTEGER NOT NULL,
                    room_id          INTEGER,

                    -- Dates
                    checkin          TEXT NOT NULL,
                    checkout         TEXT NOT NULL,

                    -- Exact times (HH:MM format, e.g. "14:00")
                    checkin_time     TEXT DEFAULT '14:00',
                    checkout_time    TEXT DEFAULT '12:00',

                    -- Guest details
                    num_guests       INTEGER DEFAULT 1,
                    special_requests TEXT DEFAULT '',

                    -- Payment
                    total_price      REAL DEFAULT 0.0,
                    payment_status   TEXT DEFAULT 'unpaid',
                    payment_method   TEXT DEFAULT 'counter',
                    paid_at          TEXT,

                    -- Booking status
                    status           TEXT DEFAULT 'active',
                    created_at       TEXT DEFAULT (datetime('now')),

                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            new_columns = [
                ("checkin_time",     "TEXT DEFAULT '14:00'"),
                ("checkout_time",    "TEXT DEFAULT '12:00'"),
                ("num_guests",       "INTEGER DEFAULT 1"),
                ("special_requests", "TEXT DEFAULT ''"),
                ("total_price",      "REAL DEFAULT 0.0"),
                ("payment_status",   "TEXT DEFAULT 'unpaid'"),
                ("payment_method",   "TEXT DEFAULT 'counter'"),
                ("paid_at",          "TEXT"),
            ]
            for col_name, col_def in new_columns:
                try:
                    conn.execute(f"ALTER TABLE rentals ADD COLUMN {col_name} {col_def}")
                    print(f"Migration: added column '{col_name}' to rentals.")
                except sqlite3.OperationalError as e:
                    print(f"Migration Error on column '{col_name}': {e}")

                
   

            conn.commit()
            print("Database check: Rentals table is ready.")
        except sqlite3.Error as e:
            print(f"Error creating rentals table: {e}")
        finally:
            conn.close()





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
    def _ensure_room_available(room_number: str) -> bool:
        """Returns True if room exists and is Available."""
        from  models.RoomModel import RoomModel

        room_list = RoomModel.get_all_rooms()
        for r in room_list:
            if str(r.get("room_number")) == str(room_number):
                return r.get("status") == "Available"
        return False

    @staticmethod
    def _compute_total_price(room_number: str, checkin: str, checkout: str) -> float:
        """Compute total price = price_per_night * number_of_nights."""
        from  models.RoomModel import RoomModel
        from datetime import datetime

        try:
            d1 = datetime.strptime(checkin, "%Y-%m-%d")
            d2 = datetime.strptime(checkout, "%Y-%m-%d")
            nights = max((d2 - d1).days, 1)
        except ValueError:
            nights = 1

        room_list = RoomModel.get_all_rooms()
        for r in room_list:
            if str(r.get("room_number")) == str(room_number):
                price_per_night = float(r.get("price", 0))
                return price_per_night * nights
        return 0.0





    @staticmethod
    def create_reservation(
        user_id:          int,
        room_number:      str,
        status:           str  = "active",
        start_date:       str  = "",
        end_date:         str  = "",
        checkin_time:     str  = "14:00",
        checkout_time:    str  = "12:00",
        num_guests:       int  = 1,
        special_requests: str  = "",
        payment_status:   str  = "unpaid",
    ) -> bool:
        """Create a reservation with full details."""
        from  models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        room_id = RentalModel._get_room_id_by_number(room_number)
        if room_id is None:
            return False

        if status == "active":
            if not RentalModel._ensure_room_available(room_number):
                return False

        total_price = RentalModel._compute_total_price(room_number, start_date, end_date)

        try:
            conn.execute(
                """
                INSERT INTO rentals (
                    user_id, room_id, checkin, checkout,
                    checkin_time, checkout_time,
                    num_guests, special_requests,
                    total_price, payment_status, payment_method,
                    paid_at,
                    status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'counter',
                          CASE WHEN ? = 'paid' THEN datetime('now') ELSE NULL END,
                          ?)
                """,
                (
                    user_id, room_id, start_date, end_date,
                    checkin_time, checkout_time,
                    num_guests, special_requests,
                    total_price, payment_status,
                    payment_status,
                    status,
                ),
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
    def approve_booking(rental_id: int) -> bool:
        from models.RoomModel import RoomModel
        from datetime import datetime

        conn = get_db_connection()
        if conn is None:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT room_id, checkin FROM rentals WHERE id = ?",
                (rental_id,),
            )
            row = cur.fetchone()
            if not row:
                return False

            room_id = row["room_id"]
            checkin_date = row["checkin"]
            today = datetime.now().strftime("%Y-%m-%d")

            if checkin_date <= today:
                cur.execute(
                    "UPDATE rentals SET status = 'active', payment_status = 'approved' WHERE id = ?",
                    (rental_id,),
                )
                conn.commit()
                cur.execute("SELECT room_number FROM rooms WHERE id = ?", (room_id,))
                room_row = cur.fetchone()
                if not room_row:
                    return False
                RoomModel.update_room_status(room_row["room_number"], "Occupied")
            else:
                cur.execute(
                    "UPDATE rentals SET status = 'pending', payment_status = 'approved' WHERE id = ?",
                    (rental_id,),
                )
                conn.commit()

            return True
        except sqlite3.Error as e:
            print(f"Error approving booking: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def mark_as_paid(rental_id: int) -> bool:
        """Mark a rental as paid at the counter."""
        from datetime import datetime

        conn = get_db_connection()
        if conn is None:
            return False
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                """
                UPDATE rentals
                SET payment_status = 'paid',
                    payment_method = 'counter',
                    paid_at        = ?
                WHERE id = ?
                """,
                (now, rental_id),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error marking as paid: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_special_requests(rental_id: int, special_requests: str) -> bool:
        """Update the special requests / notes for a rental."""
        conn = get_db_connection()
        if conn is None:
            return False
        try:
            conn.execute(
                "UPDATE rentals SET special_requests = ? WHERE id = ?",
                (special_requests, rental_id),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating special requests: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_checkin_checkout_time(
        rental_id: int,
        checkin_time: str = None,
        checkout_time: str = None,
    ) -> bool:
        """Update check-in or check-out time (HH:MM format)."""
        conn = get_db_connection()
        if conn is None:
            return False
        try:
            if checkin_time:
                conn.execute(
                    "UPDATE rentals SET checkin_time = ? WHERE id = ?",
                    (checkin_time, rental_id),
                )
            if checkout_time:
                conn.execute(
                    "UPDATE rentals SET checkout_time = ? WHERE id = ?",
                    (checkout_time, rental_id),
                )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating times: {e}")
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
    def get_rentals_joined():
        """Return ALL rentals with guest + room details (admin view)."""
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
                    u.email,
                    u.phone,
                    r.room_id,
                    rm.room_number,
                    rm.room_type,
                    rm.price          AS price_per_night,

                    r.checkin,
                    r.checkout,
                    r.checkin_time,
                    r.checkout_time,

                    r.num_guests,
                    r.special_requests,

                    r.total_price,
                    r.payment_status,
                    r.payment_method,
                    r.paid_at,

                    r.status,
                    r.created_at
                FROM rentals r
                JOIN users u  ON u.id  = r.user_id
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
        """Return rentals for a specific guest."""
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
                    rm.price          AS price_per_night,

                    r.checkin,
                    r.checkout,
                    r.checkin_time,
                    r.checkout_time,

                    r.num_guests,
                    r.special_requests,

                    r.total_price,
                    r.payment_status,
                    r.payment_method,
                    r.paid_at,

                    r.status,
                    r.created_at
                FROM rentals r
                JOIN users u  ON u.id  = r.user_id
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
    def get_unpaid_rentals():
        """Return all rentals with payment_status = 'unpaid' (counter collection)."""
        conn = get_db_connection()
        if conn is None:
            return []
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    r.id,
                    u.first_name,
                    u.last_name,
                    rm.room_number,
                    rm.room_type,
                    r.checkin,
                    r.checkout,
                    r.total_price,
                    r.payment_status,
                    r.status
                FROM rentals r
                JOIN users u  ON u.id  = r.user_id
                LEFT JOIN rooms rm ON rm.id = r.room_id
                WHERE r.payment_status = 'unpaid'
                ORDER BY r.checkin ASC
                """
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching unpaid rentals: {e}")
            return []
        finally:
            conn.close()





    @staticmethod
    def check_in(rental_id: int) -> bool:
        """Set rental status to active and set room Occupied."""
        from  models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cur = conn.cursor()
            cur.execute("SELECT room_id, status FROM rentals WHERE id = ?", (rental_id,))
            row = cur.fetchone()
            if not row:
                return False

            room_id = row["room_id"]
            current_status = str(row["status"] or "").lower()

            if current_status not in ["pending", "active"]:
                return False

            cur.execute("SELECT room_number, status FROM rooms WHERE id = ?", (room_id,))
            room_row = cur.fetchone()
            if not room_row:
                return False
            room_number = room_row["room_number"]

            room_status = str(room_row["status"] or "")
            if current_status == "pending" and room_status != "Available":
                return False

            cur.execute("UPDATE rentals SET status = 'active' WHERE id = ?", (rental_id,))
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
        from  models.RoomModel import RoomModel

        conn = get_db_connection()
        if conn is None:
            return False

        try:
            cur = conn.cursor()
            cur.execute("SELECT room_id, status FROM rentals WHERE id = ?", (rental_id,))
            row = cur.fetchone()
            if not row:
                return False

            room_id = row["room_id"]
            current_status = str(row["status"] or "").lower()

            if current_status not in ["active", "pending"]:
                return False


            cur.execute("SELECT room_number FROM rooms WHERE id = ?", (room_id,))
            room_row = cur.fetchone()
            if not room_row:
                return False
            room_number = room_row["room_number"]

            cur.execute(
                "UPDATE rentals SET status = 'completed' WHERE id = ?",
                (rental_id,),
            )
            conn.commit()

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
        from  models.RoomModel import RoomModel

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

            cur.execute(
                "UPDATE rentals SET status = 'cancelled' WHERE id = ?",
                (rental_id,),
            )
            conn.commit()

            if room_row["status"] == "Occupied":
                RoomModel.update_room_status(room_number, "Available")

            return True
        except sqlite3.Error as e:
            print(f"Error cancel rental: {e}")
            return False
        finally:
            conn.close()
