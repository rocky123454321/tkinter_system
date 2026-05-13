


import sqlite3

from  database.database_config import get_db_connection


class RoomModel:

    @staticmethod
    def create_room_table():

        conn = get_db_connection()
        if conn is None:
            return
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_number TEXT    NOT NULL UNIQUE,
                    room_type   TEXT    NOT NULL,
                    floor       INTEGER NOT NULL,
                    price       REAL    NOT NULL,
                    status      TEXT    DEFAULT 'Available'
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating rooms table: {e}")
        finally:
            conn.close()

    @staticmethod
    def seed_rooms():


        conn = get_db_connection()
        if conn is None:
            return
        try:
            cursor = conn.cursor()


            cursor.execute("SELECT COUNT(*) FROM rooms")
            count = cursor.fetchone()[0]
            if count > 0:
                return

            rooms = []
            for i in range(1, 49):
                floor       = (i - 1) // 6 + 1
                room_number = f"{floor}0{i % 6 if i % 6 != 0 else 6}"


                if floor <= 2:
                    room_type = "Standard Single"
                    price     = 2500.0
                elif floor <= 4:
                    room_type = "Deluxe Double"
                    price     = 4200.0
                elif floor <= 6:
                    room_type = "Suite"
                    price     = 8500.0
                else:
                    room_type = "Presidential Suite"
                    price     = 15000.0


                if i in [7, 9, 15, 20, 25]:
                    status = "Occupied"
                elif i in [4, 5]:
                    status = "Maintenance"
                else:
                    status = "Available"

                rooms.append((room_number, room_type, floor, price, status))

            conn.executemany("""
                INSERT OR IGNORE INTO rooms (room_number, room_type, floor, price, status)
                VALUES (?, ?, ?, ?, ?)
            """, rooms)
            conn.commit()
            print("Rooms seeded successfully.")
        except sqlite3.Error as e:
            print(f"Error seeding rooms: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_all_rooms():

        conn = get_db_connection()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms ORDER BY floor, room_number")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching rooms: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_available_rooms():

        conn = get_db_connection()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM rooms
                WHERE status = 'Available'
                ORDER BY floor, room_number
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching available rooms: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update_room_status(room_number, new_status):


        conn = get_db_connection()
        if conn is None:
            return False
        try:
            conn.execute("""
                UPDATE rooms SET status = ? WHERE room_number = ?
            """, (new_status, room_number))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating room status: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_room_counts():


        conn = get_db_connection()
        if conn is None:
            return {"Available": 0, "Occupied": 0, "Maintenance": 0}
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM rooms
                GROUP BY status
            """)
            rows = cursor.fetchall()
            counts = {"Available": 0, "Occupied": 0, "Maintenance": 0}
            for row in rows:
                counts[row["status"]] = row["count"]
            return counts
        except sqlite3.Error as e:
            print(f"Error fetching room counts: {e}")
            return {"Available": 0, "Occupied": 0, "Maintenance": 0}
        finally:
            conn.close()
