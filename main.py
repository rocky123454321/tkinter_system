import tkinter as tk

def create_signup(root):
    # --- Apple-Style Constants ---
    APPLE_BG = "#f5f5f7"        
    APPLE_WHITE = "#ffffff"     
    APPLE_BLUE = "#0071e3"      
    APPLE_GRAY_TEXT = "#86868b" 
    APPLE_DARK_TEXT = "#1d1d1f" 
    CARD_WIDTH = 450            # Ginawang 450 para mas swabe ang 2-column layout

    signup_container = tk.Frame(root, bg=APPLE_BG)
    signup_container.pack(fill=tk.BOTH, expand=True)

    # --- Main Form Card ---
    form_card = tk.Frame(signup_container, bg=APPLE_WHITE, 
                         highlightthickness=1, highlightbackground="#d2d2d7")
    form_card.place(relx=0.5, rely=0.5, anchor="center")

    inner_frame = tk.Frame(form_card, bg=APPLE_WHITE, width=CARD_WIDTH)
    inner_frame.pack(padx=40, pady=40)

    # Title
    tk.Label(inner_frame, text="Create an account", bg=APPLE_WHITE,
             fg=APPLE_DARK_TEXT, font=("SF Pro Display", 18, "bold")).pack(pady=(0, 20))

    # --- Helper Function for Inputs ---
    def create_field(parent, label_text, placeholder, is_password=False):
        container = tk.Frame(parent, bg=APPLE_WHITE)
        tk.Label(container, text=label_text, font=("SF Pro Display", 9, "bold"), 
                 bg=APPLE_WHITE, fg=APPLE_GRAY_TEXT).pack(anchor="w")
        ent = tk.Entry(container, font=("SF Pro Display", 11), bg=APPLE_BG, 
                       relief="flat", highlightthickness=1, 
                       highlightbackground="#d2d2d7", highlightcolor=APPLE_BLUE)
        if is_password: ent.config(show="●")
        ent.insert(0, placeholder)
        ent.pack(fill="x", ipady=10, pady=(5, 0))
        return container, ent

    # --- 2 COLUMN SECTION (First Name & Last Name) ---
    name_row = tk.Frame(inner_frame, bg=APPLE_WHITE)
    name_row.pack(fill="x", pady=8)

    # First Name (Left Column)
    fname_cont, entry_fname = create_field(name_row, "First name", "Juan")
    fname_cont.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))

    # Last Name (Right Column)
    lname_cont, entry_lname = create_field(name_row, "Last name", "Reyes")
    lname_cont.pack(side=tk.LEFT, fill="x", expand=True, padx=(5, 0))

    # --- FULL WIDTH SECTIONS ---
    _, entry_email = create_field(inner_frame, "Email address", "juan@email.com")
    _.pack(fill="x", pady=8)

    _, entry_phone = create_field(inner_frame, "Phone number", "+63 912 345 6789")
    _.pack(fill="x", pady=8)

    # Password Section (Pwede ring 2 columns kung gusto mo)
    pass_row = tk.Frame(inner_frame, bg=APPLE_WHITE)
    pass_row.pack(fill="x", pady=8)

    p_cont, entry_pass = create_field(pass_row, "Password", "••••••••", True)
    p_cont.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))

    cp_cont, entry_confirm = create_field(pass_row, "Confirm password", "••••••••", True)
    cp_cont.pack(side=tk.LEFT, fill="x", expand=True, padx=(5, 0))

    # --- Footer & Buttons ---
    tk.Label(inner_frame, text="By signing up you agree to our Terms and Conditions.", 
             font=("SF Pro Display", 8), bg=APPLE_WHITE, fg=APPLE_GRAY_TEXT).pack(pady=15)

    tk.Button(inner_frame, text="Create account", font=("SF Pro Display", 11, "bold"),
              bg=APPLE_BLUE, fg="white", relief="flat", cursor="hand2", 
              borderwidth=0).pack(fill="x", ipady=12)

    footer = tk.Frame(inner_frame, bg=APPLE_WHITE)
    footer.pack(pady=(20, 0))
    tk.Label(footer, text="Already have one? ", bg=APPLE_WHITE, font=("SF Pro Display", 10)).pack(side=tk.LEFT)
    tk.Button(footer, text="Sign in", font=("SF Pro Display", 10, "bold"), 
              fg=APPLE_BLUE, bg=APPLE_WHITE, relief="flat", borderwidth=0, cursor="hand2").pack(side=tk.LEFT)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Apple Signup")
    root.geometry("600x750")
    create_signup(root)
    root.mainloop()