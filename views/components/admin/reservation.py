import tkinter as tk

def create_reservation(parent):  # <--- This name must match exactly!
    frame = tk.Frame(parent, bg="#f5f5f7")
    frame.pack(fill="both", expand=True)
    
    label = tk.Label(frame, text="Reservation Management", font=("Segoe UI", 18))
    label.pack(pady=20)
    
    return frame