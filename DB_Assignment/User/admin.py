
from User.userinterface import UserInterface
from User.admin_module.manageuser import ManageUser
from User.admin_module.managebook import ManageBooks
from User.admin_module.managelibrary import ManageLibraries

class Admin(UserInterface):
    def __init__(self, cursor):
        self.Manage_User = ManageUser(cursor)
        self.Manage_Books = ManageBooks(cursor)
        self.Manage_Libraries = ManageLibraries(cursor)

    def get_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print('1. Manage User: ')
            print('2. Manage Libraries: ')
            print('3. Manage Books: ')
            print('4. Exit')

            choice = int(input("Select an option (1-4): "))

            if choice == 1:
                self.Manage_User.manage_user()
            elif choice == 2:
                self.Manage_Libraries.manage_libraries()
            elif choice == 3:
                self.Manage_Books.manage_books()
            elif choice == 4:
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")
