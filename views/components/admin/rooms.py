
import tkinter as tk
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RoomModel import RoomModel


def create_rooms(parent):
    # ── [DATA SETUP] ──────────────────────────────────────────
    # Kinukuha ang data mula sa RoomModel
    rooms_data = RoomModel.get_all_rooms()
    counts = RoomModel.get_room_counts()

    count_avail = counts["Available"]
    count_occ = counts["Occupied"]
    count_maint = counts["Maintenance"]

    # ── [MAIN CONTAINER] ──────────────────────────────────────
    rooms_container = tk.Frame(parent, bg="#f5f5f7")
    rooms_container.pack(fill=tk.BOTH, expand=True)

    # ── [TOP BAR / FILTERS] ───────────────────────────────────
    top_bar = tk.Frame(rooms_container, bg="#f5f5f7")
    top_bar.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(10, 0))

    btn_style = {"font": ("Segoe UI", 10), "bg": "#ffffff", "fg": "#1d1d1f", "relief": "flat",
                 "highlightbackground": "#e1e1e1", "highlightthickness": 1, "padx": 15, "pady": 8, "cursor": "hand2"}
    count_style = {"font": ("Segoe UI", 10, "bold"), "bg": "#f5f5f7", "fg": "#5f6368"}

    # ── [FILTER FUNCTIONS] ────────────────────────────────────
    # Ito ang mga functions na tinatawag ng mga buttons

    def clear_cards():
        """Tinatanggal lahat ng nakadisplay na cards sa screen."""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    def display_rooms(data_to_show):
        """Tagagawa ng mga cards base sa listahan na ibinigay."""
        clear_cards()
        if not data_to_show:
            tk.Label(scrollable_frame, text="No rooms found in this category.",
                     font=("Segoe UI", 11), bg="#f5f5f7", fg="#86868b").pack(pady=40)
            return

        for index, room in enumerate(data_to_show):
            add_room_card(index // 6, index % 6, room)

    def filter_all():
        display_rooms(rooms_data)

    def filter_available():
        filtered = [r for r in rooms_data if r["status"] == "Available"]
        display_rooms(filtered)

    def filter_occupied():
        filtered = [r for r in rooms_data if r["status"] == "Occupied"]
        display_rooms(filtered)

    def filter_maintenance():
        filtered = [r for r in rooms_data if r["status"] == "Maintenance"]
        display_rooms(filtered)

    # ── [FILTER BUTTONS UI] ──────────────────────────────────
    # Dito kinakabit ang mga functions sa mga pindutan

    tk.Button(top_bar, text="All Rooms", command=filter_all, **btn_style).pack(side=tk.LEFT, padx=5)

    avail_group = tk.Frame(top_bar, bg="#f5f5f7")
    avail_group.pack(side=tk.LEFT, padx=5)
    tk.Button(avail_group, text="Available", command=filter_available, **btn_style).pack(side=tk.LEFT)
    tk.Label(avail_group, text=str(count_avail), **count_style).pack(side=tk.LEFT, padx=5)

    occ_group = tk.Frame(top_bar, bg="#f5f5f7")
    occ_group.pack(side=tk.LEFT, padx=5)
    tk.Button(occ_group, text="Occupied", command=filter_occupied, **btn_style).pack(side=tk.LEFT)
    tk.Label(occ_group, text=str(count_occ), **count_style).pack(side=tk.LEFT, padx=5)

    maint_group = tk.Frame(top_bar, bg="#f5f5f7")
    maint_group.pack(side=tk.LEFT, padx=5)
    tk.Button(maint_group, text="Maintenance", command=filter_maintenance, **btn_style).pack(side=tk.LEFT)
    tk.Label(maint_group, text=str(count_maint), **count_style).pack(side=tk.LEFT, padx=5)

    # ── [SCROLLABLE AREA] ─────────────────────────────────────
    scroll_wrapper = tk.Frame(rooms_container, bg="#f5f5f7")
    scroll_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(scroll_wrapper, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", on_canvas_resize)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ── [HELPER FUNCTIONS] ────────────────────────────────────
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mousewheel(widget):
        widget.bind("<MouseWheel>", on_mousewheel)
        for child in widget.winfo_children():
            bind_mousewheel(child)

    def add_room_card(row, col, room_info):
        card = tk.Frame(scrollable_frame, bg="#ffffff", width=140, height=140,
                        highlightbackground="#e1e1e1", highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False)

        status_colors = {
            "Available": "#1a73e8",  # Blue
            "Occupied": "#d93025",  # Red
            "Maintenance": "#f9ab00"  # Yellow
        }
        color = status_colors.get(room_info["status"], "#5f6368")

        tk.Label(card, text=f"Room {room_info['room_number']}", font=("Segoe UI", 10, "bold"),
                 fg="#5f6368", bg="#ffffff").pack(pady=(20, 5))

        tk.Label(card, text=room_info["status"], font=("Segoe UI", 9),
                 fg=color, bg="#ffffff").pack()

        tk.Label(card, text=room_info["room_type"], font=("Segoe UI", 8),
                 fg="#86868b", bg="#ffffff").pack(side=tk.BOTTOM, pady=10)

        bind_mousewheel(card)

    # Initial Load (Ipakita lahat sa simula)
    filter_all()

    return rooms_container