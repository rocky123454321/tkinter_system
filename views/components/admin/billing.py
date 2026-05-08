import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.RentalModel import RentalModel
from models.RoomModel import RoomModel


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
        text="↻ Refresh",
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

    # Cards
    card_total = tk.Frame(summary, bg="#ffffff", padx=20, pady=15, highlightthickness=1, highlightbackground="#e5e5e7")
    card_total.pack(side="left", padx=10, fill="y")
    tk.Label(card_total, text="TOTAL COMPLETED", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#86868b").pack(anchor="w")
    v_total = tk.Label(card_total, text="-", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff")
    v_total.pack(anchor="w")

    card_revenue = tk.Frame(summary, bg="#ffffff", padx=20, pady=15, highlightthickness=1, highlightbackground="#e5e5e7")
    card_revenue.pack(side="left", padx=10, fill="y")
    tk.Label(card_revenue, text="ESTIMATED REVENUE", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#86868b").pack(anchor="w")
    v_revenue = tk.Label(card_revenue, text="-", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007aff")
    v_revenue.pack(anchor="w")

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
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def clear_rows():
        for w in scrollable_frame.winfo_children():
            w.destroy()

    def price_map_by_room_number():
        rooms = RoomModel.get_all_rooms()
        return {str(r.get("room_number")): r.get("price") for r in rooms}

    def render():
        clear_rows()
        rentals = RentalModel.get_rentals_joined()
        pmap = price_map_by_room_number()

        completed = [r for r in rentals if str(r.get("status") or "").lower() == "completed"]
        active = [r for r in rentals if str(r.get("status") or "").lower() == "active"]

        revenue = 0.0
        for r in completed:
            rn = str(r.get("room_number") or "")
            price = pmap.get(rn)
            try:
                revenue += float(price) if price is not None else 0.0
            except Exception:
                pass

        v_total.config(text=str(len(completed)))
        v_revenue.config(text=f"₱{revenue:,.2f}")

        if not completed:
            tk.Label(
                scrollable_frame,
                text="No completed bookings yet.",
                font=("Segoe UI", 10, "italic"),
                bg="#f5f5f7",
                fg="#86868b",
            ).pack(pady=60)
            return

        for r in completed[:200]:
            rid = r.get("id")
            guest_name = f"{r.get('first_name','')} {r.get('last_name','')}".strip()
            room_number = r.get("room_number")
            room_type = r.get("room_type") or ""
            created_at = r.get("created_at") or ""

            price = pmap.get(str(room_number), 0)

            row = tk.Frame(
                scrollable_frame,
                bg="white",
                pady=12,
                padx=20,
                highlightthickness=1,
                highlightbackground="#d2d2d7",
            )
            row.pack(fill="x", pady=8)

            tk.Label(row, text=f"Invoice #{rid}", font=("Segoe UI", 9, "bold"), bg="white", fg="#0071e3").grid(
                row=0, column=0, sticky="w"
            )
            tk.Label(row, text=guest_name, font=("Segoe UI", 10, "bold"), bg="white", fg="#1d1d1f").grid(
                row=1, column=0, sticky="w"
            )
            tk.Label(row, text=f"{room_number} • {room_type}", font=("Segoe UI", 9), bg="white", fg="#86868b").grid(
                row=0, column=1, rowspan=2, sticky="w", padx=(25, 0)
            )
            tk.Label(row, text=f"₱{float(price or 0):,.2f}", font=("Segoe UI", 12, "bold"), bg="white", fg="#0071e3").grid(
                row=0, column=2, sticky="e", padx=(10, 0)
            )
            if created_at:
                tk.Label(row, text=str(created_at), font=("Segoe UI", 8), bg="white", fg="#86868b").grid(
                    row=1, column=2, sticky="e", padx=(10, 0)
                )

    btn_refresh.config(command=render)
    render()

    return main_container

