import tkinter as tk
from datetime import datetime

from controllers.rental_controller import RentalController
from views.components.topnav import create_topnav
from views.components.user.booking_form import create_booking_form
from views.components.user_sidebar import create_user_sidebar


COLORS = {
    "bg": "#f5f5f7",
    "card": "#ffffff",
    "text_main": "#1d1d1f",
    "text_sub": "#86868b",
    "border": "#d2d2d7",
    "accent": "#0071e3",
    "success": "#1db954",
}

HEADERS = ["ID", "ROOM", "TYPE", "CHECK-IN", "CHECK-OUT", "STATUS"]
COL_WEIGHTS = [1, 1, 2, 2, 2, 1]


def create_user_dashboard(parent, user_id: int, app=None):
    main_container = tk.Frame(parent, bg=COLORS["bg"])
    main_container.pack(fill="both", expand=True)

    sidebar_host = tk.Frame(main_container, bg=COLORS["card"], width=260)
    sidebar_host.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_host.pack_propagate(False)

    content_wrapper = tk.Frame(main_container, bg=COLORS["bg"])
    content_wrapper.pack(side=tk.LEFT, fill="both", expand=True)

    def logout_callback():
        if app:
            app.show_login()

    create_topnav(content_wrapper, logout_callback=logout_callback)

    content_area = tk.Frame(content_wrapper, bg=COLORS["bg"])
    content_area.pack(fill="both", expand=True, padx=40, pady=20)

    selected_room_number_holder = {"room": None}

    def render_dashboard():
        for widget in content_area.winfo_children():
            widget.destroy()

        from utils.ui_constants import PAGE_TITLE_FONT, PAGE_TITLE_FG

        tk.Label(
            content_area,
            text="Your Bookings",
            font=PAGE_TITLE_FONT,
            bg=COLORS["bg"],
            fg=PAGE_TITLE_FG,
            pady=10,
            anchor="w",
        ).pack(anchor="w")

        card_frame = tk.Frame(
            content_area,
            bg=COLORS["card"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        card_frame.pack(fill="both", expand=True, pady=10)

        canvas = tk.Canvas(card_frame, bg=COLORS["card"], highlightthickness=0)
        scrollbar = tk.Scrollbar(card_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["card"])
        scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        grid_frame = tk.Frame(scrollable_frame, bg=COLORS["card"])
        grid_frame.pack(fill="both", expand=True)

        for col, weight in enumerate(COL_WEIGHTS):
            grid_frame.grid_columnconfigure(col, weight=weight)

        for col, header in enumerate(HEADERS):
            tk.Label(
                grid_frame,
                text=header,
                font=("SF Pro Text", 9, "bold"),
                bg="#fafafa",
                fg=COLORS["text_sub"],
                anchor="w",
                pady=12,
            ).grid(row=0, column=col, sticky="ew", padx=(20, 0))

        tk.Frame(grid_frame, bg=COLORS["border"], height=1).grid(
            row=1, column=0, columnspan=len(HEADERS), sticky="ew"
        )

        rentals = RentalController.handle_list_user_bookings(user_id=user_id)
        if not rentals:
            tk.Label(
                grid_frame,
                text="No bookings yet.",
                font=("SF Pro Text", 12),
                bg=COLORS["card"],
                fg=COLORS["text_sub"],
            ).grid(row=2, column=0, columnspan=len(HEADERS), pady=100)
            return

        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        for i, rental in enumerate(rentals):
            grid_row = (i + 1) * 2

            status_val = str(rental.get("status", "active")).upper()
            status_color = COLORS["success"] if status_val == "ACTIVE" else COLORS["accent"]

            row_data = [
                f"#{rental.get('id')}",
                rental.get("room_number"),
                rental.get("room_type"),
                rental.get("checkin"),
                rental.get("checkout"),
                status_val,
            ]

            for col, value in enumerate(row_data):
                tk.Label(
                    grid_frame,
                    text=value,
                    font=("SF Pro Text", 10),
                    bg=COLORS["card"],
                    fg=status_color if col == 5 else COLORS["text_main"],
                    anchor="w",
                    pady=14,
                ).grid(row=grid_row, column=col, sticky="ew", padx=(20, 0))

            try:
                rental_status = str(rental.get("status") or "").lower()
                payment_status = str(rental.get("payment_status") or "").lower()
                checkin_date = str(rental.get("checkin") or "")
                checkin_time = str(rental.get("checkin_time") or "14:00")
                can_show_book_now = (
                    rental_status == "pending"
                    and payment_status == "paid"
                    and checkin_date == today
                )

                if can_show_book_now:
                    checkin_dt = datetime.strptime(f"{today} {checkin_time}", "%Y-%m-%d %H:%M")
                    if now >= checkin_dt:
                        tk.Button(
                            grid_frame,
                            text="Book Now",
                            bg=COLORS["accent"],
                            fg="white",
                            relief="flat",
                            cursor="hand2",
                            activebackground="#0077ed",
                            font=("SF Pro Text", 9, "bold"),
                            command=lambda rental_id=rental.get("id"): (
                                RentalController.handle_approve_booking(rental_id=int(rental_id)),
                                render_dashboard(),
                            ),
                        ).grid(row=grid_row, column=len(HEADERS), sticky="e", padx=20)
            except (TypeError, ValueError):
                pass

            tk.Frame(grid_frame, bg=COLORS["bg"], height=1).grid(
                row=grid_row + 1, column=0, columnspan=len(HEADERS), sticky="ew", padx=10
            )

    def render_rooms():
        for widget in content_wrapper.winfo_children():
            if getattr(widget, "_is_banner", False):
                widget.destroy()

        for widget in content_area.winfo_children():
            widget.destroy()

        split_container = tk.Frame(content_area, bg=COLORS["bg"])
        split_container.pack(fill="both", expand=True)

        left_col = tk.Frame(split_container, bg=COLORS["bg"])
        left_col.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 20))

        right_col = tk.Frame(
            split_container,
            bg=COLORS["card"],
            width=380,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        right_col.pack(side=tk.RIGHT, fill="y")
        right_col.pack_propagate(False)

        def render_form():
            for widget in right_col.winfo_children():
                widget.destroy()

            if selected_room_number_holder["room"]:
                def on_booked_after_confirm():
                    selected_room_number_holder["room"] = None
                    render_dashboard()

                create_booking_form(
                    right_col,
                    user_id=user_id,
                    on_booked=on_booked_after_confirm,
                    selected_room_number=selected_room_number_holder["room"],
                )
                return

            tk.Label(
                right_col,
                text="Select a Room\nto start booking",
                font=("SF Pro Display", 14),
                bg=COLORS["card"],
                fg=COLORS["text_sub"],
                pady=100,
            ).pack()

        def on_room_clicked(room_number):
            selected_room_number_holder["room"] = room_number
            render_form()

        from views.components.user.rooms_list import create_rooms_list

        create_rooms_list(left_col, on_book=on_room_clicked)
        render_form()

    def render_map():
        for widget in content_area.winfo_children():
            widget.destroy()
        from views.pages.user.user_map import create_user_map

        create_user_map(content_area, on_back=render_dashboard)

    def render_settings():
        for widget in content_area.winfo_children():
            widget.destroy()
        from views.components.user.settings import create_user_settings

        create_user_settings(content_area, user_id=user_id, app=app)

    def on_nav(page_name: str):
        if page_name in ["Rooms", "Booking"]:
            render_rooms()
        elif page_name == "Map":
            render_map()
        elif page_name == "Settings":
            render_settings()
        else:
            render_dashboard()

    create_user_sidebar(sidebar_host, on_navigate=on_nav)
    render_dashboard()
    return main_container