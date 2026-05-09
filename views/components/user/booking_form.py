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
    create_styled_input("Check-in Date (YYYY-MM-DD)", checkin_var)
    create_styled_input("Check-in Time (HH:MM)", checkin_time_var)
    create_styled_input("Check-out Date (YYYY-MM-DD)", checkout_var)
    create_styled_input("Check-out Time (HH:MM)", checkout_time_var)

    # 5. Price Breakdown (Minimalist Touch)
    price_frame = tk.Frame(frame, bg="#f5f5f7", padx=15, pady=15)
    price_frame.pack(fill="x", pady=20)



    # 6. Logic Function
    def handle_booking():
        room_num = room_var.get()
        c_in = checkin_var.get().strip()
        c_out = checkout_var.get().strip()

        if not room_num:
            messagebox.showwarning("System", "Please select a room first.")
            return

        # Create as PENDING first; room will be occupied only when admin check-in happens.
        c_in_time = checkin_time_var.get().strip()
        c_out_time = checkout_time_var.get().strip()

        success = RentalModel.create_reservation(
            user_id=user_id,
            room_number=room_num,
            status="pending",
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

    # 7. Submit Button (Apple Blue)
    btn_confirm = tk.Button(
        frame, text="Confirm Reservation",
        bg="#0071e3", fg="white", font=("SF Pro Text", 11, "bold"),
        relief="flat", cursor="hand2", command=handle_booking,
        activebackground="#0077ed", activeforeground="white"
    )
    btn_confirm.pack(fill="x", ipady=12, pady=(10, 0))

    return frame