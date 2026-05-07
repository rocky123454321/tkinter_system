import tkinter as tk

def create_rooms(parent):
    rooms_container = tk.Frame(parent, bg="#f5f5f7")
    rooms_container.pack(fill=tk.BOTH, expand=True)

    # 1. SAMPLE DATA (Dito manggagaling ang bilang)
    # Sa totoong system, ito ay manggagaling sa Database mo.
    rooms_data = []
    for i in range(48):
        status = "Available"
        if i in [7, 9, 15]: status = "Occupied"
        if i in [4, 5]: status = "Maintenance"
        rooms_data.append({"number": i + 1, "status": status})

    # 2. CALCULATION (Bilangin kung ilan ang match sa status)
    count_avail = len([r for r in rooms_data if r["status"] == "Available"])
    count_occ = len([r for r in rooms_data if r["status"] == "Occupied"])
    count_maint = len([r for r in rooms_data if r["status"] == "Maintenance"])

    # --- TOP BAR ---
    top_bar = tk.Frame(rooms_container, bg="#f5f5f7")
    top_bar.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(10, 0))

    btn_style = {"font": ("Segoe UI", 10), "bg": "#ffffff", "fg": "#1d1d1f", "relief": "flat",
                 "highlightbackground": "#e1e1e1", "highlightthickness": 1, "padx": 15, "pady": 8}
    count_style = {"font": ("Segoe UI", 10, "bold"), "bg": "#f5f5f7", "fg": "#5f6368"}

    # Available
    avail_group = tk.Frame(top_bar, bg="#f5f5f7")
    avail_group.pack(side=tk.LEFT, padx=5)
    tk.Button(avail_group, text="Available rooms", **btn_style).pack(side=tk.LEFT)
    tk.Label(avail_group, text=str(count_avail), **count_style).pack(side=tk.LEFT, padx=5)

    # Occupied
    occ_group = tk.Frame(top_bar, bg="#f5f5f7")
    occ_group.pack(side=tk.LEFT, padx=5)
    tk.Button(occ_group, text="Occupied rooms", **btn_style).pack(side=tk.LEFT)
    tk.Label(occ_group, text=str(count_occ), **count_style).pack(side=tk.LEFT, padx=5)

    # Maintenance
    maint_group = tk.Frame(top_bar, bg="#f5f5f7")
    maint_group.pack(side=tk.LEFT, padx=5)
    tk.Button(maint_group, text="Maintenance rooms", **btn_style).pack(side=tk.LEFT)
    tk.Label(maint_group, text=str(count_maint), **count_style).pack(side=tk.LEFT, padx=5)

    # --- SCROLLABLE AREA ---
    canvas = tk.Canvas(rooms_container, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(rooms_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y")

    def add_room_card(row, col, room_info):
        card = tk.Frame(scrollable_frame, bg="#ffffff", width=140, height=140,
                        highlightbackground="#e1e1e1", highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False)

        status_colors = {"Available": "#1a73e8", "Occupied": "#d93025", "Maintenance": "#f9ab00"}
        color = status_colors.get(room_info["status"], "#5f6368")

        tk.Label(card, text=f"Room {room_info['number']:03}", font=("Segoe UI", 10, "bold"),
                 fg="#5f6368", bg="#ffffff").pack(pady=(20, 5))
        tk.Label(card, text=room_info["status"], font=("Segoe UI", 9),
                 fg=color, bg="#ffffff").pack()
        tk.Label(card, text="Standard", font=("Segoe UI", 8),
                 fg="#86868b", bg="#ffffff").pack(side=tk.BOTTOM, pady=10)

    # 3. GENERATE CARDS FROM DATA
    for index, room in enumerate(rooms_data):
        add_room_card(index // 6, index % 6, room)

    return rooms_container