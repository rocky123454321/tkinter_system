import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database_config import get_db_connection


def create_settings(parent, admin_id: int | None = None, app=None):
    """Admin Settings page (profile + password change), similar to user settings."""

    frame = tk.Frame(parent, bg="#f5f5f7")

    title = tk.Label(
        frame,
        text="Admin Settings",
        font=("SF Pro Display", 26, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
        anchor="w",
    )
    title.pack(fill="x", pady=(0, 20))

    if admin_id is None:
        tk.Label(
            frame,
            text="Unable to load admin settings.",
            font=("SF Pro Text", 12),
            bg="#f5f5f7",
            fg="#86868b",
            pady=20,
        ).pack(anchor="w")
        frame.pack(fill="both", expand=True)
        return frame

    # ── Data helpers ─────────────────────────────────────────
    def fetch_admin_by_id(uid: int):
        conn = get_db_connection()
        if conn is None:
            return None
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT first_name, last_name, email, phone, role FROM users WHERE id = ? AND role='admin'",
                (uid,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_admin_profile(uid: int, first_name: str, last_name: str, phone: str):
        conn = get_db_connection()
        if conn is None:
            return False
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET first_name = ?, last_name = ?, phone = ? WHERE id = ? AND role='admin'",
                (first_name, last_name, phone, uid),
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def change_admin_password(uid: int, current_password: str, new_password: str):
        conn = get_db_connection()
        if conn is None:
            return False, "Database error"
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT password FROM users WHERE id = ? AND role='admin'",
                (uid,),
            )
            row = cur.fetchone()
            if not row:
                return False, "Admin not found"
            if row[0] != current_password:
                return False, "Current password is incorrect"

            cur.execute(
                "UPDATE users SET password = ? WHERE id = ? AND role='admin'",
                (new_password, uid),
            )
            conn.commit()
            return cur.rowcount > 0, ""
        finally:
            conn.close()

    admin_data = fetch_admin_by_id(admin_id)
    if not admin_data:
        tk.Label(frame, text="Admin not found.", bg="#f5f5f7", fg="#86868b").pack(anchor="w", pady=10)
        frame.pack(fill="both", expand=True)
        return frame

    # ── Card ────────────────────────────────────────────────
    card = tk.Frame(frame, bg="#ffffff", highlightthickness=1, highlightbackground="#d2d2d7")
    card.pack(fill="both", expand=True)

    body = tk.Frame(card, bg="#ffffff")
    body.pack(fill="both", expand=True, padx=20, pady=20)

    left = tk.Frame(body, bg="#ffffff")
    left.pack(side=tk.LEFT, fill=tk.Y)

    right = tk.Frame(body, bg="#ffffff")
    right.pack(side=tk.LEFT, fill="both", expand=True, padx=(20, 0))

    # ── Profile image (read-only) ──────────────────────────
    profile_path = PROJECT_ROOT / "assets" / "adminProfile.png"
    try:
        from PIL import Image, ImageTk

        img = Image.open(profile_path).resize((90, 90))
        tk_img = ImageTk.PhotoImage(img)
        pic_label = tk.Label(left, image=tk_img, bg="#ffffff")
        pic_label.image = tk_img
        pic_label.pack(anchor="w")
    except Exception:
        tk.Label(left, text="Admin Profile", bg="#ffffff", fg="#86868b").pack(anchor="w")

    tk.Label(left, text="Profile picture", bg="#ffffff", fg="#86868b", font=("SF Pro Text", 10)).pack(
        anchor="w", pady=(10, 0)
    )
    
    # ── Field helper ────────────────────────────────────────
    def add_field(parent_frame, label, var, is_password=False):
        row = tk.Frame(parent_frame, bg="#ffffff")
        row.pack(fill="x", pady=8)
        tk.Label(
            row,
            text=label,
            bg="#ffffff",
            fg="#86868b",
            font=("SF Pro Text", 10, "bold"),
        ).pack(anchor="w")
        entry = tk.Entry(
            row,
            textvariable=var,
            font=("SF Pro Text", 11),
            bg="#f5f5f7",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#0071e3",
            width=30,
            show="●" if is_password else "",
        )
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        return entry

    # ── Profile editor ─────────────────────────────────────
    profile_section = tk.Frame(right, bg="#ffffff")
    profile_section.pack(fill="x")

    tk.Label(
        profile_section,
        text="Profile",
        bg="#ffffff",
        fg="#1d1d1f",
        font=("SF Pro Display", 16, "bold"),
    ).pack(anchor="w", pady=(0, 10))

    fn_var = tk.StringVar(value=admin_data.get("first_name") or "")
    ln_var = tk.StringVar(value=admin_data.get("last_name") or "")
    phone_var = tk.StringVar(value=admin_data.get("phone") or "")
    email_var = tk.StringVar(value=admin_data.get("email") or "")

    email_row = tk.Frame(profile_section, bg="#ffffff")
    email_row.pack(fill="x", pady=8)
    tk.Label(email_row, text="Email", bg="#ffffff", fg="#86868b", font=("SF Pro Text", 10, "bold")).pack(
        anchor="w"
    )
    email_entry = tk.Entry(
        email_row,
        textvariable=email_var,
        state="disabled",
        font=("SF Pro Text", 11),
        bg="#f5f5f7",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#d2d2d7",
        width=30,
    )
    email_entry.pack(fill="x", ipady=6, pady=(4, 0))

    add_field(profile_section, "First name", fn_var)
    add_field(profile_section, "Last name", ln_var)
    add_field(profile_section, "Phone", phone_var)

    def on_save_profile():
        first = fn_var.get().strip()
        last = ln_var.get().strip()
        phone = phone_var.get().strip()

        if not first or not last:
            messagebox.showerror("Error", "First name and last name are required.")
            return

        if update_admin_profile(admin_id, first, last, phone):
            messagebox.showinfo("Saved", "Profile updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update profile.")

    tk.Button(
        profile_section,
        text="Save profile",
        bg="#0071e3",
        fg="white",
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        font=("SF Pro Text", 11, "bold"),
        command=on_save_profile,
    ).pack(fill="x", pady=(10, 0))

    # ── Password change ──────────────────────────────────
    pw_section = tk.Frame(right, bg="#ffffff")
    pw_section.pack(fill="x", pady=(20, 0))

    tk.Label(
        pw_section,
        text="Password",
        bg="#ffffff",
        fg="#1d1d1f",
        font=("SF Pro Display", 16, "bold"),
    ).pack(anchor="w", pady=(0, 10))

    cur_pw_var = tk.StringVar(value="")
    new_pw_var = tk.StringVar(value="")
    confirm_pw_var = tk.StringVar(value="")

    add_field(pw_section, "Current password", cur_pw_var, is_password=True)
    add_field(pw_section, "New password", new_pw_var, is_password=True)
    add_field(pw_section, "Confirm new password", confirm_pw_var, is_password=True)

    def on_change_password():
        cur_pw = cur_pw_var.get()
        new_pw = new_pw_var.get()
        conf_pw = confirm_pw_var.get()

        if not cur_pw or not new_pw or not conf_pw:
            messagebox.showerror("Error", "All password fields are required.")
            return
        if new_pw != conf_pw:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        if len(new_pw) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters.")
            return

        ok, err = change_admin_password(admin_id, cur_pw, new_pw)
        if ok:
            messagebox.showinfo("Success", "Password changed successfully.")
            cur_pw_var.set("")
            new_pw_var.set("")
            confirm_pw_var.set("")
        else:
            messagebox.showerror("Error", err or "Failed to change password.")

    tk.Button(
        pw_section,
        text="Change password",
        bg="#1d1d1f",
        fg="white",
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        font=("SF Pro Text", 11, "bold"),
        command=on_change_password,
    ).pack(fill="x", pady=(10, 0))

    frame.pack(fill="both", expand=True)
    return frame

