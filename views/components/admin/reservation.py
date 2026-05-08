import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RentalModel import RentalModel


def create_reservation(parent):
    # Main container matching the dashboard's background
    container = tk.Frame(parent, bg="#f5f5f7")
    container.pack(fill="both", expand=True, padx=30, pady=20)

    # --- HEADER SECTION ---
    header = tk.Frame(container, bg="#f5f5f7")
    header.pack(fill="x", pady=(0, 25))

    tk.Label(
        header, text="Reservation Overview",
        font=("SF Pro Display", 20, "bold"), bg="#f5f5f7", fg="#1d1d1f"
    ).pack(side="left")

    def on_refresh():
        render()

    tk.Button(
        header, text="Refresh Data", font=("SF Pro Text", 9, "bold"),
        bg="#ffffff", fg="#0071e3", relief="flat", padx=15, pady=8,
        cursor="hand2", command=on_refresh, highlightthickness=1,
        highlightbackground="#e1e1e1"
    ).pack(side="right")

    # --- DUAL PANEL WRAPPER ---
    panels_wrapper = tk.Frame(container, bg="#f5f5f7")
    panels_wrapper.pack(fill="both", expand=True)

    def create_panel(parent_frame, title):
        # Isa itong section (Left or Right)
        section = tk.Frame(parent_frame, bg="#f5f5f7")
        section.pack(side="left", fill="both", expand=True, padx=10)

        # Subtle Table Header Label
        tk.Label(
            section, text=title.upper(), font=("SF Pro Text", 9, "bold"),
            bg="#f5f5f7", fg="#86868b", pady=10
        ).pack(anchor="w")

        # White Card-like background for the list
        list_bg = tk.Frame(section, bg="#ffffff", highlightthickness=1, highlightbackground="#e1e1e1")
        list_bg.pack(fill="both", expand=True)

        # Scrollable Canvas
        canvas = tk.Canvas(list_bg, bg="#ffffff", highlightthickness=0)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Sync width ng bawat row sa canvas width
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        return scroll_frame

    # Create the two lists
    booking_list = create_panel(panels_wrapper, "Ongoing Bookings")
    reservation_list = create_panel(panels_wrapper, "Upcoming Reservations")

    def render():
        # Clear existing data
        for w in booking_list.winfo_children(): w.destroy()
        for w in reservation_list.winfo_children(): w.destroy()

        rentals = RentalModel.get_rentals_joined()
        today = datetime.now().strftime("%Y-%m-%d")

        if not rentals:
            for target in [booking_list, reservation_list]:
                tk.Label(target, text="No entries", font=("SF Pro Text", 9),
                         bg="#ffffff", fg="#b6b6bb", pady=20).pack()
            return

        for r in rentals:
            status = str(r.get("status")).lower()
            if status != "active": continue

            checkin_date = r.get("checkin", "")
            target = booking_list if checkin_date <= today else reservation_list

            # --- MINIMALIST ROW ---
            row = tk.Frame(target, bg="#ffffff", pady=12, padx=15)
            row.pack(fill="x")

            # Border line divider (Apple Style)
            tk.Frame(target, bg="#f5f5f7", height=1).pack(fill="x")

            # Guest Name & Room
            info_frame = tk.Frame(row, bg="#ffffff")
            info_frame.pack(side="left", fill="x", expand=True)

            tk.Label(info_frame, text=f"{r.get('first_name')} {r.get('last_name')}",
                     font=("SF Pro Text", 10, "bold"), bg="#ffffff", fg="#1d1d1f", anchor="w").pack(fill="x")
            tk.Label(info_frame, text=f"Room {r.get('room_number')} • {r.get('room_type')}",
                     font=("SF Pro Text", 8), bg="#ffffff", fg="#86868b", anchor="w").pack(fill="x")

            # Schedule/Dates
            date_frame = tk.Frame(row, bg="#ffffff")
            date_frame.pack(side="left", padx=20)

            tk.Label(date_frame, text=checkin_date, font=("SF Pro Text", 9),
                     bg="#ffffff", fg="#1d1d1f").pack(anchor="e")
            tk.Label(date_frame, text=f"to {r.get('checkout')}", font=("SF Pro Text", 8),
                     bg="#ffffff", fg="#86868b").pack(anchor="e")

            # Subtle Action Button
            def cancel_booking(rid=r.get('id')):
                if messagebox.askyesno("Cancel", "Cancel this reservation?"):
                    RentalModel.cancel_rental(rid)
                    render()

            btn_cancel = tk.Button(
                row, text="Cancel", font=("SF Pro Text", 8, "bold"),
                bg="#ffffff", fg="#ff3b30", relief="flat", cursor="hand2",
                activebackground="#fff5f5", command=cancel_booking
            )
            btn_cancel.pack(side="right", padx=(10, 0))

    render()
    return container