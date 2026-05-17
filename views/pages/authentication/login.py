import tkinter as tk

from controllers.user_controller import UserController
from utils import ValidationError
from utils.ui_constants import (
    BG_PAGE, BG_CARD, TEXT_MAIN, TEXT_SUB, BORDER, ACCENT, DANGER,
    LABEL_FONT, PRIMARY_FONT, SUBTEXT_FONT,
    PRIMARY_BUTTON_STYLE, ENTRY_STYLE,
    PAGE_PADX, PAGE_PADY,
)


def create_login(root, app=None):
    container = tk.Frame(root, bg=BG_PAGE)
    container.pack(fill="both", expand=True)

    card = tk.Frame(container, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=BG_CARD, width=400)
    inner.pack(padx=PAGE_PADX + 10, pady=PAGE_PADY + 30)

    tk.Label(
        inner,
        text="Sign In",
        bg=BG_CARD,
        fg=TEXT_MAIN,
        font=("SF Pro Display", 22, "bold"),
    ).pack(pady=(0, 5))

    tk.Label(
        inner,
        text="Enter your email and password.",
        bg=BG_CARD,
        fg=TEXT_SUB,
        font=("SF Pro Text", 10),
    ).pack(pady=(0, 30))

    def make_input(label_text, placeholder="", is_password=False):
        frame = tk.Frame(inner, bg=BG_CARD)
        frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            frame,
            text=label_text.upper(),
            bg=BG_CARD,
            fg=TEXT_SUB,
            font=LABEL_FONT,
        ).pack(anchor="w")

        entry = tk.Entry(frame, width=37, **ENTRY_STYLE)
        entry.pack(fill="x", ipady=10, pady=(4, 0))

        if is_password:
            entry.config(show="*")
        elif placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=TEXT_SUB)
            entry.bind(
                "<FocusIn>",
                lambda _event: (
                    entry.delete(0, "end"),
                    entry.config(fg=TEXT_MAIN),
                )
                if entry.get() == placeholder
                else None,
            )

        return entry

    ent_email = make_input("Email Address", placeholder="name@example.com")
    ent_pass  = make_input("Password", is_password=True)

    error_v = tk.StringVar(value="")
    tk.Label(
        inner,
        textvariable=error_v,
        bg=BG_CARD,
        fg=DANGER,
        font=("SF Pro Text", 9, "bold"),
    ).pack(anchor="w")

    def submit_login():
        email    = ent_email.get().strip()
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

        error_v.set("")
        role = user["role"]
        if role == "admin" and app:
            app.show_admin_admin_dashboard(admin_id=user["id"])
        elif role == "user" and app:
            app.show_user_dashboard(user_id=user["id"])

    tk.Button(
        inner,
        text="Sign In",
        command=submit_login,
        **PRIMARY_BUTTON_STYLE,
    ).pack(fill="x", ipady=12, pady=(10, 0))

    tk.Button(
        inner,
        text="Don't have an account? Sign up",
        bg=BG_CARD,
        fg=ACCENT,
        font=("SF Pro Text", 10),
        borderwidth=0,
        cursor="hand2",
        command=lambda: app.show_signup("user") if app else None,
    ).pack(pady=16)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    root.title("Sign In")
    create_login(root)
    root.mainloop()