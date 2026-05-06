import tkinter as tk


def create_topnav(root):
    topnav  = tk.Frame(root, bg="#ffffff", height=80)
    topnav.pack(side=tk.TOP, fill=tk.X)


    button1 = tk.Button(
        topnav, 
        text="New bookings", 
        font=("Helvetica", 12),
        bg="#f5f5f7", 
        fg="#1d1d1f", 
        relief="flat", 
        cursor="hand2",
        bd=0,
        padx=10
    )
    button1.pack(side=tk.RIGHT, padx=10, pady=10)
    return topnav