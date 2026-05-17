import tkinter as tk
from PIL import Image, ImageTk

from utils.ui_constants import (
    PAGE_TITLE_FONT,
    PAGE_TITLE_FG,
    BG_CARD,
    BG_PAGE,
    TEXT_MAIN,
    TEXT_SUB,
    BORDER,
)


def create_user_sidebar(root, on_navigate=None):
    if on_navigate is None:
        on_navigate = lambda *_: None

    sidebar = tk.Frame(root, bg=BG_CARD, width=220)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    def add_nav_button(text, page_name):
        btn = tk.Button(
            sidebar,
            text=f"  {text}",
            font=("Helvetica", 10),
            bg=BG_PAGE,
            fg=TEXT_MAIN,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
            anchor="w",
            cursor="hand2",
            bd=0,
            pady=10,
            command=lambda: on_navigate(page_name),
        )
        btn.pack(fill=tk.X, padx=15, pady=5)
        return btn

    logo = Image.open("assets/logo.png")
    logo = logo.resize((40, 40))
    img = ImageTk.PhotoImage(logo)

    logo_frame = tk.Frame(sidebar, bg=BG_CARD)
    logo_frame.pack(padx=20, pady=(20, 5), anchor="w")

    label1 = tk.Label(logo_frame, image=img, bg=BG_CARD)
    label1.image = img
    label1.pack(side=tk.LEFT)

    tk.Label(
        logo_frame,
        text="RockStay",
        bg=BG_CARD,
        fg=PAGE_TITLE_FG,
        font=PAGE_TITLE_FONT,
    ).pack(side=tk.LEFT, padx=(10, 0))

    tk.Label(
        sidebar,
        text="User Area",
        bg=BG_CARD,
        fg=TEXT_SUB,
        font=("Segoe UI Light", 10),
    ).pack(padx=20, pady=(0, 30), anchor="w")

    tk.Label(
        sidebar,
        text="MAIN",
        bg=BG_CARD,
        fg=TEXT_SUB,
        font=("Segoe UI Light", 10),
    ).pack(padx=20, pady=(0, 10), anchor="w")

    add_nav_button("Home", "Dashboard")
    add_nav_button("Booking", "Booking")
    add_nav_button("Map", "Map")
    add_nav_button("Settings", "Settings")

    return sidebar
