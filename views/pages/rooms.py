import tkinter as tk

def create_rooms(root):
    
    rooms = tk.Frame(root , bg="#f5f5f7")
    rooms.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    top_bar = tk.Frame(rooms, bg="#f5f5f7")
    top_bar.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

    button1 = tk.Button(
        top_bar, 
        text="Maintenance rooms", 
        font=("Helvetica", 12),
        bg="#f5f5f7", 
        fg="#1d1d1f", 
        relief="flat", 
        cursor="hand2",
        bd=0,
        padx=10,
        anchor="w" ,
        highlightbackground="#e1e1e1", highlightthickness=1,
    )
    button2 = tk.Button(
        top_bar,
        text="Available rooms", 
        font=("Helvetica", 12),
        bg="#f5f5f7", 
        fg="#1d1d1f", 
        relief="flat", 
        cursor="hand2",
        highlightbackground="#e1e1e1", highlightthickness=1,
        bd=0,
        padx=10
    )

    button3 = tk.Button(
        top_bar,
        text="Occupied rooms", 
        font=("Helvetica", 12),
        highlightbackground="#e1e1e1", highlightthickness=1,
        bg="#f5f5f7", 
        fg="#1d1d1f",
        relief="flat",
        cursor="hand2",
        bd=0,
        padx=10
    )


    button2.pack(side=tk.LEFT, padx=10, pady=10)
    button3.pack(side=tk.LEFT, padx=10, pady=10)    
    button1.pack(side=tk.LEFT, padx=10, pady=10)
    return rooms