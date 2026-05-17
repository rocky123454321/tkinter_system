import tkinter as tk
from tkinter import messagebox

from  controllers.rental_controller import RentalController


def create_checkin_checkout(parent):
    main_container = tk.Frame(parent, bg="#f5f5f7")
    main_container.pack(fill="both", expand=True)

    header = tk.Frame(main_container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)

    tk.Label(
        header,
        text="Check-in / Check-out",
        font=("Segoe UI", 18, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
    ).pack(side="left")

    btn_refresh = tk.Button(
        header,
        text="↻ Refresh",
        font=("Segoe UI", 9),
        bg="#0071e3",
        fg="white",
        relief="flat",
        padx=15,
        cursor="hand2",
    )
    btn_refresh.pack(side="right", pady=10)

    list_wrapper = tk.Frame(main_container, bg="#f5f5f7")
    list_wrapper.pack(fill="both", expand=True, padx=40, pady=10)

    canvas = tk.Canvas(list_wrapper, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(list_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width)
    )

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mousewheel(widget):
        widget.bind("<MouseWheel>", on_mousewheel)
        for child in widget.winfo_children():
            bind_mousewheel(child)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    bind_mousewheel(scrollable_frame)
    bind_mousewheel(canvas)


    def clear_rows():
        for w in scrollable_frame.winfo_children():
            w.destroy()

    def render():
        clear_rows()
        rentals = RentalController.handle_list_all_bookings()

        if not rentals:
            tk.Label(
                scrollable_frame,
                text="No rentals found.",
                font=("Segoe UI", 10, "italic"),
                bg="#f5f5f7",
                fg="#86868b",
            ).pack(pady=60)
            return

        for r in rentals:
            rental_id = r.get("id")
            status = str(r.get("status") or "")
            guest_name = f"{r.get('first_name','')} {r.get('last_name','')}".strip()
            room_number = r.get("room_number") or "N/A"
            room_type = r.get("room_type") or ""




            can_checkin = status.lower() == "pending"
            can_checkout = status.lower() == "active"

            if not (can_checkin or can_checkout):
                continue

            card = tk.Frame(
                scrollable_frame,
                bg="white",
                pady=12,
                padx=20,
                highlightthickness=1,
                highlightbackground="#d2d2d7",
            )
            card.pack(fill="x", pady=8)

            tk.Label(
                card,
                text=f"Booking #{rental_id}",
                font=("Segoe UI", 9, "bold"),
                fg="#0071e3",
                bg="white",
            ).grid(row=0, column=0, sticky="w")

            tk.Label(
                card,
                text=guest_name,
                font=("Segoe UI", 10, "bold"),
                fg="#1d1d1f",
                bg="white",
            ).grid(row=1, column=0, sticky="w")

            tk.Label(
                card,
                text=f"{room_number} • {room_type}",
                font=("Segoe UI", 9),
                fg="#86868b",
                bg="white",
            ).grid(row=0, column=1, rowspan=2, sticky="w", padx=(25, 0))

            status_fg = "#1db954" if can_checkout else "#f5a623"
            tk.Label(
                card,
                text=status.upper(),
                font=("Segoe UI", 8, "bold"),
                fg=status_fg,
                bg="white",
            ).grid(row=0, column=2, sticky="e", padx=(10, 0))

            actions = tk.Frame(card, bg="white")
            actions.grid(row=1, column=2, sticky="e", padx=(10, 0))

            if can_checkin:
                def do_checkin(rid=rental_id):
                    ok = RentalController.handle_check_in(rental_id=int(rid))
                    if not ok:
                        messagebox.showerror("Error", "Failed to check-in.")
                    render()

                tk.Button(
                    actions,
                    text="Check-in",
                    bg="#f9ab00",
                    fg="black",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    cursor="hand2",
                    padx=12,
                    pady=6,
                    command=do_checkin,
                ).pack(side="top", anchor="e", pady=(0, 6))

            if can_checkout:
                def do_checkout(rid=rental_id):
                    ok = RentalController.handle_check_out(rental_id=int(rid))
                    if not ok:
                        messagebox.showerror("Error", "Failed to check-out.")
                    render()

                tk.Button(
                    actions,
                    text="Check-out",
                    bg="#0071e3",
                    fg="white",
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    cursor="hand2",
                    padx=12,
                    pady=6,
                    command=do_checkout,
                ).pack(side="top", anchor="e")

        if not any(
            (str(r.get("status") or "").lower() == "completed") or (str(r.get("status") or "").lower() == "active")
            for r in rentals
        ):
            tk.Label(
                scrollable_frame,
                text="No pending check-in / check-out actions.",
                font=("Segoe UI", 10, "italic"),
                bg="#f5f5f7",
                fg="#86868b",
            ).pack(pady=60)

    btn_refresh.config(command=render)
    render()

    return main_container

