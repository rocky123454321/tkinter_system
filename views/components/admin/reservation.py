import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from controllers.rental_controller import RentalController


def create_reservation(parent):
    from utils.ui_constants import (
        PAGE_TITLE_FONT, PAGE_TITLE_FG,
        COLORS, PAGE_PADX, PAGE_PADY, TITLE_PADY,
        LABEL_FONT, LABEL_FG, SUBTEXT_FONT, BODY_FONT,
    )

    container = tk.Frame(parent, bg=COLORS["bg"])
    container.pack(fill="both", expand=True)

    header = tk.Frame(container, bg=COLORS["bg"])
    header.pack(fill="x", pady=TITLE_PADY)

    tk.Label(
        header, text="Booking Overview",
        font=PAGE_TITLE_FONT, bg=COLORS["bg"], fg=PAGE_TITLE_FG,
        anchor="w",
    ).pack(side="left")

    tk.Button(
        header, text="Refresh Data", font=("SF Pro Text", 9, "bold"),
        bg=COLORS["card"], fg=COLORS["accent"], relief="flat", padx=15, pady=8,
        cursor="hand2", command=lambda: render(), highlightthickness=1,
        highlightbackground=COLORS["border"]
    ).pack(side="right")

    tk.Frame(container, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 10))

    panels_wrapper = tk.Frame(container, bg=COLORS["bg"])
    panels_wrapper.pack(fill="both", expand=True)

    def create_panel(parent_frame, title):
        section = tk.Frame(parent_frame, bg=COLORS["bg"])
        section.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(
            section, text=title.upper(), font=LABEL_FONT,
            bg=COLORS["bg"], fg=COLORS["text_sub"], pady=10
        ).pack(anchor="w")

        list_bg = tk.Frame(section, bg=COLORS["card"], highlightthickness=1, highlightbackground=COLORS["border"])
        list_bg.pack(fill="both", expand=True)

        return list_bg

    booking_bg     = create_panel(panels_wrapper, "Ongoing Bookings")
    reservation_bg = create_panel(panels_wrapper, "Upcoming Reservations")
    approval_bg    = create_panel(panels_wrapper, "For Approval (Paid)")

    PANEL_LABELS = {
        booking_bg:     ("No ongoing bookings",      "Active stays will appear here."),
        reservation_bg: ("No upcoming reservations", "Approved reservations will appear here."),
        approval_bg:    ("No pending approvals",     "Paid bookings awaiting approval will appear here."),
    }

    def build_scroll(bg_frame):
        canvas = tk.Canvas(bg_frame, bg=COLORS["card"], highlightthickness=0)
        scrollbar = tk.Scrollbar(bg_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["card"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)

        scroll_frame.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<MouseWheel>", on_mousewheel)
        scroll_frame.bind("<Map>", lambda e: bind_mousewheel(scroll_frame))

        return scroll_frame

    def show_empty(bg_frame):
        title_text, sub_text = PANEL_LABELS[bg_frame]

        inner = tk.Frame(bg_frame, bg=COLORS["card"])
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            inner,
            text=title_text,
            font=("SF Pro Text", 10, "bold"),
            bg=COLORS["card"],
            fg=COLORS["text_main"],
        ).pack()

        tk.Label(
            inner,
            text=sub_text,
            font=("SF Pro Text", 8),
            bg=COLORS["card"],
            fg=COLORS["text_sub"],
            wraplength=180,
            justify="center",
        ).pack(pady=(2, 0))

    def render():
        for w in booking_bg.winfo_children():     w.destroy()
        for w in reservation_bg.winfo_children(): w.destroy()
        for w in approval_bg.winfo_children():    w.destroy()

        rentals = RentalController.handle_list_all_bookings()
        today   = datetime.now().strftime("%Y-%m-%d")

        if not rentals:
            show_empty(booking_bg)
            show_empty(reservation_bg)
            show_empty(approval_bg)
            return

        booking_list     = build_scroll(booking_bg)
        reservation_list = build_scroll(reservation_bg)
        approval_list    = build_scroll(approval_bg)

        panel_has_cards = {
            booking_bg:     False,
            reservation_bg: False,
            approval_bg:    False,
        }

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

            if payment_status == "paid":
                target    = approval_list
                target_bg = approval_bg
            elif payment_status == "approved" and status == "active":
                target    = booking_list
                target_bg = booking_bg
            elif payment_status == "approved":
                target    = reservation_list
                target_bg = reservation_bg
            else:
                target    = reservation_list
                target_bg = reservation_bg

            panel_has_cards[target_bg] = True

            card = tk.Frame(target, bg=COLORS["card"], padx=16, pady=14)
            card.pack(fill="x")
            tk.Frame(target, bg="#f0f0f3", height=1).pack(fill="x")

            row1 = tk.Frame(card, bg=COLORS["card"])
            row1.pack(fill="x")

            tk.Label(
                row1,
                text=f"{r.get('first_name')} {r.get('last_name')}",
                font=("SF Pro Text", 10, "bold"), bg=COLORS["card"], fg=COLORS["text_main"]
            ).pack(side="left")

            badge_color = {
                "paid":     ("#e3f5e8", "#34c759"),
                "approved": ("#e8f0fe", COLORS["accent"]),
                "unpaid":   ("#fff3e0", "#ff9500"),
            }.get(payment_status, (COLORS["bg"], COLORS["text_sub"]))

            tk.Label(
                row1,
                text=f"  {payment_status.upper()}  ",
                font=LABEL_FONT,
                bg=badge_color[0], fg=badge_color[1],
                relief="flat", padx=4, pady=2
            ).pack(side="right")

            tk.Label(
                card,
                text=f"Room {r.get('room_number')}  •  {r.get('room_type')}  •  {num_guests} guest{'s' if int(num_guests) > 1 else ''}",
                font=("SF Pro Text", 8), bg=COLORS["card"], fg=COLORS["text_sub"]
            ).pack(anchor="w", pady=(2, 6))

            tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=4)

            dates_frame = tk.Frame(card, bg=COLORS["card"])
            dates_frame.pack(fill="x", pady=4)

            ci_block = tk.Frame(dates_frame, bg=COLORS["card"])
            ci_block.pack(side="left", expand=True, anchor="w")
            tk.Label(ci_block, text="CHECK-IN", font=LABEL_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="w")
            tk.Label(ci_block, text=checkin_date, font=("SF Pro Text", 10, "bold"),
                     bg=COLORS["card"], fg=COLORS["text_main"]).pack(anchor="w")
            tk.Label(ci_block, text=f"at {checkin_time}", font=("SF Pro Text", 8),
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="w")

            tk.Label(dates_frame, text="→", font=("SF Pro Text", 14),
                     bg=COLORS["card"], fg=COLORS["border"]).pack(side="left", padx=10)

            co_block = tk.Frame(dates_frame, bg=COLORS["card"])
            co_block.pack(side="left", expand=True, anchor="w")
            tk.Label(co_block, text="CHECK-OUT", font=LABEL_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="w")
            tk.Label(co_block, text=checkout_date, font=("SF Pro Text", 10, "bold"),
                     bg=COLORS["card"], fg=COLORS["text_main"]).pack(anchor="w")
            tk.Label(co_block, text=f"at {checkout_time}", font=("SF Pro Text", 8),
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="w")

            price_block = tk.Frame(dates_frame, bg=COLORS["card"])
            price_block.pack(side="right", anchor="e")
            tk.Label(price_block, text="TOTAL", font=LABEL_FONT,
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="e")
            tk.Label(price_block, text=f"₱{float(total_price):,.2f}",
                     font=("SF Pro Text", 11, "bold"), bg=COLORS["card"], fg=COLORS["text_main"]).pack(anchor="e")
            tk.Label(price_block, text=f"via {payment_method}", font=("SF Pro Text", 7),
                     bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="e")

            if special_req:
                tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=(6, 4))
                req_frame = tk.Frame(card, bg="#f9f9fb", padx=10, pady=6)
                req_frame.pack(fill="x")
                tk.Label(req_frame, text="Special Requests:", font=LABEL_FONT,
                         bg="#f9f9fb", fg=COLORS["text_sub"]).pack(anchor="w")
                tk.Label(req_frame, text=special_req, font=("SF Pro Text", 8),
                         bg="#f9f9fb", fg=COLORS["text_main"], wraplength=280, justify="left").pack(anchor="w")

            tk.Frame(card, bg="#f0f0f3", height=1).pack(fill="x", pady=(8, 6))

            btn_frame = tk.Frame(card, bg=COLORS["card"])
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
                    btn_frame, text="Approve",
                    font=("SF Pro Text", 9, "bold"),
                    bg=COLORS["accent"], fg="white", relief="flat",
                    padx=16, pady=6, cursor="hand2",
                    activebackground="#0077ed",
                    command=approve_booking
                ).pack(side="left", padx=(0, 8))

            tk.Button(
                btn_frame, text="Cancel",
                font=("SF Pro Text", 9),
                bg=COLORS["card"], fg="#ff3b30", relief="flat",
                padx=16, pady=6, cursor="hand2",
                highlightthickness=1, highlightbackground="#ffcdd2",
                activebackground="#fff5f5",
                command=cancel_booking
            ).pack(side="left")

        for bg_frame, has_cards in panel_has_cards.items():
            if not has_cards:
                show_empty(bg_frame)

    render()
    return container