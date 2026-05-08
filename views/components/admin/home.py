import tkinter as tk
from pathlib import Path
import sys

# Setup Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RoomModel import RoomModel
from models.RentalModel import RentalModel  # Import para sa booking data


def create_home(root):
    # --- Data Fetching ---
    counts = RoomModel.get_room_counts()
    rooms_data = RoomModel.get_all_rooms()
    # Kunin ang real booking data
    recent_bookings = RentalModel.get_rentals_joined()

    count_avail = counts.get("Available", 0)
    count_occ = counts.get("Occupied", 0)
    count_maint = counts.get("Maintenance", 0)

    revenue = sum(int(room['price']) for room in rooms_data if room['status'] == 'Occupied')
    total_rooms = count_avail + count_maint + count_occ

    # Main Scrollable Container (Optional kung gusto mo ng scrolling dashboard)
    main_scroll = tk.Frame(root, bg="#f5f5f7")
    main_scroll.pack(fill="both", expand=True)

    # --- Top Stats Section ---
    top_frames = tk.Frame(main_scroll, pady=20, bg="#f5f5f7")
    top_frames.pack(fill="x", padx=10)

    def render_stats():
        header_style = {"bg": "#ffffff", "font": ("Helvetica", 10, "bold"), "fg": "#86868b"}
        value_style = {"bg": "#ffffff", "font": ("Helvetica", 20, "bold"), "fg": "#1d1d1f"}
        label_style = {"bg": "#ffffff", "font": ("Helvetica", 10), "fg": "#007aff"}

        def create_card(title, value, subtitle):
            f = tk.Frame(top_frames, bg="#ffffff", padx=20, pady=20, highlightthickness=1,
                         highlightbackground="#d2d2d7")
            f.pack(side="left", padx=10, expand=True, fill="both")
            tk.Label(f, text=title, **header_style).pack(anchor="w")
            tk.Label(f, text=value, **value_style).pack(anchor="w", pady=5)
            tk.Label(f, text=subtitle, **label_style).pack(anchor="w")

        create_card("TOTAL ROOMS", str(total_rooms), "All Floors")
        create_card("OCCUPANCY", f"{int((count_occ / total_rooms) * 100) if total_rooms > 0 else 0}%",
                    f"{count_occ} Rooms filled")
        create_card("REVENUE", f"₱{revenue:,.2f}", "Total from Occupied")
        create_card("AVAILABLE", str(count_avail), "Ready for Check-in")

    # --- Middle Section ---
    middle_container = tk.Frame(main_scroll, bg="#f5f5f7")
    middle_container.pack(fill="both", expand=True, padx=10, pady=10)

    def render_room_status(parent):
        Main_frame = tk.Frame(parent, bg="#ffffff", pady=20, padx=20, highlightthickness=1,
                              highlightbackground="#d2d2d7")
        Main_frame.pack(side="left", fill="both", expand=True, padx=10)

        header_row = tk.Frame(Main_frame, bg="#ffffff")
        header_row.pack(fill="x", pady=(0, 15))

        tk.Label(header_row, text="Room Status", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#1d1d1f").pack(
            side="left")

        # Room list scroll area
        canvas = tk.Canvas(Main_frame, bg="#ffffff", highlightthickness=0, height=300)
        scrollbar = tk.Scrollbar(Main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        preview_list = rooms_data[:15]  # Pakitang 15 rooms

        for room in preview_list:
            row = tk.Frame(scrollable_frame, bg="#ffffff", pady=10)
            row.pack(fill="x")

            status_color = "#34c759" if room['status'] == "Available" else "#ff3b30"
            if room['status'] == "Maintenance": status_color = "#ff9500"

            tk.Label(row, text=f"Room {room['room_number']}", font=("Helvetica", 10, "bold"), bg="#ffffff", width=12,
                     anchor="w").pack(side="left")
            tk.Label(row, text=room['room_type'], font=("Helvetica", 9), bg="#ffffff", fg="#86868b", width=15,
                     anchor="w").pack(side="left")
            tk.Label(row, text=room['status'].upper(), font=("Helvetica", 8, "bold"), fg=status_color, bg="#ffffff",
                     width=12, anchor="e").pack(side="right")

            tk.Frame(scrollable_frame, height=1, bg="#f5f5f7").pack(fill="x")

    def render_recent_bookings(parent):
        Main_frame = tk.Frame(parent, bg="#ffffff", pady=20, padx=20, highlightthickness=1,
                              highlightbackground="#d2d2d7")
        Main_frame.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(Main_frame, text="Booking Overview", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#1d1d1f").pack(
            anchor="w", pady=(0, 15))

        if not recent_bookings:
            tk.Label(Main_frame, text="No bookings recorded yet.", font=("Helvetica", 10), bg="#ffffff",
                     fg="#86868b").pack(pady=50)
            return

        # I-loop ang real data mula sa RentalModel
        for booking in recent_bookings[:8]:  # Show last 8 bookings
            row = tk.Frame(Main_frame, bg="#ffffff", pady=10)
            row.pack(fill="x")

            # Guest Name & Room
            guest_name = f"{booking.get('first_name', '')} {booking.get('last_name', '')}"
            room_info = f"Room {booking.get('room_number', 'N/A')}"

            info_frame = tk.Frame(row, bg="#ffffff")
            info_frame.pack(side="left")

            tk.Label(info_frame, text=guest_name, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#1d1d1f",
                     anchor="w").pack(fill="x")
            tk.Label(info_frame, text=room_info, font=("Helvetica", 9), bg="#ffffff", fg="#86868b", anchor="w").pack(
                fill="x")

            # Status Tag
            status = str(booking.get('status', 'active')).upper()
            status_bg = "#e8f5e9" if status == "ACTIVE" else "#f5f5f7"
            status_fg = "#2e7d32" if status == "ACTIVE" else "#1d1d1f"

            lbl_status = tk.Label(row, text=status, font=("Helvetica", 7, "bold"), bg=status_bg, fg=status_fg, padx=8,
                                  pady=2)
            lbl_status.pack(side="right")

            tk.Frame(Main_frame, height=1, bg="#f5f5f7").pack(fill="x")

    # --- Execute ---
    render_stats()
    render_room_status(middle_container)
    render_recent_bookings(middle_container)