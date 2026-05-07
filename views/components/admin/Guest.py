import tkinter as tk
from tkinter import ttk
from models.user_model import UserModel


def create_guest(parent):
    # Main Canvas/Scrollbar setup para sa mahabang listahan
    main_container = tk.Frame(parent, bg="#f5f5f7")
    main_container.pack(fill="both", expand=True)

    # Header Section
    header = tk.Frame(main_container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(
        header, text="Guest Management",
        font=("Segoe UI", 18, "bold"), bg="#f5f5f7", fg="#1d1d1f"
    ).pack(side="left")

    # Table Header (Para may label ang columns)
    table_header = tk.Frame(main_container, bg="#f5f5f7")
    table_header.pack(fill="x", padx=40, pady=(10, 0))

    tk.Label(table_header, text="NAME", font=("Segoe UI", 9, "bold"), bg="#f5f5f7", fg="#86868b").pack(side="left")
    tk.Label(table_header, text="CONTACT", font=("Segoe UI", 9, "bold"), bg="#f5f5f7", fg="#86868b").pack(side="right")

    # Scrollable Area
    canvas = tk.Canvas(main_container, bg="#f5f5f7", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=parent.winfo_width() - 100)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=40)
    scrollbar.pack(side="right", fill="y")

    # --- Fetch Data ---
    guests = UserModel.get_all_guest()

    if not guests:
        tk.Label(
            scrollable_frame, text="No guests registered yet.",
            font=("Segoe UI", 10, "italic"), bg="#f5f5f7", fg="#86868b"
        ).pack(pady=50)
    else:
        for guest in guests:
            # Gumamit tayo ng index base sa SELECT query mo (id, first, last, email, phone)
            full_name = f"{guest[1]} {guest[2]}"
            phone_num = guest[4] if guest[4] else "N/A"

            # Guest Card/Row
            card = tk.Frame(scrollable_frame, bg="white", pady=15, padx=20, highlightthickness=1,
                            highlightbackground="#d2d2d7")
            card.pack(fill="x", pady=5)

            # Left side: Name and Email
            name_container = tk.Frame(card, bg="white")
            name_container.pack(side="left")

            tk.Label(name_container, text=full_name, font=("Segoe UI", 10, "bold"), bg="white", fg="#1d1d1f").pack(
                anchor="w")
            tk.Label(name_container, text=guest[3], font=("Segoe UI", 9), bg="white", fg="#86868b").pack(anchor="w")

            # Right side: Phone
            tk.Label(card, text=phone_num, font=("Segoe UI", 10), bg="white", fg="#1d1d1f").pack(side="right")

    return main_container