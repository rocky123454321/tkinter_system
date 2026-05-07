import tkinter as tk

def create_sidebar(root, Onclick_button=None):
    # Default lambda para hindi mag-error kung walang Onclick_button na pinasa
    if Onclick_button is None:
        Onclick_button = lambda x: print(f"Clicked: {x}")

    # --- Sidebar Container ---
    sidebar = tk.Frame(root, bg="#ffffff", width=220)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False) 

    # --- Helper Function para sa Buttons (Clean Code) ---
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
            command=lambda: Onclick_button(page_name)
        )
        btn.pack(fill=tk.X, padx=15, pady=5)
        return btn

    # --- Branding Section ---
    tk.Label(sidebar, text="RockStay", bg="#ffffff", fg="#1d1d1f", 
             font=("Helvetica", 16, "bold")).pack(padx=20, pady=(20, 0), anchor="w")
    
    tk.Label(sidebar, text="Hotel System", bg="#ffffff", fg="#86868b", 
             font=("Segoe UI Light", 10)).pack(padx=20, pady=(0, 30), anchor="w")

    # --- MAIN Section ---
    tk.Label(sidebar, text="MAIN", bg="#ffffff", fg="#86868b", 
             font=("Segoe UI Light", 10)).pack(padx=20, pady=(0, 10), anchor="w")
    
    add_nav_button("Dashboard", "Dashboard")
    add_nav_button("Reservation", "Reservation")
    add_nav_button("Rooms", "Rooms")
    add_nav_button("Guest", "Guest")

    # --- OPERATION Section ---
    tk.Label(sidebar, text="OPERATION", bg="#ffffff", fg="#86868b", 
             font=("Segoe UI Light", 10)).pack(padx=20, pady=(30, 10), anchor="w")
    
    add_nav_button("Check-in / Check-out", "Check-in")
    add_nav_button("Billing", "Billing")
    add_nav_button("Reports", "Reports")

    return sidebar