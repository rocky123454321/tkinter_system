import tkinter as tk

from controllers.rental_controller import RentalController
from controllers.room_controller import RoomController


def create_home(root):
    from utils.ui_constants import (
        PAGE_TITLE_FONT, PAGE_TITLE_FG,
        COLORS, TITLE_PADY, LABEL_FONT, BODY_FONT,
    )

    counts         = RoomController.handle_room_counts()
    rooms_data     = RoomController.handle_list_rooms()[:15]
    recent_bookings = RentalController.handle_list_all_bookings()

    count_avail = counts.get("Available", 0)
    count_occ   = counts.get("Occupied", 0)
    count_maint = counts.get("Maintenance", 0)

    revenue     = sum(int(room['price']) for room in rooms_data if room['status'] == 'Occupied')
    total_rooms = count_avail + count_maint + count_occ

    main_scroll = tk.Frame(root, bg=COLORS["bg"])
    main_scroll.pack(fill="both", expand=True)

    # ── Stat cards ───────────────────────────────────────────────────────────
    top_frames = tk.Frame(main_scroll, bg=COLORS["bg"], pady=20)
    top_frames.pack(fill="x")

    def render_stats():
        header_style = {"bg": COLORS["card"], "font": LABEL_FONT,          "fg": COLORS["text_sub"]}
        value_style  = {"bg": COLORS["card"], "font": ("SF Pro Display", 20, "bold"), "fg": COLORS["text_main"]}
        label_style  = {"bg": COLORS["card"], "font": ("SF Pro Text", 10),  "fg": COLORS["accent"]}

        def create_card(title, value, subtitle):
            f = tk.Frame(top_frames, bg=COLORS["card"], padx=20, pady=20,
                         highlightthickness=1, highlightbackground=COLORS["border"])
            f.pack(side="left", padx=10, expand=True, fill="both")
            tk.Label(f, text=title, **header_style).pack(anchor="w")
            tk.Label(f, text=value, **value_style).pack(anchor="w", pady=5)
            tk.Label(f, text=subtitle, **label_style).pack(anchor="w")

        create_card("TOTAL ROOMS", str(total_rooms), "All Floors")
        create_card("OCCUPANCY",
                    f"{int((count_occ / total_rooms) * 100) if total_rooms > 0 else 0}%",
                    f"{count_occ} Rooms filled")
        create_card("REVENUE", f"₱{revenue:,.2f}", "Total from Occupied")
        create_card("AVAILABLE", str(count_avail), "Ready for Check-in")

    # ── Middle panels ────────────────────────────────────────────────────────
    middle_container = tk.Frame(main_scroll, bg=COLORS["bg"])
    middle_container.pack(fill="both", expand=True, pady=10)

    def render_room_status(parent):
        panel = tk.Frame(parent, bg=COLORS["card"], pady=20, padx=20,
                         highlightthickness=1, highlightbackground=COLORS["border"])
        panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(panel, text="Room Status", font=("SF Pro Display", 14, "bold"),
                 bg=COLORS["card"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 15))

        header_table = tk.Frame(panel, bg=COLORS["card"])
        header_table.pack(fill="x", padx=(0, 20))
        for i, (col, sticky) in enumerate([("ROOM", "w"), ("TYPE", "w"), ("STATUS", "e")]):
            header_table.grid_columnconfigure(i, weight=1)
            tk.Label(header_table, text=col, font=LABEL_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).grid(row=0, column=i, sticky=sticky)

        canvas = tk.Canvas(panel, bg=COLORS["card"], highlightthickness=0, height=350)
        scrollbar = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["card"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar.pack(side="right", fill="y")

        status_colors = {"AVAILABLE": COLORS["success"], "OCCUPIED": "#ff3b30", "MAINTENANCE": "#ff9500"}

        for room in rooms_data:
            row = tk.Frame(scrollable_frame, bg=COLORS["card"], pady=8)
            row.pack(fill="x")
            for i in range(3):
                row.grid_columnconfigure(i, weight=1)

            status_val   = room['status'].upper()
            status_color = status_colors.get(status_val, COLORS["text_sub"])

            tk.Label(row, text=f"Room {room['room_number']}", font=("SF Pro Text", 10, "bold"),
                     bg=COLORS["card"], fg=COLORS["text_main"]).grid(row=0, column=0, sticky="w")
            tk.Label(row, text=room['room_type'], font=BODY_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).grid(row=0, column=1, sticky="w")
            tk.Label(row, text=status_val, font=("SF Pro Text", 9, "bold"),
                     fg=status_color, bg=COLORS["card"]).grid(row=0, column=2, sticky="e")

    def render_recent_bookings(parent):
        panel = tk.Frame(parent, bg=COLORS["card"], pady=20, padx=20,
                         highlightthickness=1, highlightbackground=COLORS["border"])
        panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(panel, text="Booking Overview", font=("SF Pro Display", 14, "bold"),
                 bg=COLORS["card"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 15))

        if not recent_bookings:
            tk.Label(panel, text="No bookings recorded yet.", font=BODY_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(pady=50)
            return

        for booking in recent_bookings[:8]:
            row = tk.Frame(panel, bg=COLORS["card"], pady=10)
            row.pack(fill="x")

            guest_name = f"{booking.get('first_name', '')} {booking.get('last_name', '')}"
            room_info  = f"Room {booking.get('room_number', 'N/A')}"

            info_frame = tk.Frame(row, bg=COLORS["card"])
            info_frame.pack(side="left")

            tk.Label(info_frame, text=guest_name, font=("SF Pro Text", 10, "bold"),
                     bg=COLORS["card"], fg=COLORS["text_main"], anchor="w").pack(fill="x")
            tk.Label(info_frame, text=room_info, font=("SF Pro Text", 9),
                     bg=COLORS["card"], fg=COLORS["text_sub"], anchor="w").pack(fill="x")

            status    = str(booking.get('status', 'active')).upper()
            status_bg = "#e8f5e9" if status == "ACTIVE" else COLORS["bg"]
            status_fg = COLORS["success"] if status == "ACTIVE" else COLORS["text_main"]

            tk.Label(row, text=status, font=LABEL_FONT,
                     bg=status_bg, fg=status_fg, padx=8, pady=2).pack(side="right")

    render_stats()
    render_room_status(middle_container)
    render_recent_bookings(middle_container)