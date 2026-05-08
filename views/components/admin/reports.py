import tkinter as tk
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RoomModel import RoomModel
from models.RentalModel import RentalModel
from models.user_model import UserModel


def create_reports(parent):
    main_container = tk.Frame(parent, bg="#f5f5f7")
    main_container.pack(fill="both", expand=True)

    header = tk.Frame(main_container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(
        header,
        text="Reports",
        font=("Segoe UI", 18, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
    ).pack(side="left")

    btn_refresh = tk.Button(
        header,
        text="↻ Refresh",
        font=("Segoe UI", 9),
        bg="#0071e3",
        fg="white",
        relief="flat",
        padx=15,
        cursor="hand2",
    )
    btn_refresh.pack(side="right", pady=10)

    content = tk.Frame(main_container, bg="#f5f5f7")
    content.pack(fill="both", expand=True, padx=40, pady=10)

    def render():
        for w in content.winfo_children():
            w.destroy()

        counts = RoomModel.get_room_counts()
        rentals = RentalModel.get_rentals_joined()

        total_guests = len(UserModel.get_all_guest())
        rental_counts = {"active": 0, "completed": 0, "cancelled": 0}
        for r in rentals:
            st = str(r.get("status") or "").lower()
            if st in rental_counts:
                rental_counts[st] += 1

        left = tk.Frame(content, bg="#f5f5f7")
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(content, bg="#f5f5f7")
        right.pack(side="right", fill="both", expand=False)

        def card(parent_frame, title, value):
            c = tk.Frame(parent_frame, bg="#ffffff", padx=20, pady=15, highlightthickness=1, highlightbackground="#e5e5e7")
            c.pack(fill="x", pady=8)
            tk.Label(c, text=title, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#86868b").pack(anchor="w")
            tk.Label(c, text=str(value), font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff").pack(anchor="w")

        tk.Label(left, text="Rooms", font=("Segoe UI", 12, "bold"), bg="#f5f5f7", fg="#1d1d1f").pack(anchor="w", pady=(0, 10))
        card(left, "Available", counts.get("Available", 0))
        card(left, "Occupied", counts.get("Occupied", 0))
        card(left, "Maintenance", counts.get("Maintenance", 0))

        tk.Label(right, text="Rental Status", font=("Segoe UI", 12, "bold"), bg="#f5f5f7", fg="#1d1d1f").pack(anchor="w", pady=(0, 10))
        card(right, "Active (Checked-in)", rental_counts.get("active", 0))
        card(right, "Completed (Checked-out)", rental_counts.get("completed", 0))
        card(right, "Cancelled", rental_counts.get("cancelled", 0))

        # bottom guest summary
        bottom = tk.Frame(content, bg="#f5f5f7")
        bottom.pack(fill="x", pady=(15, 0))
        tk.Label(bottom, text="Guests", font=("Segoe UI", 12, "bold"), bg="#f5f5f7", fg="#1d1d1f").pack(anchor="w", pady=(0, 10))

        guest_card = tk.Frame(bottom, bg="#ffffff", padx=20, pady=15, highlightthickness=1, highlightbackground="#e5e5e7")
        guest_card.pack(fill="x")
        tk.Label(guest_card, text="Total Registered Users", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#86868b").pack(anchor="w")
        tk.Label(guest_card, text=str(total_guests), font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff").pack(anchor="w")

    btn_refresh.config(command=render)
    render()
    return main_container

