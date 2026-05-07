# login.py — Login page ng application

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.user_model import UserModel


# ── Colors ────────────────────────────────────────────────────────
BG         = "#f5f5f7"
WHITE      = "#ffffff"
BLUE       = "#0071e3"
GRAY       = "#86868b"
DARK       = "#1d1d1f"
BORDER     = "#d2d2d7"


def create_login(root, app=None):

    # ── Outer container ───────────────────────────────────────────
    container = tk.Frame(root, bg=BG)
    container.pack(fill="both", expand=True)

    # ── Login card (nakasentro sa screen) ─────────────────────────
    card = tk.Frame(container, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=WHITE, width=400)
    inner.pack(padx=50, pady=50)

    # ── Title ─────────────────────────────────────────────────────
    tk.Label(inner, text="Sign In", bg=WHITE, fg=DARK,
             font=("Segoe UI", 22, "bold")).pack(pady=(0, 5))
    tk.Label(inner, text="Enter your email and password.",
             bg=WHITE, fg=GRAY, font=("Segoe UI", 10)).pack(pady=(0, 30))

    # ── Input helper ──────────────────────────────────────────────
    def make_input(label_text, placeholder="", is_password=False):
        frame = tk.Frame(inner, bg=WHITE)
        frame.pack(fill="x", pady=(0, 12))

        tk.Label(frame, text=label_text, bg=WHITE, fg=GRAY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        entry = tk.Entry(frame, font=("Segoe UI", 11), bg=BG,
                         relief="flat", width=37, highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=BLUE)
        entry.pack(fill="x", ipady=10, pady=(4, 0))

        if is_password:
            entry.config(show="*")
        elif placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=GRAY)
            entry.bind("<FocusIn>", lambda e: (
                entry.delete(0, "end"), entry.config(fg=DARK)
            ) if entry.get() == placeholder else None)

        return entry

    ent_email = make_input("Email Address", placeholder="name@example.com")
    ent_pass  = make_input("Password", is_password=True)

    # ── Submit logic ──────────────────────────────────────────────
    def submit_login():
        email    = ent_email.get().strip()
        password = ent_pass.get()

        if not email or not password or email == "name@example.com":
            messagebox.showwarning("Input Error", "Please enter your credentials.")
            return

        user = UserModel.verify_user(email, password)

        if user:
            role       = user["role"]
            first_name = user["first_name"]

            if role == "admin" and app:
                app.show_admin_dashboard()
            elif role == "user" and app:
                print(f"Welcome, {first_name}! You have successfully logged in as a user.")
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    # ── Buttons ───────────────────────────────────────────────────
    tk.Button(inner, text="Sign In", command=submit_login,
              bg=BLUE, fg=WHITE, font=("Segoe UI", 11, "bold"),
              relief="flat", cursor="hand2", borderwidth=0
              ).pack(fill="x", ipady=12, pady=(10, 0))

    tk.Button(inner, text="Don't have an account? Sign up",
              bg=WHITE, fg=BLUE, font=("Segoe UI", 10),
              borderwidth=0, cursor="hand2",
              command=lambda: app.show_signup() if app else None
              ).pack(pady=16)


