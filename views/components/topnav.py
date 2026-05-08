import tkinter as tk
from tkinter import messagebox


def create_topnav(root, logout_callback=None):

    topnav = tk.Frame(root, bg="#ffffff", height=80)
    topnav.pack(side=tk.TOP, fill=tk.X)

    def handle_logout():
        # Magpakita ng confirmation dialog
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            
            if logout_callback:
                logout_callback()


    button1 = tk.Button(
        topnav,
        text="Log Out",
        font=("Helvetica", 10, "bold"),
        bg="#ff3b30",
        fg="white",
        relief="flat",
        cursor="hand2",
        bd=0,
        padx=15,
        pady=5,
        command=handle_logout  
    )
    button1.pack(side=tk.RIGHT, padx=20, pady=20)

    return topnav