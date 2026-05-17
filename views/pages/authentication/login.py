import tkinter as tk

from  controllers.user_controller import UserController
from utils import ValidationError


BG = "#f5f5f7"
WHITE = "#ffffff"
BLUE = "#0071e3"
GRAY = "#86868b"
DARK = "#1d1d1f"
BORDER = "#d2d2d7"


def create_login(root, app=None):
    container = tk.Frame(root, bg=BG)
    container.pack(fill="both", expand=True)

    card = tk.Frame(container, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=WHITE, width=400)
    inner.pack(padx=50, pady=50)

    tk.Label(
        inner,
        text="Sign In",
        bg=WHITE,
        fg=DARK,
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=(0, 5))
    tk.Label(
        inner,
        text="Enter your email and password.",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10),
    ).pack(pady=(0, 30))

    def make_input(label_text, placeholder="", is_password=False):
        frame = tk.Frame(inner, bg=WHITE)
        frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            frame,
            text=label_text,
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        entry = tk.Entry(
            frame,
            font=("Segoe UI", 11),
            bg=BG,
            relief="flat",
            width=37,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE,
        )
        entry.pack(fill="x", ipady=10, pady=(4, 0))

        if is_password:
            entry.config(show="*")
        elif placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=GRAY)
            entry.bind(
                "<FocusIn>",
                lambda _event: (
                    entry.delete(0, "end"),
                    entry.config(fg=DARK),
                )
                if entry.get() == placeholder
                else None,
            )

        return entry

    ent_email = make_input("Email Address", placeholder="name@example.com")
    ent_pass = make_input("Password", is_password=True)

    error_v = tk.StringVar(value="")
    tk.Label(
        inner,
        textvariable=error_v,
        bg=WHITE,
        fg="#DB5C5C",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w")

    def submit_login():
        email = ent_email.get().strip()
        password = ent_pass.get()

        if not email or not password or email == "name@example.com":
            error_v.set("Please enter your credentials.")
            return

        try:
            login_result = UserController.handle_login(email=email, password=password)
        except ValidationError as exc:
            error_v.set(str(exc))
            return

        user = login_result.user
        if not user:
            error_v.set("Invalid email or password.")
            return

        role = user["role"]
        if role == "admin" and app:
            app.show_admin_admin_dashboard(admin_id=user["id"])
        elif role == "user" and app:
            app.show_user_dashboard(user_id=user["id"])

    tk.Button(
        inner,
        text="Sign In",
        command=submit_login,
        bg=BLUE,
        fg=WHITE,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        borderwidth=0,
    ).pack(fill="x", ipady=12, pady=(10, 0))
    tk.Button(
        inner,
        text="Don't have an account? Sign up",
        bg=WHITE,
        fg=BLUE,
        font=("Segoe UI", 10),
        borderwidth=0,
        cursor="hand2",
        command=lambda: app.show_signup("user") if app else None,
    ).pack(pady=16)
