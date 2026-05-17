import tkinter as tk
from tkinter import ttk

from controllers.rental_controller import RentalController
from controllers.user_controller import UserController


def create_guest(parent):
    from utils.ui_constants import (
        PAGE_TITLE_FONT, PAGE_TITLE_FG,
        COLORS, TITLE_PADY, LABEL_FONT, BODY_FONT, SUBTEXT_FONT,
    )

    main_container = tk.Frame(parent, bg=COLORS["bg"])
    main_container.pack(fill="both", expand=True)

    # ── Header ───────────────────────────────────────────────────────────────
    header = tk.Frame(main_container, bg=COLORS["bg"])
    header.pack(fill="x", pady=TITLE_PADY)

    tk.Label(
        header, text="Guest Management",
        font=PAGE_TITLE_FONT, bg=COLORS["bg"], fg=PAGE_TITLE_FG,
    ).pack(side="left")

    btn_refresh = tk.Button(
        header, text="⟳ Refresh", font=("SF Pro Text", 9),
        bg=COLORS["accent"], fg="white", relief="flat", padx=15,
        cursor="hand2"
    )
    btn_refresh.pack(side="right")

    tk.Frame(main_container, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 10))

    # ── Table header ─────────────────────────────────────────────────────────
    table_header = tk.Frame(main_container, bg=COLORS["bg"])
    table_header.pack(fill="x", pady=(0, 5))

    for i in range(6):
        table_header.columnconfigure(i, weight=1, uniform="col")

    column_titles = ["NO", "FIRST NAME", "LAST NAME", "EMAIL", "CONTACT", "STATUS"]
    for i, text in enumerate(column_titles):
        alignment = "w" if i < 5 else "e"
        tk.Label(table_header, text=text, font=LABEL_FONT,
                 bg=COLORS["bg"], fg=COLORS["text_sub"]).grid(row=0, column=i, sticky=alignment)

    # ── Scrollable list ──────────────────────────────────────────────────────
    scroll_wrapper = tk.Frame(main_container, bg=COLORS["bg"])
    scroll_wrapper.pack(fill="both", expand=True)

    canvas = tk.Canvas(scroll_wrapper, bg=COLORS["bg"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_wrapper, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

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


    def load_guests():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        guests = UserController.handle_list_guests()

        if not guests:
            tk.Label(scrollable_frame, text="No guests registered yet.",
                     font=SUBTEXT_FONT, bg=COLORS["bg"], fg=COLORS["text_sub"]).pack(pady=50)
            return

        all_rentals    = RentalController.handle_list_all_bookings()
        active_user_ids = {
            r["user_id"] for r in all_rentals
            if str(r.get("status") or "").lower() == "active"
        }

        for guest in guests:
            g_id   = guest.get("id")
            f_name = guest.get("first_name")
            l_name = guest.get("last_name")
            email  = guest.get("email")
            phone  = guest.get("phone")

            card = tk.Frame(scrollable_frame, bg=COLORS["card"], pady=12, padx=20,
                            highlightthickness=1, highlightbackground=COLORS["border"])
            card.pack(fill="x", pady=2)

            for i in range(6):
                card.columnconfigure(i, weight=1, uniform="col")

            tk.Label(card, text=f"#{g_id}", font=("SF Pro Text", 8, "bold"),
                     bg=COLORS["card"], fg=COLORS["accent"]).grid(row=0, column=0, sticky="w")
            tk.Label(card, text=f_name, font=("SF Pro Text", 9, "bold"),
                     bg=COLORS["card"], fg=COLORS["text_main"]).grid(row=0, column=1, sticky="w")
            tk.Label(card, text=l_name, font=("SF Pro Text", 9),
                     bg=COLORS["card"], fg=COLORS["text_main"]).grid(row=0, column=2, sticky="w")
            tk.Label(card, text=email, font=("SF Pro Text", 9),
                     bg=COLORS["card"], fg=COLORS["text_sub"]).grid(row=0, column=3, sticky="w")
            tk.Label(card, text=phone if phone else "N/A", font=("SF Pro Text", 9),
                     bg=COLORS["card"], fg=COLORS["text_main"]).grid(row=0, column=4, sticky="w")

            if g_id in active_user_ids:
                bg_color, fg_color, label = "#e2f9e1", COLORS["success"], "ACTIVE"
            else:
                bg_color, fg_color, label = COLORS["bg"], COLORS["text_sub"], "NO BOOKING"

            status_frame = tk.Frame(card, bg=bg_color, padx=10, pady=3)
            status_frame.grid(row=0, column=5, sticky="e")
            tk.Label(status_frame, text=label, font=LABEL_FONT,
                     bg=bg_color, fg=fg_color).pack()

    btn_refresh.config(command=load_guests)
    load_guests()
    return main_container