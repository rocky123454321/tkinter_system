import tkinter as tk

# Inayos ang spelling mula 'authentecation' tungo sa 'authentication'
# Siguraduhin na ang folder name mo ay tama rin ang spelling
from views.pages.authentication.login  import create_login
from views.pages.authentication.signup import create_signup
from views.pages.admin.dashboard       import create_dashboard
from models.user_model                 import UserModel

class HotelApp:
   
    def __init__(self, root):
        self.root = root

        UserModel.create_user_table()

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

    def show_signup(self):
        self.clear_screen()
        create_signup(self.container, app=self)

    def show_admin_dashboard(self):
        self.clear_screen()
        def handle_app_navigation(page_name):
            if page_name == "Logout":
                self.show_login()
            else:
                print(f"App level navigation to: {page_name}")
                
        #dashboard
        create_dashboard(self.container, on_navigate=handle_app_navigation)

def main():
    root = tk.Tk()
    root.title("RockStay - Hotel Management System")
    

    root.geometry("1100x720")
    root.configure(bg="#f5f5f7")

    # Simulan ang class
    HotelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()