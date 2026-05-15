import tkinter as tk

from  views.components.admin.Guest import create_guest
from  views.components.admin.billing import create_billing
from  views.components.admin.checkin_checkout import create_checkin_checkout
from  views.components.admin.home import create_home
from  views.components.admin.reports import create_reports
from  views.components.admin.reservation import create_reservation
from  views.components.admin.rooms import create_rooms
from  views.components.admin.settings import create_settings
from  views.components.sidebar import create_sidebar
from  views.components.topnav import create_topnav


COLORS = {
    "bg": "#f5f5f7",
    "white": "#ffffff",
    "text_dark": "#1d1d1f",
    "border": "#d2d2d7",
}


def create_admin_dashboard(root, admin_id: int, on_navigate=None):
    if on_navigate is None:
        on_navigate = lambda *_: None

    wrapper = tk.Frame(root, bg=COLORS["bg"])
    wrapper.pack(fill="both", expand=True)

    sidebar_container = tk.Frame(wrapper, bg=COLORS["white"], width=250)
    sidebar_container.pack(side="left", fill="y")
    sidebar_container.pack_propagate(False)

    right_side_container = tk.Frame(wrapper, bg=COLORS["bg"])
    right_side_container.pack(side="left", fill="both", expand=True)
    create_topnav(right_side_container, logout_callback=lambda: on_navigate("Logout"))

    content_area = tk.Frame(right_side_container, bg=COLORS["bg"])
    content_area.pack(fill="both", expand=True, padx=40, pady=30)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def handle_navigation(page_name):
        clear_content()
        pages = {
            "Home": lambda: create_home(content_area),
            "Rooms": lambda: create_rooms(content_area),
            "Booking": lambda: create_reservation(content_area),
            "Check-in/Out": lambda: create_checkin_checkout(content_area),
            "Billing": lambda: create_billing(content_area),
            "Reports": lambda: create_reports(content_area),
            "Guest": lambda: create_guest(content_area),
            "Settings": lambda: create_settings(content_area, admin_id=admin_id),
        }

        page_function = pages.get(page_name)
        if page_function:
            page_function()
            return

        fallback_frame = tk.Frame(content_area, bg=COLORS["bg"])
        fallback_frame.place(relx=0.5, rely=0.5, anchor="center")
        from utils.ui_constants import PAGE_TITLE_FONT, PAGE_TITLE_FG

        tk.Label(
            fallback_frame,
            text=page_name,
            font=PAGE_TITLE_FONT,
            bg=COLORS["bg"],
            fg=PAGE_TITLE_FG,
            anchor="w",
        ).pack()

        tk.Label(
            fallback_frame,
            text="Module not found or under construction.",
            font=("SF Pro Text", 12),
            bg=COLORS["bg"],
            fg="#86868b",
            pady=10,
        ).pack()

    create_sidebar(sidebar_container, on_click_button=handle_navigation)
    handle_navigation("Home")


if __name__ == "__main__":
    app_root = tk.Tk()
    app_root.geometry("1280x800")
    app_root.title("RockStay Admin Panel")

    try:
        app_root.option_add("*Font", ("SF Pro Text", 10))
    except tk.TclError:
        app_root.option_add("*Font", ("Segoe UI", 10))

    app_root.configure(bg=COLORS["bg"])
    create_admin_dashboard(app_root, admin_id=1)
    app_root.mainloop()
