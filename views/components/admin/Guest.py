import tkinter as tk
from tkinter import ttk

from  controllers.rental_controller import RentalController
from  controllers.user_controller import UserController


def create_guest(parent):
    main_container = tk.Frame(parent, bg="#f5f5f7")
    main_container.pack(fill="both", expand=True)


    header = tk.Frame(main_container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(
        header, text="Guest Management",
        font=("Segoe UI", 18, "bold"), bg="#f5f5f7", fg="#1d1d1f"
    ).pack(side="left")

    btn_refresh = tk.Button(
        header, text="⟳ Refresh", font=("Segoe UI", 9),
        bg="#0071e3", fg="white", relief="flat", padx=15,
        cursor="hand2"
    )
    btn_refresh.pack(side="right", pady=10)


    table_header = tk.Frame(main_container, bg="#f5f5f7")
    table_header.pack(fill="x", padx=60, pady=(0, 5))

    for i in range(6):
        table_header.columnconfigure(i, weight=1, uniform="col")

    column_titles = ["NO", "FIRST NAME", "LAST NAME", "EMAIL", "CONTACT", "STATUS"]
    for i, text in enumerate(column_titles):
        alignment = "w" if i < 5 else "e"
        tk.Label(table_header, text=text, font=("Segoe UI", 8, "bold"),
                 bg="#f5f5f7", fg="#86868b").grid(row=0, column=i, sticky=alignment)


    scroll_wrapper = tk.Frame(main_container, bg="#f5f5f7")
    scroll_wrapper.pack(fill="both", expand=True, padx=40)

    canvas = tk.Canvas(scroll_wrapper, bg="#f5f5f7", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_guests():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        guests = UserController.handle_list_guests()

        if not guests:
            tk.Label(scrollable_frame, text="No guests registered yet.",
                     font=("Segoe UI", 10, "italic"), bg="#f5f5f7", fg="#86868b").pack(pady=50)
            return


        all_rentals = RentalController.handle_list_all_bookings()
        active_user_ids = {
            r["user_id"] for r in all_rentals
            if str(r.get("status") or "").lower() == "active"
        }

        for guest in guests:
            g_id = guest.get("id")
            f_name = guest.get("first_name")
            l_name = guest.get("last_name")
            email = guest.get("email")
            phone = guest.get("phone")

            card = tk.Frame(scrollable_frame, bg="white", pady=12, padx=20,
                            highlightthickness=1, highlightbackground="#d2d2d7")
            card.pack(fill="x", pady=2)

            for i in range(6):
                card.columnconfigure(i, weight=1, uniform="col")

            tk.Label(card, text=f"#{g_id}", font=("Segoe UI", 8, "bold"),
                     bg="white", fg="#0071e3").grid(row=0, column=0, sticky="w")
            tk.Label(card, text=f_name, font=("Segoe UI", 9, "bold"),
                     bg="white", fg="#1d1d1f").grid(row=0, column=1, sticky="w")
            tk.Label(card, text=l_name, font=("Segoe UI", 9),
                     bg="white", fg="#1d1d1f").grid(row=0, column=2, sticky="w")
            tk.Label(card, text=email, font=("Segoe UI", 9),
                     bg="white", fg="#86868b").grid(row=0, column=3, sticky="w")
            tk.Label(card, text=phone if phone else "N/A", font=("Segoe UI", 9),
                     bg="white", fg="#1d1d1f").grid(row=0, column=4, sticky="w")


            if g_id in active_user_ids:
                bg_color, fg_color, label = "#e2f9e1", "#1db954", "ACTIVE"
            else:
                bg_color, fg_color, label = "#f2f2f7", "#86868b", "NO BOOKING"

            status_frame = tk.Frame(card, bg=bg_color, padx=10, pady=3)
            status_frame.grid(row=0, column=5, sticky="e")
            tk.Label(status_frame, text=label, font=("Segoe UI", 7, "bold"),
                     bg=bg_color, fg=fg_color).pack()

    btn_refresh.config(command=load_guests)
    load_guests()
    return main_container
