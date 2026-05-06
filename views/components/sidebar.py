import tkinter as tk

def create_sidebar(root , Onclick_button):
 
    sidebar = tk.Frame(root, bg="#ffffff", width=220)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False) 


    label_brand = tk.Label(sidebar, text="RockStay", bg="#ffffff", 
                           fg="#1d1d1f", font=("Helvetica", 16, "bold"))

    label_sub = tk.Label(sidebar, text="Hotel System", bg="#ffffff", 
                         fg="#86868b", font=("Segoe UI Light", 10))
    



    label_main = tk.Label(sidebar, text="MAIN", bg="#ffffff", 
                         fg="#86868b", font=("Segoe UI Light", 10))
    

    btn_dashboard = tk.Button(
        sidebar, 
        text="  Dashboard",     
        font=("Helvetica", 10),
        bg="#f5f5f7",            
        fg="#1d1d1f", 
        relief="flat",   
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w",             
        cursor="hand2",          
        bd=0,
        pady=10
    )

    
    btn_Reservation = tk.Button(
        sidebar, 
        text="  Reservation",   
        font=("Helvetica", 10),
        bg="#f5f5f7",           
        fg="#1d1d1f", 
        relief="flat",   
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w",             
        cursor="hand2",          
        bd=0,
        pady=10
    )

    bt_Rooms = tk.Button(
        sidebar , 
        text="  Rooms",     
        font=("Helvetica", 10),
        bg="#f5f5f7",
        relief="flat",
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w" ,
        cursor="hand2",
        bd=0,
        pady=10
    )

    bt_Guest = tk.Button(
        sidebar , 
        text="  Guest",     
        font=("Helvetica", 10),
        bg="#f5f5f7",
        highlightbackground="#e1e1e1", highlightthickness=1,
        relief="flat",
        anchor="w" ,
        cursor="hand2",
        bd=0,
        pady=10
    )








     
    label_Operation = tk.Label(sidebar, text="OPERATION", bg="#ffffff", 
                         fg="#86868b", font=("Segoe UI Light", 10))
    

    bt_checkin = tk.Button(
        sidebar, 
        text="  Check-in / Check-out",     
        font=("Helvetica", 10),
        bg="#f5f5f7",            
        fg="#1d1d1f", 
        relief="flat",   
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w",             
        cursor="hand2",          
        bd=0,
        pady=10
    )

    
    bt_billing= tk.Button(
        sidebar, 
        text="  Billing",   
        font=("Helvetica", 10),
        bg="#f5f5f7",           
        fg="#1d1d1f", 
        relief="flat",   
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w",             
        cursor="hand2",          
        bd=0,
        pady=10
    )

    btn_reports = tk.Button(
        sidebar , 
        text="  Reports",     
        font=("Helvetica", 10),
        bg="#f5f5f7",
        relief="flat",
        highlightbackground="#e1e1e1", highlightthickness=1,
        anchor="w" ,
        
        cursor="hand2",
        bd=0,
        pady=10
    )

    label_brand.pack(padx=20, pady=(5, 0), anchor="w")
    label_sub.pack(padx=20, pady=(0, 30), anchor="w")


    label_main.pack(padx=20, pady=(0, 10), anchor="w")
    btn_dashboard.pack(fill=tk.X, padx=15, pady=5)
    btn_dashboard.config(command=lambda: Onclick_button("Dashboard"))

    btn_Reservation.pack(fill=tk.X, padx=15, pady=5)
    btn_Reservation.config(command=lambda: Onclick_button("Reservation"))

    bt_Rooms.pack(fill=tk.X, padx=15, pady=5)
    bt_Rooms.config(command=lambda: Onclick_button("Rooms"))
    bt_Guest.pack(fill=tk.X, padx=15, pady=5)

    label_Operation.pack(padx=20, pady=(30, 10), anchor="w")

    bt_checkin.pack(fill=tk.X, padx=15, pady=5)
    bt_billing.pack(fill=tk.X, padx=15, pady=5)
    btn_reports.pack(fill=tk.X, padx=15, pady=5)
    return sidebar