import tkinter as tk
from tkinter import messagebox

from utils.ui_constants import DANGER_BUTTON_STYLE


def create_topnav(root, logout_callback=None):
    topnav = tk.Frame(root, bg="#ffffff", height=80)
    topnav.pack(side=tk.TOP, fill=tk.X)

    def handle_logout():
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm and logout_callback:
            logout_callback()

    button1 = tk.Button(
        topnav,
        text="Log Out",
        padx=15,
        pady=5,
        bd=0,
        command=handle_logout,
        **DANGER_BUTTON_STYLE,
    )
    button1.pack(side=tk.RIGHT, padx=20, pady=20)

    return topnav

