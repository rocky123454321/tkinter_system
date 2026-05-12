import tkinter as tk


from views.pages.authentication.login  import create_login
from views.pages.authentication.signup import create_signup
from views.pages.admin.admin_dashboard  import create_admin_dashboard
from views.pages.user.user_dashboard import create_user_dashboard
from models.user_model                 import UserModel
from models.RoomModel import RoomModel
from models.RentalModel import RentalModel


class HotelApp:
   
    def __init__(self, root):
        self.root = root

        UserModel.create_user_table()
        UserModel.ensure_admin_user(email="admin@temp.com", password="admin123", first_name="Admin", last_name="Temp", phone="")

        RoomModel.create_room_table()
        RentalModel.create_rentals_table()
        RoomModel.seed_rooms()


        # container
        self.container = tk.Frame(self.root, bg="#f5f5f7")
        self.container.pack(fill="both", expand=True)

        #starting page ay login
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
            else:
                print(f"App level navigation to: {page_name}")

        create_admin_dashboard(self.container, admin_id=admin_id, on_navigate=handle_app_navigation)


    def show_user_dashboard(self, user_id: int):
        self.clear_screen()

        def handle_navigation(pagename):
            if pagename == 'logout':
                self.show_login()
            else:
                print(f"App level navigation to: {page_name}")



        create_user_dashboard(self.container, user_id=user_id, app=self)



def main():
    root = tk.Tk()
    root.title("RockStay - Hotel Management System")
    root.geometry("2300x1120")
    root.configure(bg="#f5f5f7")
    HotelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()