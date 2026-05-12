import tkinter as tk
from models.RoomModel import RoomModel


def create_rooms_list(parent, on_book=None):
    # Fallback if on_book is not provided
    on_book_func = on_book if on_book else lambda rm: print(f"Booking {rm}")

    # 1. Get ONLY Available Rooms
    all_rooms = RoomModel.get_all_rooms()
    available_rooms = [r for r in all_rooms if r.get("status") == "Available"]



    # 2. Main Container
    container = tk.Frame(parent, bg="#f5f5f7")
    container.pack(fill="both", expand=True)

    # 3. Simple Header
    header = tk.Frame(container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(
        header, text="Available Rooms",
        font=("Segoe UI", 18, "bold"), bg="#f5f5f7", fg="#1d1d1f"
    ).pack(side="left")

    # 4. Scrollable Area
    canvas = tk.Canvas(container, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    canvas.pack(side="left", fill="both", expand=True, padx=30)
    scrollbar.pack(side="right", fill="y")

    # 5. Room Card Builder
    def create_card(room_info, index):
        room_num = room_info.get("room_number")

        # Card Box
        card = tk.Frame(
            scrollable_frame, bg="white", highlightthickness=1,
            highlightbackground="#d2d2d7", padx=15, pady=15, cursor="hand2"
        )
        card.grid(row=index // 4, column=index % 4, padx=15, pady=15, sticky="nsew")

        # Room Info inside card
        tk.Label(card, text=f"Room {room_num}", font=("Segoe UI", 12, "bold"), bg="white", fg="#1d1d1f").pack()
        tk.Label(card, text=room_info.get("room_type"), font=("Segoe UI", 9), bg="white", fg="#86868b").pack(pady=5)
        tk.Label(card, text="● Available", font=("Segoe UI", 9, "bold"), bg="white", fg="#1db954").pack(side="bottom",
                                                                                                        pady=5)

        # Click Event
        def click_event(e): on_book_func(str(room_num))

        card.bind("<Button-1>", click_event)
        for child in card.winfo_children():
            child.bind("<Button-1>", click_event)

    # 6. Display Cards
    if not available_rooms:
        tk.Label(scrollable_frame, text="No rooms available.", font=("Segoe UI", 11), bg="#f5f5f7").pack(pady=50)
    else:
        for i, room in enumerate(available_rooms):
            create_card(room, i)

    return container