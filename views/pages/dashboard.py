import tkinter as tk

def create_dashboard(root):
    dashboard = tk.Frame(root, bg="#f5f5f7")
    dashboard.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
   
        # --- DIV 1 ---
    div1 = tk.Frame(dashboard, bg="#ffffff", width=250, height=140, highlightbackground="#e1e1e1", highlightthickness=1)
    div1.pack_propagate(False)
    tk.Label(div1, text="Total Rooms", font=("Segoe UI", 10, "bold"), fg="#5f6368", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 0))
    tk.Label(div1, text="48", font=("Segoe UI", 24, "bold"), fg="#202124", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    tk.Label(div1, text="12 Floors", font=("Segoe UI", 9), fg="#1a73e8", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    div1.pack(side=tk.LEFT, anchor="n", padx=15, pady=15)

    # --- DIV 2 ---
    div2 = tk.Frame(dashboard, bg="#ffffff", width=250, height=140, highlightbackground="#e1e1e1", highlightthickness=1)
    div2.pack_propagate(False)
    tk.Label(div2, text="Active Guests", font=("Segoe UI", 10, "bold"), fg="#5f6368", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 0))
    tk.Label(div2, text="32", font=("Segoe UI", 24, "bold"), fg="#202124", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    tk.Label(div2, text="View details", font=("Segoe UI", 9), fg="#1a73e8", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    div2.pack(side=tk.LEFT, anchor="n", padx=15, pady=15)

    # --- DIV 3 ---
    div3 = tk.Frame(dashboard, bg="#ffffff", width=250, height=140, highlightbackground="#e1e1e1", highlightthickness=1)
    div3.pack_propagate(False)
    tk.Label(div3, text="Pending Tasks", font=("Segoe UI", 10, "bold"), fg="#5f6368", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 0))
    tk.Label(div3, text="08", font=("Segoe UI", 24, "bold"), fg="#202124", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    tk.Label(div3, text="Check list", font=("Segoe UI", 9), fg="#1a73e8", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    div3.pack(side=tk.LEFT, anchor="n", padx=15, pady=15)

    # --- DIV 4 ---
    div4 = tk.Frame(dashboard, bg="#ffffff", width=250, height=140, highlightbackground="#e1e1e1", highlightthickness=1)
    div4.pack_propagate(False)
    tk.Label(div4, text="Revenue", font=("Segoe UI", 10, "bold"), fg="#5f6368", bg="#ffffff").pack(anchor="w", padx=20, pady=(15, 0))
    tk.Label(div4, text="₱12,400", font=("Segoe UI", 24, "bold"), fg="#202124", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    tk.Label(div4, text="+15% from yesterday", font=("Segoe UI", 9), fg="#1a73e8", bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
    div4.pack(side=tk.LEFT, anchor="n", padx=15, pady=15)
    return dashboard
