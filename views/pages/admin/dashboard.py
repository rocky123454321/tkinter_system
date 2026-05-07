import tkinter as tk
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from views.components.admin.home import create_home
from views.components.admin.rooms import create_rooms
from views.components.admin.reservation import create_reservation
from views.components.admin.Guest import create_guest
from views.components.sidebar import create_sidebar
from views.components.topnav import create_topnav

COLORS = {
    "bg": "#f5f5f7",
    "white": "#ffffff",
    "text_dark": "#202124",
    "border": "#e1e1e1"
}

def create_dashboard(root, on_navigate=None):
    if on_navigate is None:
        on_navigate = lambda page: None

    wrapper = tk.Frame(root, bg=COLORS["bg"])
    wrapper.pack(fill="both", expand=True)

    main_container = tk.Frame(wrapper, bg=COLORS["bg"])
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def handle_navigation(page_name):
        clear_content()
        pages = {
            "Home": lambda: create_home(content_area),
            "Rooms": lambda: create_rooms(content_area),
            "Reservation": lambda: create_reservation(content_area),
            "Guest": lambda: create_guest(content_area)
        }
        page_function = pages.get(page_name, pages["Home"])
        page_function()

    create_sidebar(main_container, handle_navigation)
    create_topnav(main_container)
    content_area = tk.Frame(main_container, bg=COLORS["bg"])
    content_area.pack(side="left", fill="both", expand=True)

   

    handle_navigation("Home")

if __name__ == "__main__":
    app_root = tk.Tk()
    app_root.geometry("1100x720")
    app_root.title("RockStay Admin Panel")
    create_dashboard(app_root)
    app_root.mainloop()