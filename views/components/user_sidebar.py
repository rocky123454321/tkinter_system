import tkinter as tk


def create_user_sidebar(root, on_navigate=None):
    if on_navigate is None:
        on_navigate = lambda *_: None

    sidebar = tk.Frame(root, bg="#ffffff", width=220)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    def add_nav_button(text, page_name):
        btn = tk.Button(
            sidebar,
            text=f"  {text}",
            font=("Helvetica", 10),
            bg="#f5f5f7",
            fg="#1d1d1f",
            relief="flat",
            highlightbackground="#e1e1e1",
            highlightthickness=1,
            anchor="w",
            cursor="hand2",
            bd=0,
            pady=10,
            command=lambda: on_navigate(page_name),
        )
        btn.pack(fill=tk.X, padx=15, pady=5)
        return btn

    tk.Label(
        sidebar,
        text="RockStay",
        bg="#ffffff",
        fg="#1d1d1f",
        font=("Helvetica", 16, "bold"),
    ).pack(padx=20, pady=(20, 0), anchor="w")
    tk.Label(
        sidebar,
        text="User Area",
        bg="#ffffff",
        fg="#86868b",
        font=("Segoe UI Light", 10),
    ).pack(padx=20, pady=(0, 30), anchor="w")
    tk.Label(
        sidebar,
        text="MAIN",
        bg="#ffffff",
        fg="#86868b",
        font=("Segoe UI Light", 10),
    ).pack(padx=20, pady=(0, 10), anchor="w")

    add_nav_button("Dashboard", "Dashboard")
    add_nav_button("Booking", "Booking")
    add_nav_button("Map", "Map")
    add_nav_button("Settings", "Settings")

    return sidebar
