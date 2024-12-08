from User.userinterface import UserInterface
from User.librarian_module.managelibrarybook import ManageLibraryBooks
from User.librarian_module.manageloan import ManageLoanProposals
from User.librarian_module.managelibrarian import ManageLibrarian


class Librarian(UserInterface):
    def __init__(self, cursor, usercode, libCode):
        self.Manage_Books = ManageLibraryBooks(cursor, libCode)
        self.Manage_Loans = ManageLoanProposals(cursor, libCode)
        self.Manage_Librarian = ManageLibrarian(cursor, usercode, libCode)
        self.libCode = libCode  # 도서관 코드

    def get_menu(self):
        while True:
            print("\n--- Librarian Menu ---")
            print('1. Manage Books')
            print('2. Manage Loans')
            print('3. Manage Information')
            print('4. Exit')

            choice = int(input("Select an option (1-4): "))

            if choice == 1:
                self.Manage_Books.manage_library_books()  # 장서 관리 기능 호출
            elif choice == 2:
                self.Manage_Loans.manage_loan_proposals()  # 대출 관리 기능 호출
            elif choice == 3:
                self.Manage_Librarian.manage_librarian()  # 대출 관리 기능 호출
            elif choice == 4:
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")
