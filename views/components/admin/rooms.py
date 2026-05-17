import tkinter as tk

from controllers.room_controller import RoomController


def create_rooms(parent):
    from utils.ui_constants import (
        PAGE_TITLE_FONT, PAGE_TITLE_FG,
        COLORS, TITLE_PADY, LABEL_FONT, BODY_FONT,
    )

    rooms_data = RoomController.handle_list_rooms()
    counts     = RoomController.handle_room_counts()

    count_avail = counts["Available"]
    count_occ   = counts["Occupied"]
    count_maint = counts["Maintenance"]

    rooms_container = tk.Frame(parent, bg=COLORS["bg"])
    rooms_container.pack(fill=tk.BOTH, expand=True)

    # ── Title ────────────────────────────────────────────────────────────────
    title_frame = tk.Frame(rooms_container, bg=COLORS["bg"])
    title_frame.pack(fill="x", pady=TITLE_PADY)

    tk.Label(
        title_frame,
        text="Rooms",
        font=PAGE_TITLE_FONT,
        bg=COLORS["bg"],
        fg=PAGE_TITLE_FG,
        anchor="w",
    ).pack(side="left")

    tk.Frame(rooms_container, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 10))

    # ── Filter buttons ───────────────────────────────────────────────────────
    top_bar = tk.Frame(rooms_container, bg=COLORS["bg"])
    top_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

    btn_style = {
        "font": ("SF Pro Text", 10),
        "bg": COLORS["card"],
        "fg": COLORS["text_main"],
        "relief": "flat",
        "highlightbackground": COLORS["border"],
        "highlightthickness": 1,
        "padx": 15,
        "pady": 8,
        "cursor": "hand2",
    }

    status_colors = {
        "Available":   "#1db954",
        "Occupied":    "#ff3b30",
        "Maintenance": "#ff9500",
    }

    def clear_cards():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    def display_rooms(data_to_show):
        clear_cards()
        if not data_to_show:
            tk.Label(scrollable_frame, text="No rooms found in this category.",
                     font=BODY_FONT, bg=COLORS["bg"], fg=COLORS["text_sub"]).pack(pady=40)
            return
        for index, room in enumerate(data_to_show):
            add_room_card(index // 9, index % 9, room)

    def filter_all():        display_rooms(rooms_data)
    def filter_available():  display_rooms([r for r in rooms_data if r["status"] == "Available"])
    def filter_occupied():   display_rooms([r for r in rooms_data if r["status"] == "Occupied"])
    def filter_maintenance(): display_rooms([r for r in rooms_data if r["status"] == "Maintenance"])

    tk.Button(top_bar, text="All Rooms",               command=filter_all,         **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(top_bar, text=f"Available {count_avail}", command=filter_available,  **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(top_bar, text=f"Occupied {count_occ}",    command=filter_occupied,   **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(top_bar, text=f"Maintenance {count_maint}", command=filter_maintenance, **btn_style).pack(side=tk.LEFT, padx=5)

    # ── Scrollable grid ──────────────────────────────────────────────────────
    scroll_wrapper = tk.Frame(rooms_container, bg=COLORS["bg"])
    scroll_wrapper.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(scroll_wrapper, bg=COLORS["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mousewheel(widget):
        widget.bind("<MouseWheel>", on_mousewheel)
        for child in widget.winfo_children():
            bind_mousewheel(child)

    def add_room_card(row, col, room_info):
        card = tk.Frame(
            scrollable_frame, bg=COLORS["card"], width=140, height=140,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False)

        color = status_colors.get(room_info["status"], COLORS["text_sub"])

        tk.Label(card, text=f"Room {room_info['room_number']}", font=("SF Pro Text", 10, "bold"),
                 fg=COLORS["text_sub"], bg=COLORS["card"]).pack(pady=(20, 5))
        tk.Label(card, text=room_info["status"], font=("SF Pro Text", 9),
                 fg=color, bg=COLORS["card"]).pack()
        tk.Label(card, text=room_info["room_type"], font=("SF Pro Text", 8),
                 fg=COLORS["text_sub"], bg=COLORS["card"]).pack(side=tk.BOTTOM, pady=10)

        bind_mousewheel(card)

    filter_all()
    return rooms_container