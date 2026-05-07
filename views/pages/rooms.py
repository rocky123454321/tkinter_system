import tkinter as tk


def create_rooms(parent):
    """
    Rooms page content only.

    NOTE:
    This must NOT create/destroy app-level layout. It should only build UI
    inside the provided parent frame.
    """
    rooms_container = tk.Frame(parent, bg="#f5f5f7")
    rooms_container.pack(fill=tk.BOTH, expand=True)

    # --- 1. TOP BAR (Navigation Buttons) ---
    top_bar = tk.Frame(rooms_container, bg="#f5f5f7")
    top_bar.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(10, 0))

    button_style = {
        "font": ("Segoe UI", 10),
        "bg": "#ffffff",
        "fg": "#1d1d1f",
        "relief": "flat",
        "cursor": "hand2",
        "highlightbackground": "#e1e1e1",
        "highlightthickness": 1,
        "padx": 15,
        "pady": 8,
    }

    tk.Button(top_bar, text="Available rooms", **button_style).pack(side=tk.LEFT, padx=5)
    tk.Button(top_bar, text="Occupied rooms", **button_style).pack(side=tk.LEFT, padx=5)
    tk.Button(top_bar, text="Maintenance rooms", **button_style).pack(side=tk.LEFT, padx=5)

    # --- 2. SCROLLABLE AREA SETUP ---
    canvas = tk.Canvas(rooms_container, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(rooms_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y")

    # --- 3. GENERATE 48 ROOM BOXES ---
    for i in range(48):
        room_num = i + 1

        room_box = tk.Frame(
            scrollable_frame,
            bg="#ffffff",
            width=140,
            height=140,
            highlightbackground="#e1e1e1",
            highlightthickness=1,
        )
        room_box.grid(row=i // 6, column=i % 6, padx=10, pady=10)
        room_box.pack_propagate(False)

        tk.Label(
            room_box,
            text=f"Room {room_num:03}",
            font=("Segoe UI", 10, "bold"),
            fg="#5f6368",
            bg="#ffffff",
        ).pack(pady=(20, 5))

        tk.Label(
            room_box,
            text="Available",
            font=("Segoe UI", 9),
            fg="#1a73e8",
            bg="#ffffff",
        ).pack()

        tk.Label(
            room_box,
            text="Standard",
            font=("Segoe UI", 8),
            fg="#86868b",
            bg="#ffffff",
        ).pack(side=tk.BOTTOM, pady=10)

    return rooms_container
