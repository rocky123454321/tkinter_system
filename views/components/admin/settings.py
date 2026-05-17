import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from controllers.user_controller import UserController
from utils import ValidationError
from utils.ui_constants import (
    BG_PAGE,
    BG_CARD,
    TEXT_SUB,
    TEXT_MAIN,
    BORDER,
    ACCENT,
    PRIMARY_BUTTON_STYLE,
    ENTRY_STYLE,
    PAGE_TITLE_FONT,
    PAGE_TITLE_FG,
    SECTION_TITLE_FONT,
)


def create_settings(parent, admin_id: int | None = None, app=None):
    """Admin Settings page.

    Goal: make Admin Settings UI content/structure match User Settings UI content,
    while keeping admin-specific handlers/role.
    """

    from utils.ui_constants import (
        COLORS,
        CARD_PADX,
        CARD_PADY,
        TITLE_PADY,
        BODY_FONT,
        LABEL_FONT,
        LABEL_FG,
        SUBTEXT_FONT,
        SUBTEXT_FG,
        PAGE_TITLE_FONT,
        PAGE_TITLE_FG,
        PAGE_TITLE_BG,
        SECTION_TITLE_FONT,
        SECTION_TITLE_FG,
    )

    project_root = Path(__file__).resolve().parents[3]

    frame = tk.Frame(parent, bg=COLORS["bg"])

    tk.Label(
        frame,
        text="Settings",
        font=PAGE_TITLE_FONT,
        bg=COLORS["bg"],
        fg=PAGE_TITLE_FG,
        anchor="w",
    ).pack(fill="x", pady=TITLE_PADY)

    if admin_id is None:
        tk.Label(
            frame,
            text="Unable to load admin settings.",
            font=BODY_FONT,
            bg=COLORS["bg"],
            fg=COLORS["text_sub"],
            pady=20,
        ).pack(anchor="w")
        frame.pack(fill="both", expand=True)
        return frame

    if not UserController.handle_get_profile(user_id=admin_id, role="admin"):
        tk.Label(
            frame,
            text="Admin not found.",
            font=BODY_FONT,
            bg=COLORS["bg"],
            fg=COLORS["text_sub"],
            pady=10,
        ).pack(anchor="w")
        frame.pack(fill="both", expand=True)
        return frame

    card = tk.Frame(
        frame,
        bg=COLORS["card"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
    )
    card.pack(fill="both", expand=True)

    body = tk.Frame(card, bg=COLORS["card"])
    body.pack(fill="both", expand=True, padx=CARD_PADX, pady=CARD_PADY)

    left = tk.Frame(body, bg=COLORS["card"])
    left.pack(side=tk.LEFT, fill=tk.Y)

    right = tk.Frame(body, bg=COLORS["card"])
    right.pack(side=tk.LEFT, fill="both", expand=True, padx=(20, 0))

    profile_path = project_root / "assets" / "adminProfile.png"
    try:
        from PIL import Image, ImageTk

        img = Image.open(profile_path).resize((90, 90))
        tk_img = ImageTk.PhotoImage(img)
        pic_label = tk.Label(left, image=tk_img, bg=COLORS["card"])
        pic_label.image = tk_img
        pic_label.pack(anchor="w")
    except (ImportError, OSError, tk.TclError):
        tk.Label(left, text="Admin Profile", bg=COLORS["card"], fg=COLORS["text_sub"]).pack(anchor="w")

    tk.Label(
        left,
        text="Profile picture",
        bg=COLORS["card"],
        fg=COLORS["text_sub"],
        font=SUBTEXT_FONT,
    ).pack(anchor="w", pady=(10, 0))

    admin_data = UserController.handle_get_profile(user_id=admin_id, role="admin") or {}

    def add_field(parent_frame, label, var, is_password=False, state="normal"):
        row = tk.Frame(parent_frame, bg=COLORS["card"])
        row.pack(fill="x", pady=8)
        tk.Label(
            row,
            text=label,
            bg=COLORS["card"],
            fg=LABEL_FG,
            font=LABEL_FONT,
        ).pack(anchor="w")
        entry = tk.Entry(
            row,
            textvariable=var,
            state=state,
            font=BODY_FONT,
            bg=COLORS["bg"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            width=30,
            show="*" if is_password else "",
        )
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        return entry

    email_var = tk.StringVar(value=admin_data.get("email") or "")
    fn_var = tk.StringVar(value=admin_data.get("first_name") or "")
    ln_var = tk.StringVar(value=admin_data.get("last_name") or "")
    phone_var = tk.StringVar(value=admin_data.get("phone") or "")

    # ── Profile section ──────────────────────────────────────────────────────
    profile_section = tk.Frame(right, bg=COLORS["card"])
    profile_section.pack(fill="x")

    tk.Label(
        profile_section,
        text="Profile",
        bg=COLORS["card"],
        fg=SECTION_TITLE_FG,
        font=SECTION_TITLE_FONT,
        anchor="w",
    ).pack(anchor="w", pady=(0, 10))

    add_field(profile_section, "EMAIL", email_var, state="disabled")
    add_field(profile_section, "FIRST NAME", fn_var)
    add_field(profile_section, "LAST NAME", ln_var)
    add_field(profile_section, "PHONE", phone_var)

    def on_save_profile():
        try:
            ok = UserController.handle_update_profile(
                user_id=admin_id,
                first_name=fn_var.get().strip(),
                last_name=ln_var.get().strip(),
                phone=phone_var.get().strip(),
                role="admin",
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
        bg=COLORS["accent"],
        fg="white",
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        font=("SF Pro Text", 11, "bold"),
        command=on_save_profile,
    ).pack(fill="x", ipady=12, pady=(10, 0))

    # ── Password section ─────────────────────────────────────────────────────
    pw_section = tk.Frame(right, bg=COLORS["card"])
    pw_section.pack(fill="x", pady=(20, 0))

    tk.Label(
        pw_section,
        text="Password",
        bg=COLORS["card"],
        fg=SECTION_TITLE_FG,
        font=SECTION_TITLE_FONT,
        anchor="w",
    ).pack(anchor="w", pady=(0, 10))

    cur_pw_var = tk.StringVar(value="")
    new_pw_var = tk.StringVar(value="")
    confirm_pw_var = tk.StringVar(value="")

    add_field(pw_section, "CURRENT PASSWORD", cur_pw_var, is_password=True)
    add_field(pw_section, "NEW PASSWORD", new_pw_var, is_password=True)
    add_field(pw_section, "CONFIRM NEW PASSWORD", confirm_pw_var, is_password=True)

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
                user_id=admin_id,
                current_password=cur_pw,
                new_password=new_pw,
                role="admin",
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
        bg=COLORS["text_main"],
        fg="white",
        relief="flat",
        cursor="hand2",
        borderwidth=0,
        font=("SF Pro Text", 11, "bold"),
        command=on_change_password,
    ).pack(fill="x", ipady=12, pady=(10, 0))

    frame.pack(fill="both", expand=True)
    return frame


