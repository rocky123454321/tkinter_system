import tkinter as tk
from tkinter import messagebox

from controllers.user_controller import UserController
from exceptions import ValidationError


def create_signup(root, app=None, preset_role: str = "user"):
    from utils.ui_constants import COLORS, BODY_FONT, LABEL_FONT, SUBTEXT_FONT

    container = tk.Frame(root, bg=COLORS["bg"])
    container.pack(fill="both", expand=True)

    card = tk.Frame(container, bg=COLORS["card"], highlightthickness=1, highlightbackground=COLORS["border"])
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=COLORS["card"], width=480)
    inner.pack(padx=40, pady=40)

    tk.Label(
        inner,
        text="Create account",
        bg=COLORS["card"],
        fg=COLORS["text_main"],
        font=("SF Pro Display", 20, "bold"),
    ).pack()

    tk.Label(
        inner,
        text="Select your role and enter your details.",
        bg=COLORS["card"],
        fg=COLORS["text_sub"],
        font=SUBTEXT_FONT,
    ).pack(pady=(2, 20))

    def make_input(parent, label_text, is_password=False):
        frame = tk.Frame(parent, bg=COLORS["card"])
        tk.Label(
            frame,
            text=label_text.upper(),
            bg=COLORS["card"],
            fg=COLORS["text_sub"],
            font=LABEL_FONT,
        ).pack(anchor="w")

        entry = tk.Entry(
            frame,
            font=BODY_FONT,
            bg=COLORS["bg"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
        )
        if is_password:
            entry.config(show="*")
        entry.pack(fill="x", ipady=10, pady=(4, 0))
        return frame, entry

    selected_role = tk.StringVar(value=preset_role)

    name_row = tk.Frame(inner, bg=COLORS["card"])
    name_row.pack(fill="x", pady=(0, 8))
    f_frame, ent_fname = make_input(name_row, "First name")
    f_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
    l_frame, ent_lname = make_input(name_row, "Last name")
    l_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))

    e_frame, ent_email = make_input(inner, "Email address")
    e_frame.pack(fill="x", pady=(0, 8))
    p_frame, ent_phone = make_input(inner, "Phone number")
    p_frame.pack(fill="x", pady=(0, 8))

    pass_row = tk.Frame(inner, bg=COLORS["card"])
    pass_row.pack(fill="x", pady=(0, 8))
    pw_frame, ent_pass = make_input(pass_row, "Password", is_password=True)
    pw_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
    cpw_frame, ent_confirm = make_input(pass_row, "Confirm password", is_password=True)
    cpw_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))

    error_v = tk.StringVar(value="")
    tk.Label(
        inner,
        textvariable=error_v,
        bg=COLORS["card"],
        fg="#db5c5c",
        font=LABEL_FONT,
    ).pack(anchor="w")

    def submit_signup():
        first    = ent_fname.get().strip()
        last     = ent_lname.get().strip()
        email    = ent_email.get().strip()
        phone    = ent_phone.get().strip()
        password = ent_pass.get()
        confirm  = ent_confirm.get()
        role     = selected_role.get()

        required_fields = {
            "First Name":       first,
            "Last Name":        last,
            "Email":            email,
            "Phone":            phone,
            "Password":         password,
            "Confirm Password": confirm,
        }
        for field_name, value in required_fields.items():
            if not value:
                error_v.set(f"{field_name} is required.")
                messagebox.showwarning("Input Error", f"The field '{field_name}' cannot be empty.")
                return

        if len(phone) != 11:
            error_v.set("Phone number must be exactly 11 digits.")
            return
        if not phone.isdigit():
            error_v.set("Phone number must contain numbers only.")
            return
        if not phone.startswith("0"):
            error_v.set("Invalid phone number format.")
            return
        if password != confirm:
            error_v.set("Passwords do not match.")
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            success = UserController.handle_signup(
                first_name=first,
                last_name=last,
                email=email,
                phone=phone,
                password=password,
                confirm_password=confirm,
                role=role,
            )
        except ValidationError as exc:
            error_v.set(str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Error", f"System error: {exc}")
            return

        if success:
            messagebox.showinfo("Success", f"Account created as {role.upper()}!")
            if app:
                app.show_login()
        else:
            error_v.set("Email already exists.")

    tk.Button(
        inner,
        text="Create account",
        command=submit_signup,
        bg=COLORS["accent"],
        fg=COLORS["card"],
        font=("SF Pro Text", 11, "bold"),
        relief="flat",
        cursor="hand2",
        borderwidth=0,
    ).pack(fill="x", ipady=12, pady=(16, 0))

    tk.Button(
        inner,
        text="Already have an account? Sign in",
        bg=COLORS["card"],
        fg=COLORS["accent"],
        font=SUBTEXT_FONT,
        borderwidth=0,
        cursor="hand2",
        command=lambda: app.show_login() if app else None,
    ).pack(pady=12)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x850")
    root.title("Sign Up")
    create_signup(root)
    root.mainloop()