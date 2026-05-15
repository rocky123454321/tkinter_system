import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from controllers.user_controller import UserController
from exceptions import ValidationError


def create_user_settings(parent, user_id: int | None = None, app=None):
    """User-side Settings page."""

    project_root = Path(__file__).resolve().parents[3]

    frame = tk.Frame(parent, bg="#f5f5f7")

    title = tk.Label(
        frame,
        text="Settings",
        font=("SF Pro Display", 26, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
        anchor="w",
    )
    title.pack(fill="x", pady=(0, 20))

    if user_id is None:
        tk.Label(
            frame,
            text="Unable to load user settings.",
            font=("SF Pro Text", 12),
            bg="#f5f5f7",
            fg="#86868b",
            pady=20,
        ).pack(anchor="w")
        frame.pack(fill="both", expand=True)
        return frame

    card = tk.Frame(
        frame,
        bg="#ffffff",
        highlightthickness=1,
        highlightbackground="#d2d2d7",
    )
    card.pack(fill="both", expand=True)

    body = tk.Frame(card, bg="#ffffff")
    body.pack(fill="both", expand=True, padx=20, pady=20)

    left = tk.Frame(body, bg="#ffffff")
    left.pack(side=tk.LEFT, fill=tk.Y)

    right = tk.Frame(body, bg="#ffffff")
    right.pack(side=tk.LEFT, fill="both", expand=True, padx=(20, 0))

    profile_path = project_root / "assets" / "userProfile.png"
    try:
        from PIL import Image, ImageTk

        img = Image.open(profile_path).resize((90, 90))
        tk_img = ImageTk.PhotoImage(img)
        pic_label = tk.Label(left, image=tk_img, bg="#ffffff")
        pic_label.image = tk_img
        pic_label.pack(anchor="w")
    except (ImportError, OSError, tk.TclError):
        tk.Label(left, text="User Profile", bg="#ffffff", fg="#86868b").pack(anchor="w")

    tk.Label(
        left,
        text="Profile picture",
        bg="#ffffff",
        fg="#86868b",
        font=("SF Pro Text", 10),
    ).pack(anchor="w", pady=(10, 0))

    user_data = UserController.handle_get_profile(user_id=user_id)
    if not user_data:
        tk.Label(
            right,
            text="User not found.",
            bg="#ffffff",
            fg="#86868b",
            font=("SF Pro Text", 12),
        ).pack(anchor="w")
        frame.pack(fill="both", expand=True)
        return frame

    def add_field(parent_frame, label, var, is_password=False, state="normal"):
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
            state=state,
            font=("SF Pro Text", 11),
            bg="#f5f5f7",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#0071e3",
            width=30,
            show="*" if is_password else "",
        )
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        return entry

    email_var = tk.StringVar(value=user_data.get("email") or "")
    fn_var = tk.StringVar(value=user_data.get("first_name") or "")
    ln_var = tk.StringVar(value=user_data.get("last_name") or "")
    phone_var = tk.StringVar(value=user_data.get("phone") or "")

    profile_section = tk.Frame(right, bg="#ffffff")
    profile_section.pack(fill="x")

    tk.Label(
        profile_section,
        text="Profile",
        bg="#ffffff",
        fg="#1d1d1f",
        font=("SF Pro Display", 16, "bold"),
    ).pack(anchor="w", pady=(0, 10))  # Dinagdag ang anchor="w" para pantay sa kaliwa

    add_field(profile_section, "Email", email_var, state="disabled")
    add_field(profile_section, "First name", fn_var)
    add_field(profile_section, "Last name", ln_var)
    add_field(profile_section, "Phone", phone_var)

    def on_save_profile():
        try:
            ok = UserController.handle_update_profile(
                user_id=user_id,
                first_name=fn_var.get().strip(),
                last_name=ln_var.get().strip(),
                phone=phone_var.get().strip(),
            )
        except ValidationError as exc:
            messagebox.showerror("Error", str(exc))
            return

        if ok:
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

    pw_section = tk.Frame(right, bg="#ffffff")
    pw_section.pack(fill="x", pady=(20, 0))

    tk.Label(
        pw_section,
        text="Password",
        bg="#ffffff",
        fg="#1d1d1f",
        font=("SF Pro Display", 16, "bold"),
    ).pack(anchor="w", pady=(0, 10))  # Dinagdag ang anchor="w" para pantay sa kaliwa

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

        try:
            ok, err = UserController.handle_change_password(
                user_id=user_id,
                current_password=cur_pw,
                new_password=new_pw,
            )
        except ValidationError as exc:
            messagebox.showerror("Error", str(exc))
            return

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