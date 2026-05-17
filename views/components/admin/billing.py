import tkinter as tk

from  controllers.rental_controller import RentalController
from  controllers.room_controller import RoomController


def create_billing(parent):
    main_container = tk.Frame(parent, bg="#f5f5f7")
    main_container.pack(fill="both", expand=True)

    header = tk.Frame(main_container, bg="#f5f5f7", pady=20)
    header.pack(fill="x", padx=40)
    tk.Label(
        header,
        text="Billing",
        font=("Segoe UI", 18, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
    ).pack(side="left")

    btn_refresh = tk.Button(
        header,
        text="Refresh",
        font=("Segoe UI", 9),
        bg="#0071e3",
        fg="white",
        relief="flat",
        padx=15,
        cursor="hand2",
    )
    btn_refresh.pack(side="right", pady=10)

    summary = tk.Frame(main_container, bg="#f5f5f7")
    summary.pack(fill="x", padx=40, pady=(5, 15))

    card_total = tk.Frame(
        summary,
        bg="#ffffff",
        padx=20,
        pady=15,
        highlightthickness=1,
        highlightbackground="#e5e5e7",
    )
    card_total.pack(side="left", padx=10, fill="y")
    tk.Label(
        card_total,
        text="TOTAL COMPLETED",
        font=("Helvetica", 10, "bold"),
        bg="#ffffff",
        fg="#86868b",
    ).pack(anchor="w")
    v_total = tk.Label(card_total, text="-", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff")
    v_total.pack(anchor="w")

    card_revenue = tk.Frame(
        summary,
        bg="#ffffff",
        padx=20,
        pady=15,
        highlightthickness=1,
        highlightbackground="#e5e5e7",
    )
    card_revenue.pack(side="left", padx=10, fill="y")
    tk.Label(
        card_revenue,
        text="ESTIMATED REVENUE",
        font=("Helvetica", 10, "bold"),
        bg="#ffffff",
        fg="#86868b",
    ).pack(anchor="w")
    v_revenue = tk.Label(card_revenue, text="-", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff")
    v_revenue.pack(anchor="w")

    list_wrapper = tk.Frame(main_container, bg="#f5f5f7")
    list_wrapper.pack(fill="both", expand=True, padx=40, pady=10)

    canvas = tk.Canvas(list_wrapper, bg="#f5f5f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(list_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f7")

    scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))

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
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    def price_map_by_room_number():
        rooms = RoomController.handle_list_rooms()
        return {str(room.get("room_number")): room.get("price") for room in rooms}

    def render():
        clear_rows()
        rentals = RentalController.handle_list_all_bookings()
        price_map = price_map_by_room_number()
        completed = [rental for rental in rentals if str(rental.get("status") or "").lower() == "completed"]

        revenue = 0.0
        for rental in completed:
            room_number = str(rental.get("room_number") or "")
            price = price_map.get(room_number)
            try:
                revenue += float(price) if price is not None else 0.0
            except (TypeError, ValueError):
                pass

        v_total.config(text=str(len(completed)))
        v_revenue.config(text=f"PHP {revenue:,.2f}")

        if not completed:
            tk.Label(
                scrollable_frame,
                text="No completed bookings yet.",
                font=("Segoe UI", 10, "italic"),
                bg="#f5f5f7",
                fg="#86868b",
            ).pack(pady=60)
            return

        for rental in completed[:200]:
            invoice_id = rental.get("id")
            guest_name = f"{rental.get('first_name', '')} {rental.get('last_name', '')}".strip()
            room_number = rental.get("room_number")
            room_type = rental.get("room_type") or ""
            created_at = rental.get("created_at") or ""
            price = float(price_map.get(str(room_number), 0) or 0)

            row = tk.Frame(
                scrollable_frame,
                bg="white",
                pady=12,
                padx=20,
                highlightthickness=1,
                highlightbackground="#d2d2d7",
            )
            row.pack(fill="x", pady=8)

            tk.Label(
                row,
                text=f"Invoice #{invoice_id}",
                font=("Segoe UI", 9, "bold"),
                bg="white",
                fg="#0071e3",
            ).grid(row=0, column=0, sticky="w")
            tk.Label(
                row,
                text=guest_name,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#1d1d1f",
            ).grid(row=1, column=0, sticky="w")
            tk.Label(
                row,
                text=f"{room_number} | {room_type}",
                font=("Segoe UI", 9),
                bg="white",
                fg="#86868b",
            ).grid(row=0, column=1, rowspan=2, sticky="w", padx=(25, 0))
            tk.Label(
                row,
                text=f"PHP {price:,.2f}",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="#0071e3",
            ).grid(row=0, column=2, sticky="e", padx=(10, 0))

            if created_at:
                tk.Label(
                    row,
                    text=str(created_at),
                    font=("Segoe UI", 8),
                    bg="white",
                    fg="#86868b",
                ).grid(row=1, column=2, sticky="e", padx=(10, 0))

    btn_refresh.config(command=render)
    render()

    return main_container
