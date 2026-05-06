import tkinter as tk

from views.components.topnav import create_topnav
from views.components.sidebar import create_sidebar
from views.pages.dashboard import create_dashboard
from views.pages.rooms import create_rooms
window = tk.Tk()
window.title("Tkinter System")
window.geometry("1350x800")

def handle_navigation(page_name):

    for wid in content_Area.winfo_children():
        wid.destroy()

    print(f"Navigating to {page_name}")
    if page_name == "Dashboard":
        create_dashboard(content_Area)
    elif page_name == "Reservation":
        print("Reservation page clicked")
    elif page_name == "Rooms":
        create_rooms(content_Area)
    elif page_name == "Guest":
        print("Guest page clicked")
    elif page_name == "New bookings":
        print("New bookings page clicked")
    elif page_name == "Settings":
        print("Settings page clicked")
    else:
        print("Unknown page")




create_sidebar(window , handle_navigation)
right_con = tk.Frame(window)

right_con.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
create_topnav(right_con)


content_Area = tk.Frame(right_con, bg="#f5f5f7")
content_Area.pack(fill=tk.BOTH, side=tk.TOP ,expand=True)


handle_navigation("Dashboard")
#ito yung dashbord

window.mainloop()