import tkinter as tk

from controllers.rental_controller import RentalController
from controllers.room_controller import RoomController
from controllers.user_controller import UserController
from views.pages.admin.admin_dashboard import create_admin_dashboard
from views.pages.authentication.login import create_login
from views.pages.authentication.signup import create_signup
from views.pages.user.user_dashboard import create_user_dashboard


class HotelApp:
    def __init__(self, root):
        self.root = root

        UserController.initialize_users(
            admin_email="admin@gmail.com",
            admin_password="admin123",
            first_name="Admin",
            last_name="Temp",
            phone="",
        )
        RoomController.initialize_room_table()
        RentalController.initialize_rentals_table()
        RoomController.seed_default_rooms()

        self.container = tk.Frame(self.root, bg="#f5f5f7")
        self.container.pack(fill="both", expand=True)
        self.show_login()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        create_login(self.container, app=self)

    def show_signup(self, role_choice: str = "user"):
        self.clear_screen()
        create_signup(self.container, app=self, preset_role=role_choice)

    def show_admin_admin_dashboard(self, admin_id: int):
        self.clear_screen()

        def handle_app_navigation(page_name):
            if page_name == "Logout":
                self.show_login()

        create_admin_dashboard(self.container, admin_id=admin_id, on_navigate=handle_app_navigation)

    def show_user_dashboard(self, user_id: int):
        self.clear_screen()
        create_user_dashboard(self.container, user_id=user_id, app=self)


def main():
    root = tk.Tk()
    root.title("RockStay - Hotel Management System")
    root.state("zoomed")
    root.configure(bg="#f5f5f7")
    HotelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
