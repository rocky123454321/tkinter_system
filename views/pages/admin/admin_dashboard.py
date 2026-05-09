import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Setup Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import Components
from views.components.admin.home import create_home
from views.components.admin.rooms import create_rooms
from views.components.admin.Guest import create_guest
from views.components.admin.reservation import create_reservation
from views.components.admin.checkin_checkout import create_checkin_checkout
from views.components.admin.billing import create_billing
from views.components.admin.reports import create_reports
from views.components.sidebar import create_sidebar
from views.components.topnav import create_topnav
from views.components.admin.settings import create_settings

# Minimalist Color Palette (Apple Aesthetic)
COLORS = {
    "bg": "#f5f5f7",  # Off-white / Light Gray
    "white": "#ffffff",
    "text_dark": "#1d1d1f",
    "border": "#d2d2d7"
}

def create_admin_dashboard(root, on_navigate=None):
    if on_navigate is None:
        on_navigate = lambda page: None

    # 1. Main Wrapper - Full Screen Container
    wrapper = tk.Frame(root, bg=COLORS["bg"])
    wrapper.pack(fill="both", expand=True)

    # 2. Sidebar Container (Kaliwa)
    # create_sidebar function should pack itself to the left of this wrapper
    sidebar_container = tk.Frame(wrapper, bg=COLORS["white"], width=250)
    sidebar_container.pack(side="left", fill="y")
    sidebar_container.pack_propagate(False) # Prevent shrinking

    # Initializing Sidebar
    create_sidebar(sidebar_container, lambda page: handle_navigation(page))

    # 3. Main Content Area (Kanan: Topnav + Dynamic Content)
    right_side_container = tk.Frame(wrapper, bg=COLORS["bg"])
    right_side_container.pack(side="left", fill="both", expand=True)

    # 4. Top Navigation (Naka-pack sa taas ng right container)
    create_topnav(right_side_container, logout_callback=lambda: on_navigate("Logout") if on_navigate else None)

    # 5. Dynamic Content Area (Dito lumalabas ang mga tables/forms)
    content_area = tk.Frame(right_side_container, bg=COLORS["bg"])
    content_area.pack(fill="both", expand=True, padx=40, pady=30)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def handle_navigation(page_name):
        clear_content()
        print(f"DEBUG: Navigating to -> {page_name}")


        #pangalan dito ay tugma sa text ng buttons sa sidebar.py
        pages = {
            "Home": lambda: create_home(content_area),
            "Rooms": lambda: create_rooms(content_area),
            "Booking": lambda: create_reservation(content_area),
            "Check-in/Out": lambda: create_checkin_checkout(content_area),
            "Billing": lambda: create_billing(content_area),
            "Reports": lambda: create_reports(content_area),
            "Guest" : lambda :create_guest(content_area),
            "Settings":lambda :create_settings(content_area)
        }



        page_function = pages.get(page_name)

        if page_function:
            page_function()
        else:
            fallback_frame = tk.Frame(content_area, bg=COLORS["bg"])
            fallback_frame.place(relx=0.5, rely=0.5, anchor="center")

            tk.Label( fallback_frame,text=f"{page_name}",font=("SF Pro Display", 24, "bold"), bg=COLORS["bg"], fg=COLORS["text_dark"]).pack()
            tk.Label( fallback_frame,text="Module not found or under construction.", font=("SF Pro Text", 12), bg=COLORS["bg"], fg="#86868b", pady=10 ).pack()

    handle_navigation("Home")

if __name__ == "__main__":
    app_root = tk.Tk()
    app_root.geometry("1280x800")
    app_root.title("RockStay Admin Panel")

    try:
        app_root.option_add("*Font", ("SF Pro Text", 10))
    except:
        app_root.option_add("*Font", ("Segoe UI", 10))

    app_root.configure(bg=COLORS["bg"])

    create_admin_dashboard(app_root)

    app_root.mainloop()