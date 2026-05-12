import tkinter as tk
from tkinter import messagebox
from models.RoomModel import RoomModel
from models.RentalModel import RentalModel


def create_booking_form(parent, user_id, on_booked=None, selected_room_number=None):
    # 1. Main Container (Match the background of the dashboard)
    frame = tk.Frame(parent, bg="white")  # Changed to white to blend with the 'card' container in dashboard
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # 2. Title Section
    title_frame = tk.Frame(frame, bg="white")
    title_frame.pack(fill="x", pady=(0, 20))

    tk.Label(
        title_frame, text="Confirm Booking",
        font=("SF Pro Display", 18, "bold"), bg="white", fg="#1d1d1f"
    ).pack(anchor="w")

    tk.Label(
        title_frame, text="Please verify the details below.",
        font=("SF Pro Text", 9), bg="white", fg="#86868b"
    ).pack(anchor="w")

    # 3. Form Variables
    room_var = tk.StringVar(value=selected_room_number if selected_room_number else "")

    # Defaulting to today and tomorrow for convenience
    from datetime import datetime, timedelta
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Two choices for check-in: "Now/Today" vs "Set day & time"
    checkin_choice_var = tk.StringVar(value="now")  # now | set

    checkin_var = tk.StringVar(value=today)
    checkout_var = tk.StringVar(value=tomorrow)
    checkin_time_var = tk.StringVar(value="14:00")
    checkout_time_var = tk.StringVar(value="12:00")



    # 4. Modern UI Fields Helper
    def create_styled_input(label_text, var, readonly=False):
        group = tk.Frame(frame, bg="white")
        group.pack(fill="x", pady=10)

        tk.Label(
            group, text=label_text.upper(),
            font=("SF Pro Text", 7, "bold"),
            bg="white", fg="#86868b"
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            group,
            textvariable=var,
            font=("SF Pro Text", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#0071e3",  # Blue focus color
            insertbackground="#0071e3"
        )

        if readonly:
            entry.configure(state="readonly", readonlybackground="#f5f5f7", fg="#1d1d1f")

        entry.pack(fill="x", ipady=12, padx=1)  # ipady makes it taller/Apple-like

    # Render Fields
    create_styled_input("Selected Room", room_var, readonly=True)

    # Check-in mode selection (Now/Today vs Set day & time)
    mode_group = tk.Frame(frame, bg="white")
    mode_group.pack(fill="x", pady=(10, 0))

    tk.Label(
        mode_group,
        text="CHECK-IN MODE".upper(),
        font=("SF Pro Text", 7, "bold"),
        bg="white",
        fg="#86868b",
    ).pack(anchor="w", pady=(0, 5))

    rb_now = tk.Radiobutton(
        mode_group,
        text="Now/Today",
        variable=checkin_choice_var,
        value="now",
        bg="white",
        activebackground="white",
        font=("SF Pro Text", 11),
        command=lambda: on_checkin_mode_change_safe(),
    )
    rb_set = tk.Radiobutton(

        mode_group,
        text="Set day & time",
        variable=checkin_choice_var,
        value="set",
        bg="white",
        activebackground="white",
        font=("SF Pro Text", 11),
        command=lambda: on_checkin_mode_change(),
    )
    rb_now.pack(anchor="w")
    rb_set.pack(anchor="w")

    # Helpers to toggle enabled/disabled state for date/time fields
    def set_widget_state(widget, enabled: bool):
        # Tkinter: disable by state="disabled", readonly by state="readonly".
        # For normal enabled input we can just use "normal".
        if enabled:
            widget.configure(state="normal")
        else:
            widget.configure(state="disabled")

    # Keep references to the specific entry widgets for toggling.
    # We create them in a controlled way below (instead of create_styled_input) to allow state updates.
    checkin_date_group = tk.Frame(frame, bg="white")
    checkin_date_group.pack(fill="x", pady=10)
    tk.Label(
        checkin_date_group,
        text="Check-in Date (YYYY-MM-DD)".upper(),
        font=("SF Pro Text", 7, "bold"),
        bg="white",
        fg="#86868b",
    ).pack(anchor="w", pady=(0, 5))
    checkin_date_entry = tk.Entry(
        checkin_date_group,
        textvariable=checkin_var,
        font=("SF Pro Text", 11),
        relief="flat",
        highlightthickness=1,
        highlightbackground="#d2d2d7",
        highlightcolor="#0071e3",
        insertbackground="#0071e3",
    )
    checkin_date_entry.pack(fill="x", ipady=12, padx=1)

    checkin_time_group = tk.Frame(frame, bg="white")
    checkin_time_group.pack(fill="x", pady=10)
    tk.Label(
        checkin_time_group,
        text="Check-in Time (HH:MM)".upper(),
        font=("SF Pro Text", 7, "bold"),
        bg="white",
        fg="#86868b",
    ).pack(anchor="w", pady=(0, 5))
    checkin_time_entry = tk.Entry(
        checkin_time_group,
        textvariable=checkin_time_var,
        font=("SF Pro Text", 11),
        relief="flat",
        highlightthickness=1,
        highlightbackground="#d2d2d7",
        highlightcolor="#0071e3",
        insertbackground="#0071e3",
    )
    checkin_time_entry.pack(fill="x", ipady=12, padx=1)

    # Check-out fields keep existing styled helper
    create_styled_input("Check-out Date (YYYY-MM-DD)", checkout_var)
    create_styled_input("Check-out Time (HH:MM)", checkout_time_var)

    def on_checkin_mode_change():
        mode = (checkin_choice_var.get() or "now").lower()
        if mode == "now":
            # Auto-fill BOTH date and time for "Now/Today".
            checkin_var.set(today)
            # Auto-fill time as current time + 1 minute (HH:MM) to reduce edge cases
            # where admin approval happens within the same minute.
            from datetime import datetime, timedelta
            checkin_time_var.set((datetime.now() + timedelta(minutes=1)).strftime("%H:%M"))


            # Disable editing for date and time (automatic).
            set_widget_state(checkin_date_entry, enabled=False)
            set_widget_state(checkin_time_entry, enabled=False)
        else:

            # Allow both date/time editing.
            set_widget_state(checkin_date_entry, enabled=True)
            set_widget_state(checkin_time_entry, enabled=True)

    def on_checkin_mode_change_safe():
        # If user toggles quickly, keep UI consistent.
        try:
            on_checkin_mode_change()
        except Exception:
            # fail silently; booking still works with stored StringVars
            pass

    # Apply initial mode state
    on_checkin_mode_change()

    # (Check-in fields are already rendered above; create_styled_input for them is removed.)



    # 5. Price Breakdown (Minimalist Touch)
    price_frame = tk.Frame(frame, bg="#f5f5f7", padx=15, pady=15)
    price_frame.pack(fill="x", pady=20)

    # Booking total is computed inside RentalModel using room price + number of nights.
    # Here we just show the user an estimated total after they selected dates.
    # Also show the optional “reservation/admin fee” if your workflow needs it.
    price_total_lbl = tk.Label(
        price_frame,
        text="TOTAL: ₱0.00",
        font=("SF Pro Text", 14, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
        anchor="w",
    )
    price_total_lbl.pack(fill="x")

    

    # recompute when user edits dates (simple heuristic)
    def update_price_preview(*_):
        try:
            room_number = room_var.get()
            if not room_number:
                return
            c_in = checkin_var.get().strip()
            c_out = checkout_var.get().strip()
            # RentalModel already calculates total_price; but it needs room_number + dates.
            # Use same helper by calling create_reservation? No—so compute locally:
            room_list = RoomModel.get_all_rooms()
            price_per_night = 0.0
            for rm in room_list:
                if str(rm.get("room_number")) == str(room_number):
                    price_per_night = float(rm.get("price", 0))
                    break
            from datetime import datetime
            d1 = datetime.strptime(c_in, "%Y-%m-%d")
            d2 = datetime.strptime(c_out, "%Y-%m-%d")
            nights = max((d2 - d1).days, 1)
            total = price_per_night * nights

            # Admin reservation extra price (if you want fixed fee). Keep 0 unless you set it.
            reservation_fee = 0.0
            total_with_fee = total + reservation_fee

            price_total_lbl.config(text=f"TOTAL: ₱{total_with_fee:,.2f}")

        except Exception:
            # keep UI stable if parsing fails
            pass

    # trace changes
    checkin_var.trace_add("write", update_price_preview)
    checkout_var.trace_add("write", update_price_preview)
    update_price_preview()

    # 6. Logic Function
    def handle_booking():

        room_num = room_var.get()
        c_in = checkin_var.get().strip()
        c_out = checkout_var.get().strip()

        if not room_num:
            messagebox.showwarning("System", "Please select a room first.")
            return

        # Create as ACTIVE so the selected room becomes Occupied immediately
        # and disappears from the Available rooms list.
        c_in_time = checkin_time_var.get().strip()
        c_out_time = checkout_time_var.get().strip()

        success = RentalModel.create_reservation(
            user_id=user_id,
            room_number=room_num,
            status="active",
            start_date=c_in,
            end_date=c_out,
            checkin_time=c_in_time,
            checkout_time=c_out_time,
            payment_status="paid",
        )

        if success:
            messagebox.showinfo("Success", "Booking Confirmed!")
            if on_booked:
                on_booked()
        else:
            messagebox.showerror("Error", "Could not complete booking. Please check the dates.")

    # Book Now button logic removed because we already set status="active" on confirmation
    # which marks the room as Occupied immediately.



    # 7a. Submit Button (Apple Blue)
    btn_confirm = tk.Button(
        frame, text="Confirm Reservation",
        bg="#0071e3", fg="white", font=("SF Pro Text", 11, "bold"),
        relief="flat", cursor="hand2", command=handle_booking,
        activebackground="#0077ed", activeforeground="white"
    )
    btn_confirm.pack(fill="x", ipady=12, pady=(10, 0))

    # NOTE: Remove the extra time-gated "Book Now" button.
    # Only keep "Confirm Reservation" as requested.

    return frame


