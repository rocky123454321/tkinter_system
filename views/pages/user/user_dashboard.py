import tkinter as tk
from pathlib import Path
import sys

# Path setup
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RentalModel import RentalModel
from views.components.user_sidebar import create_user_sidebar
from views.components.user.booking_form import create_booking_form
from views.components.topnav import create_topnav

# Global Style Constants
COLORS = {
    "bg": "#f5f5f7",  # Light gray background (Apple style)
    "card": "#ffffff",  # White for content cards
    "text_main": "#1d1d1f",
    "text_sub": "#86868b",
    "border": "#d2d2d7",
    "accent": "#0071e3",  # Apple blue
    "success": "#1db954"
}


def create_user_dashboard(parent, user_id: int, app=None):
    main_container = tk.Frame(parent, bg=COLORS["bg"])
    main_container.pack(fill="both", expand=True)

    # --- 1. SIDEBAR SETUP ---
    sidebar_host = tk.Frame(main_container, bg=COLORS["card"], width=260)
    sidebar_host.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_host.pack_propagate(False)  # Keep width fixed

    # --- 2. CONTENT WRAPPER ---
    content_wrapper = tk.Frame(main_container, bg=COLORS["bg"])
    content_wrapper.pack(side=tk.LEFT, fill="both", expand=True)

    def logout_callback():
        if app: app.show_login()

    # Topbar
    create_topnav(content_wrapper, logout_callback=logout_callback)

    # Dynamic Content Area
    content_area = tk.Frame(content_wrapper, bg=COLORS["bg"])
    content_area.pack(fill="both", expand=True, padx=40, pady=20)

    selected_room_number_holder = {"room": None}

    # --- RENDER FUNCTIONS ---

    def render_dashboard():
        """Table view with Apple-style card layout."""
        for w in content_area.winfo_children(): w.destroy()

        # Header Title
        title_lbl = tk.Label(
            content_area, text="Your Bookings",
            font=("SF Pro Display", 24, "bold"),
            bg=COLORS["bg"], fg=COLORS["text_main"], pady=10
        )
        title_lbl.pack(anchor="w")

        # The 'Card' container
        card_frame = tk.Frame(content_area, bg=COLORS["card"], highlightthickness=1,
                              highlightbackground=COLORS["border"])
        card_frame.pack(fill="both", expand=True, pady=10)

        # Table Header
        table_header = tk.Frame(card_frame, bg="#fafafa", pady=15)
        table_header.pack(fill="x")

        headers = ["ID", "ROOM", "TYPE", "CHECK-IN", "CHECK-OUT", "STATUS"]
        for i, h in enumerate(headers):
            lbl = tk.Label(table_header, text=h, font=("SF Pro Text", 8, "bold"), bg="#fafafa", fg=COLORS["text_sub"])
            lbl.grid(row=0, column=i, sticky="w", padx=20)
            table_header.grid_columnconfigure(i, weight=1)

        # Scrollable Area inside card
        canvas = tk.Canvas(card_frame, bg=COLORS["card"], highlightthickness=0)
        scrollbar = tk.Scrollbar(card_frame, orient="vertical", command=canvas.yview, width=12)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["card"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Sync width
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fetch Data
        rentals = RentalModel.get_rentals_joined_by_user(user_id)

        if not rentals:
            tk.Label(scrollable_frame, text="No bookings yet.", font=("SF Pro Text", 10),
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(pady=100)
            return

        for r in rentals:
            row = tk.Frame(scrollable_frame, bg=COLORS["card"], pady=15)
            row.pack(fill="x")

            status_val = str(r.get("status", "active")).upper()
            status_color = COLORS["success"] if status_val == "ACTIVE" else COLORS["accent"]
            if status_val not in ["ACTIVE", "COMPLETED"]: status_color = "#ff3b30"

            row_data = [
                f"#{r.get('id')}",
                r.get("room_number", "N/A"),
                r.get("room_type", "N/A"),
                r.get("checkin", "---"),
                r.get("checkout", "---"),
                status_val
            ]

            for i, text in enumerate(row_data):
                f_style = ("SF Pro Text", 10, "bold") if i == 5 else ("SF Pro Text", 10)
                fg_col = status_color if i == 5 else COLORS["text_main"]

                cell = tk.Label(row, text=text, font=f_style, bg=COLORS["card"], fg=fg_col)
                cell.grid(row=0, column=i, sticky="w", padx=20)
                row.grid_columnconfigure(i, weight=1)

            # Subtle Divider
            tk.Frame(scrollable_frame, bg=COLORS["bg"], height=1).pack(fill="x", padx=10)

    def render_rooms():
        """Split view: List on left, Form on right."""
        for w in content_area.winfo_children(): w.destroy()

        # Split Layout
        split_container = tk.Frame(content_area, bg=COLORS["bg"])
        split_container.pack(fill="both", expand=True)

        # Left Column (Rooms List)
        left_col = tk.Frame(split_container, bg=COLORS["bg"])
        left_col.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 20))

        # Right Column (Booking Form Card)
        right_col = tk.Frame(split_container, bg=COLORS["card"], width=380,
                             highlightthickness=1, highlightbackground=COLORS["border"])
        right_col.pack(side=tk.RIGHT, fill="y")
        right_col.pack_propagate(False)

        def render_form():
            for w in right_col.winfo_children(): w.destroy()

            # Header of form
            form_header = tk.Frame(right_col, bg=COLORS["card"], pady=20)
            form_header.pack(fill="x")

            if selected_room_number_holder["room"]:
                create_booking_form(
                    right_col, user_id=user_id,
                    on_booked=render_dashboard,
                    selected_room_number=selected_room_number_holder["room"]
                )
            else:
                tk.Label(right_col, text="Select a Room\nto start booking",
                         font=("SF Pro Display", 14), bg=COLORS["card"],
                         fg=COLORS["text_sub"], pady=100).pack()

        def on_room_clicked(rm):
            selected_room_number_holder["room"] = rm
            render_form()

        # Load list in left column
        from views.components.user.rooms_list import create_rooms_list
        create_rooms_list(left_col, on_book=on_room_clicked)
        render_form()

    # --- NAVIGATION LOGIC ---
    def on_nav(page_name: str):
        if page_name in ["Rooms", "Booking"]:
            render_rooms()
        else:
            render_dashboard()

    create_user_sidebar(sidebar_host, on_navigate=on_nav)
    render_dashboard()

    return main_container