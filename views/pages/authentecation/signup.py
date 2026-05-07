import tkinter as tk

def create_signup(root):
    # --- 1. SETTINGS & COLORS (Apple Aesthetic) ---
    APPLE_BG = "#f5f5f7"        # Light Gray background
    APPLE_WHITE = "#ffffff"     # Card background
    APPLE_BLUE = "#0071e3"      # Signature Apple Blue
    APPLE_GRAY_TEXT = "#86868b" # Secondary text
    APPLE_DARK_TEXT = "#1d1d1f" # Primary text
    CARD_WIDTH = 480            # Eksaktong lapad para sa 2-column look

    # Main Container
    signup_container = tk.Frame(root, bg=APPLE_BG)
    signup_container.pack(fill=tk.BOTH, expand=True)

    # --- 2. LOGIC FUNCTIONS ---
    def password_match(pw1, pw2):
        return pw1 == pw2

    def submit_signup():
        print("Signup submitted!")
        firstname = ent_fname.get()
        lastname = ent_lname.get()
        email = ent_email.get()
        phone = ent_phone.get()
        
        if not password_match(ent_pass.get(), ent_confirm.get()):
            print("Error: Passwords do not match!")
            return
            
        password = ent_pass.get()
        print(f"First Name: {firstname}")
        print(f"Last Name: {lastname}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Password: {password}") 

    # --- 3. INPUT COMPONENT CREATOR ---
    def add_input_group(parent, label, placeholder, is_password=False):
        container = tk.Frame(parent, bg=APPLE_WHITE)
        
        # Label sa itaas
        tk.Label(container, text=label, font=("SF Pro Display", 9, "bold"), 
                 bg=APPLE_WHITE, fg=APPLE_GRAY_TEXT).pack(anchor="w")
        
        # Entry Box
        entry = tk.Entry(container, font=("SF Pro Display", 11), bg=APPLE_BG, 
                         relief="flat", highlightthickness=1, 
                         highlightbackground="#d2d2d7", highlightcolor=APPLE_BLUE)
        
        if is_password: 
            entry.config(show="●")
            
        entry.insert(0, placeholder) 
        entry.pack(fill="x", ipady=10, pady=(5, 0))
        
        return container, entry

    # --- 4. THE SIGN-UP CARD ---
    form_card = tk.Frame(signup_container, bg=APPLE_WHITE, highlightthickness=1, highlightbackground="#d2d2d7")
    form_card.place(relx=0.5, rely=0.5, anchor="center")

    inner_frame = tk.Frame(form_card, bg=APPLE_WHITE, width=CARD_WIDTH)
    inner_frame.pack(padx=40, pady=40)

    # Header Section
    tk.Label(inner_frame, text="Create your account", bg=APPLE_WHITE, 
             fg=APPLE_DARK_TEXT, font=("SF Pro Display", 20, "bold")).pack(pady=(0, 5))
    tk.Label(inner_frame, text="Join our community today.", bg=APPLE_WHITE, 
             fg=APPLE_GRAY_TEXT, font=("SF Pro Display", 10)).pack(pady=(0, 25))

    # --- 5. THE FORM FIELDS ---

    # ROW 1: Names (2 Columns)
    name_row = tk.Frame(inner_frame, bg=APPLE_WHITE)
    name_row.pack(fill="x", pady=8)

    fname_group, ent_fname = add_input_group(name_row, "First name", "Juan")
    fname_group.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))

    lname_group, ent_lname = add_input_group(name_row, "Last name", "Reyes")
    lname_group.pack(side=tk.LEFT, fill="x", expand=True, padx=(5, 0))

    # ROW 2: Email (Full Width)
    email_group, ent_email = add_input_group(inner_frame, "Email address", "juan@email.com")
    email_group.pack(fill="x", pady=8)

    # ROW 3: Phone (Full Width)
    phone_group, ent_phone = add_input_group(inner_frame, "Phone number", "+63 912 345 6789")
    phone_group.pack(fill="x", pady=8)

    # ROW 4: Password Section (2 Columns)
    pass_row = tk.Frame(inner_frame, bg=APPLE_WHITE)
    pass_row.pack(fill="x", pady=8)

    p_group, ent_pass = add_input_group(pass_row, "Password", "••••••••", True)
    p_group.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))

    cp_group, ent_confirm = add_input_group(pass_row, "Confirm password", "••••••••", True)
    cp_group.pack(side=tk.LEFT, fill="x", expand=True, padx=(5, 0))

    # --- 6. FOOTER & ACTIONS ---

    # Terms
    terms_lbl = tk.Label(inner_frame, text="By signing up, you agree to our Terms and Privacy Policy.",  
                         font=("SF Pro Display", 8), bg=APPLE_WHITE, fg=APPLE_GRAY_TEXT)
    terms_lbl.pack(pady=20)

    # Submit Button
    btn_signup = tk.Button(inner_frame, command=submit_signup, text="Create account", 
                           font=("SF Pro Display", 11, "bold"), bg=APPLE_BLUE, fg="white", 
                           relief="flat", activebackground="#0077ed", activeforeground="white", 
                           cursor="hand2", borderwidth=0)
    btn_signup.pack(fill="x", ipady=12)

    # Switch to Sign In
    login_frame = tk.Frame(inner_frame, bg=APPLE_WHITE)
    login_frame.pack(pady=(20, 0))
    
    tk.Label(login_frame, text="Already have one? ", bg=APPLE_WHITE, 
             font=("SF Pro Display", 10)).pack(side=tk.LEFT)
    
    tk.Button(login_frame, text="Sign in", font=("SF Pro Display", 10, "bold"), 
              fg=APPLE_BLUE, bg=APPLE_WHITE, relief="flat", 
              borderwidth=0, cursor="hand2").pack(side=tk.LEFT)

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    app = tk.Tk()
    app.title("Apple Style Signup")
    app.geometry("600x800")
    create_signup(app)
    app.mainloop()