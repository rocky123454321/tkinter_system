import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

from  controllers.rental_controller import RentalController
from  controllers.room_controller import RoomController


def create_booking_form(parent, user_id, on_booked=None, selected_room_number=None):
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    title_frame = tk.Frame(frame, bg="white")
    title_frame.pack(fill="x", pady=(0, 20))
    from utils.ui_constants import PAGE_TITLE_FONT, PAGE_TITLE_FG

    tk.Label(
        title_frame,
        text="Confirm Booking",
        font=PAGE_TITLE_FONT,
        bg="white",
        fg=PAGE_TITLE_FG,
        anchor="w",
    ).pack(anchor="w")
    tk.Label(
        title_frame,
        text="Please verify the details below.",
        font=("SF Pro Text", 9),
        bg="white",
        fg="#86868b",
    ).pack(anchor="w")

    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    room_var = tk.StringVar(value=selected_room_number or "")
    checkin_choice_var = tk.StringVar(value="now")
    checkin_var = tk.StringVar(value=today)
    checkout_var = tk.StringVar(value=tomorrow)
    checkin_time_var = tk.StringVar(value="14:00")
    checkout_time_var = tk.StringVar(value="12:00")

    def create_styled_input(label_text, var, readonly=False):
        group = tk.Frame(frame, bg="white")
        group.pack(fill="x", pady=10)
        tk.Label(
            group,
            text=label_text.upper(),
            font=("SF Pro Text", 7, "bold"),
            bg="white",
            fg="#86868b",
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            group,
            textvariable=var,
            font=("SF Pro Text", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#0071e3",
            insertbackground="#0071e3",
        )
        if readonly:
            entry.configure(state="readonly", readonlybackground="#f5f5f7", fg="#1d1d1f")
        entry.pack(fill="x", ipady=12, padx=1)
        return entry

    create_styled_input("Selected Room", room_var, readonly=True)

    mode_group = tk.Frame(frame, bg="white")
    mode_group.pack(fill="x", pady=(10, 0))
    tk.Label(
        mode_group,
        text="CHECK-IN MODE",
        font=("SF Pro Text", 7, "bold"),
        bg="white",
        fg="#86868b",
    ).pack(anchor="w", pady=(0, 5))

    def set_widget_state(widget, enabled: bool):
        widget.configure(state="normal" if enabled else "disabled")

    checkin_date_group = tk.Frame(frame, bg="white")
    checkin_date_group.pack(fill="x", pady=10)
    tk.Label(
        checkin_date_group,
        text="CHECK-IN DATE (YYYY-MM-DD)",
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
        text="CHECK-IN TIME (HH:MM)",
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

    def on_checkin_mode_change():
        if (checkin_choice_var.get() or "now").lower() == "now":
            checkin_var.set(today)
            checkin_time_var.set((datetime.now() + timedelta(minutes=1)).strftime("%H:%M"))
            set_widget_state(checkin_date_entry, enabled=False)
            set_widget_state(checkin_time_entry, enabled=False)
        else:
            set_widget_state(checkin_date_entry, enabled=True)
            set_widget_state(checkin_time_entry, enabled=True)

    def on_checkin_mode_change_safe():
        try:
            on_checkin_mode_change()
        except tk.TclError:
            pass

    tk.Radiobutton(
        mode_group,
        text="Now/Today",
        variable=checkin_choice_var,
        value="now",
        bg="white",
        activebackground="white",
        font=("SF Pro Text", 11),
        command=on_checkin_mode_change_safe,
    ).pack(anchor="w")
    tk.Radiobutton(
        mode_group,
        text="Set day & time",
        variable=checkin_choice_var,
        value="set",
        bg="white",
        activebackground="white",
        font=("SF Pro Text", 11),
        command=on_checkin_mode_change,
    ).pack(anchor="w")

    create_styled_input("Check-out Date (YYYY-MM-DD)", checkout_var)
    create_styled_input("Check-out Time (HH:MM)", checkout_time_var)
    on_checkin_mode_change()

    price_frame = tk.Frame(frame, bg="#f5f5f7", padx=15, pady=15)
    price_frame.pack(fill="x", pady=20)
    price_total_lbl = tk.Label(
        price_frame,
        text="TOTAL: PHP 0.00",
        font=("SF Pro Text", 14, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
        anchor="w",
    )
    price_total_lbl.pack(fill="x")

    def update_price_preview(*_args):
        try:
            room_number = room_var.get()
            if not room_number:
                return

            room_list = RoomController.handle_list_rooms()
            price_per_night = 0.0
            for room in room_list:
                if str(room.get("room_number")) == str(room_number):
                    price_per_night = float(room.get("price", 0))
                    break

            start_date = datetime.strptime(checkin_var.get().strip(), "%Y-%m-%d")
            end_date = datetime.strptime(checkout_var.get().strip(), "%Y-%m-%d")
            nights = max((end_date - start_date).days, 1)
            total = price_per_night * nights
            price_total_lbl.config(text=f"TOTAL: PHP {total:,.2f}")
        except (TypeError, ValueError):
            pass

    checkin_var.trace_add("write", update_price_preview)
    checkout_var.trace_add("write", update_price_preview)
    update_price_preview()

    def handle_booking():
        room_num = room_var.get()
        c_in = checkin_var.get().strip()
        c_out = checkout_var.get().strip()

        if not room_num:
            messagebox.showwarning("System", "Please select a room first.")
            return

        success = RentalController.handle_confirm_booking(
            user_id=user_id,
            room_number=room_num,
            start_date=c_in,
            end_date=c_out,
            checkin_time=checkin_time_var.get().strip(),
            checkout_time=checkout_time_var.get().strip(),
            payment_status="paid",
        )

        if success:
            messagebox.showinfo("Success", "Booking confirmed.")
            if on_booked:
                on_booked()
            return

        messagebox.showerror("Error", "Could not complete booking. Please check the dates.")

    tk.Button(
        frame,
        text="Confirm Reservation",
        bg="#0071e3",
        fg="white",
        font=("SF Pro Text", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=handle_booking,
        activebackground="#0077ed",
        activeforeground="white",
    ).pack(fill="x", ipady=12, pady=(10, 0))

    return frame
