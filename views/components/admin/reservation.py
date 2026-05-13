import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from  controllers.rental_controller import RentalController


def create_reservation(parent):
    container = tk.Frame(parent, bg="#f5f5f7")
    container.pack(fill="both", expand=True, padx=30, pady=20)


    header = tk.Frame(container, bg="#f5f5f7")
    header.pack(fill="x", pady=(0, 25))

    tk.Label(
        header, text="Booking Overview",
        font=("SF Pro Display", 20, "bold"), bg="#f5f5f7", fg="#1d1d1f"
    ).pack(side="left")

    tk.Button(
        header, text="Refresh Data", font=("SF Pro Text", 9, "bold"),
        bg="#ffffff", fg="#0071e3", relief="flat", padx=15, pady=8,
        cursor="hand2", command=lambda: render(), highlightthickness=1,
        highlightbackground="#e1e1e1"
    ).pack(side="right")


    panels_wrapper = tk.Frame(container, bg="#f5f5f7")
    panels_wrapper.pack(fill="both", expand=True)

    def create_panel(parent_frame, title):
        section = tk.Frame(parent_frame, bg="#f5f5f7")
        section.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(
            section, text=title.upper(), font=("SF Pro Text", 9, "bold"),
            bg="#f5f5f7", fg="#86868b", pady=10
        ).pack(anchor="w")

        list_bg = tk.Frame(section, bg="#ffffff", highlightthickness=1, highlightbackground="#e1e1e1")
        list_bg.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_bg, bg="#ffffff", highlightthickness=0)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))
        canvas.pack(side="left", fill="both", expand=True)

        return scroll_frame

    booking_list     = create_panel(panels_wrapper, "Ongoing Bookings")
    reservation_list = create_panel(panels_wrapper, "Upcoming Reservations")
    approval_list    = create_panel(panels_wrapper, "For Approval (Paid)")

    def render():
        for w in booking_list.winfo_children():     w.destroy()
        for w in reservation_list.winfo_children(): w.destroy()
        for w in approval_list.winfo_children():    w.destroy()

        rentals = RentalController.handle_list_all_bookings()
        today   = datetime.now().strftime("%Y-%m-%d")

        if not rentals:
            for t in [booking_list, reservation_list, approval_list]:
                tk.Label(t, text="No entries", font=("SF Pro Text", 9),
                         bg="#ffffff", fg="#b6b6bb", pady=20).pack()
            return

        for r in rentals:
            status         = str(r.get("status") or "").lower()
            payment_status = str(r.get("payment_status") or "").lower()
            checkin_date   = str(r.get("checkin") or "")
            checkout_date  = str(r.get("checkout") or "")
            checkin_time   = str(r.get("checkin_time") or "14:00")
            checkout_time  = str(r.get("checkout_time") or "12:00")
            num_guests     = r.get("num_guests") or 1
            total_price    = r.get("total_price") or 0.0
            special_req    = str(r.get("special_requests") or "").strip()
            payment_method = str(r.get("payment_method") or "counter").capitalize()

            if status not in ["active", "pending"]:
                continue


            if status == "pending" and payment_status == "paid":
                target = approval_list
            elif status == "pending" and payment_status == "approved":
                target = reservation_list
            elif status == "pending":
                target = reservation_list
            else:
                target = booking_list if checkin_date >= today else reservation_list


            card = tk.Frame(target, bg="#ffffff", padx=16, pady=14)
            card.pack(fill="x")
            tk.Frame(target, bg="#f0f0f3", height=1).pack(fill="x")


            row1 = tk.Frame(card, bg="#ffffff")
            row1.pack(fill="x")

            tk.Label(
                row1,
                text=f"{r.get('first_name')} {r.get('last_name')}",
                font=("SF Pro Text", 10, "bold"), bg="#ffffff", fg="#1d1d1f"
            ).pack(side="left")


            badge_color = {
                "paid":     ("#e3f5e8", "#34c759"),
                "approved": ("#e8f0fe", "#0071e3"),
                "unpaid":   ("#fff3e0", "#ff9500"),
            }.get(payment_status, ("#f5f5f7", "#86868b"))

            tk.Label(
                row1,
                text=f"  {payment_status.upper()}  ",
                font=("SF Pro Text", 7, "bold"),
                bg=badge_color[0], fg=badge_color[1],
                relief="flat", padx=4, pady=2
            ).pack(side="right")


            tk.Label(
                card,
                text=f"Room {r.get('room_number')}  •  {r.get('room_type')}  •  {num_guests} guest{'s' if int(num_guests) > 1 else ''}",
                font=("SF Pro Text", 8), bg="#ffffff", fg="#86868b"
            ).pack(anchor="w", pady=(2, 6))


            tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=4)


            dates_frame = tk.Frame(card, bg="#ffffff")
            dates_frame.pack(fill="x", pady=4)


            ci_block = tk.Frame(dates_frame, bg="#ffffff")
            ci_block.pack(side="left", expand=True, anchor="w")
            tk.Label(ci_block, text="CHECK-IN", font=("SF Pro Text", 7, "bold"),
                     bg="#ffffff", fg="#86868b").pack(anchor="w")
            tk.Label(ci_block, text=checkin_date, font=("SF Pro Text", 10, "bold"),
                     bg="#ffffff", fg="#1d1d1f").pack(anchor="w")
            tk.Label(ci_block, text=f"at {checkin_time}", font=("SF Pro Text", 8),
                     bg="#ffffff", fg="#86868b").pack(anchor="w")


            tk.Label(dates_frame, text="→", font=("SF Pro Text", 14),
                     bg="#ffffff", fg="#c7c7cc").pack(side="left", padx=10)


            co_block = tk.Frame(dates_frame, bg="#ffffff")
            co_block.pack(side="left", expand=True, anchor="w")
            tk.Label(co_block, text="CHECK-OUT", font=("SF Pro Text", 7, "bold"),
                     bg="#ffffff", fg="#86868b").pack(anchor="w")
            tk.Label(co_block, text=checkout_date, font=("SF Pro Text", 10, "bold"),
                     bg="#ffffff", fg="#1d1d1f").pack(anchor="w")
            tk.Label(co_block, text=f"at {checkout_time}", font=("SF Pro Text", 8),
                     bg="#ffffff", fg="#86868b").pack(anchor="w")


            price_block = tk.Frame(dates_frame, bg="#ffffff")
            price_block.pack(side="right", anchor="e")
            tk.Label(price_block, text="TOTAL", font=("SF Pro Text", 7, "bold"),
                     bg="#ffffff", fg="#86868b").pack(anchor="e")
            tk.Label(price_block, text=f"₱{float(total_price):,.2f}",
                     font=("SF Pro Text", 11, "bold"), bg="#ffffff", fg="#1d1d1f").pack(anchor="e")
            tk.Label(price_block, text=f"via {payment_method}", font=("SF Pro Text", 7),
                     bg="#ffffff", fg="#86868b").pack(anchor="e")


            if special_req:
                tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=(6, 4))
                req_frame = tk.Frame(card, bg="#f9f9fb", padx=10, pady=6)
                req_frame.pack(fill="x")
                tk.Label(req_frame, text="Special Requests:", font=("SF Pro Text", 7, "bold"),
                         bg="#f9f9fb", fg="#86868b").pack(anchor="w")
                tk.Label(req_frame, text=special_req, font=("SF Pro Text", 8),
                         bg="#f9f9fb", fg="#1d1d1f", wraplength=280, justify="left").pack(anchor="w")


            tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=(8, 6))

            btn_frame = tk.Frame(card, bg="#ffffff")
            btn_frame.pack(fill="x")

            def cancel_booking(rid=r.get("id")):
                if messagebox.askyesno("Cancel", "Cancel this reservation?"):
                    RentalController.handle_cancel_booking(rental_id=rid)
                    render()

            def approve_booking(rid=r.get("id")):
                ok = RentalController.handle_approve_booking(rental_id=rid)
                if not ok:
                    messagebox.showerror("Error", "Failed to approve booking.")
                render()

            if target == approval_list:
                tk.Button(
                    btn_frame, text="✓  Approve",
                    font=("SF Pro Text", 9, "bold"),
                    bg="#0071e3", fg="white", relief="flat",
                    padx=16, pady=6, cursor="hand2",
                    activebackground="#0077ed",
                    command=approve_booking
                ).pack(side="left", padx=(0, 8))

            tk.Button(
                btn_frame, text="✕  Cancel",
                font=("SF Pro Text", 9),
                bg="#ffffff", fg="#ff3b30", relief="flat",
                padx=16, pady=6, cursor="hand2",
                highlightthickness=1, highlightbackground="#ffcdd2",
                activebackground="#fff5f5",
                command=cancel_booking
            ).pack(side="left")

    render()
    return container
