import psycopg2

class ManageLibraryBooks:
    def __init__(self, cursor, libcode):
        self.cursor = cursor
        self.libCode = libcode  # 도서관 코드

    def manage_library_books(self):
        while True:
            print("\n--- Library Books Management ---")
            print("1. Add Book to Library")
            print("2. View Library Books")
            print("3. Update Library Book")
            print("4. Delete Library Book")
            print("5. Back to Main Menu")

            choice = int(input("Select an option (1-5): "))

            if choice == 1:
                self.add_book_to_library()
            elif choice == 2:
                self.view_library_books()
            elif choice == 3:
                self.update_library_book()
            elif choice == 4:
                self.delete_library_book()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    def add_book_to_library(self):
        book_data = self.get_book_data_defaults()
        self.input_book_data(book_data)

        # 유효성 검사
        if not self.validate_book_data(book_data):
            print("Book addition failed due to invalid data.")
            return

        # 데이터베이스에 책 정보 등록
        self.cursor.execute('''
        INSERT INTO LibraryBooks (LibCode, ISBN, Vol, CallNumber, RegistrationDate, ISLoan)
        VALUES (%s, %s, %s, %s, CURRENT_DATE, %s)
        ''', (self.libCode, book_data['ISBN'], book_data['Vol'], book_data['CallNumber'], False))

        print(f"Book '{book_data['ISBN']}' added to library successfully.")
        self.cursor.connection.commit()

    def view_library_books(self):
        self.cursor.execute("SELECT * FROM LibraryBooks WHERE LibCode = %s", (self.libCode,))
        library_books = self.cursor.fetchall()

        print("\n--- Library Books ---")
        for book in library_books:
            print(f"LibCode: {book[0]}, ISBN: {book[1]}, Volume: {book[2]}, Call Number: {book[3]}, Registration Date: {book[4]}, Is Loaned: {book[5]}")

    def update_library_book(self):
        library_books = self.get_all_library_books()
        if not library_books:
            print("No books available to update.")
            return

        self.display_all_library_books(library_books)
        isbn_to_update = input("Enter the ISBN of the book you want to update: ")
        selected_book = self.get_book_by_isbn(library_books, isbn_to_update)

        if not selected_book:
            print(f"Error: Book with ISBN {isbn_to_update} does not exist in this library.")
            return

        book_data = self.get_book_data_from_selected(selected_book)
        self.input_book_data(book_data, is_update=True)

        # 유효성 검사
        if not self.validate_book_data(book_data):
            print("Book update failed due to invalid data.")
            return

        # 데이터베이스에 책 정보 업데이트
        self.cursor.execute('''
        UPDATE LibraryBooks
        SET Vol = %s, CallNumber = %s
        WHERE LibCode = %s AND ISBN = %s
        ''', (book_data['Vol'], book_data['CallNumber'], self.libCode, book_data['ISBN']))

        print(f"Book with ISBN {isbn_to_update} updated successfully.")
        self.cursor.connection.commit()

    def delete_library_book(self):
        library_books = self.get_all_library_books()
        if not library_books:
            print("No books available to delete.")
            return

        self.display_all_library_books(library_books)
        isbn_to_delete = input("Enter the ISBN of the book you want to delete: ")
        selected_book = self.get_book_by_isbn(library_books, isbn_to_delete)

        if not selected_book:
            print(f"Error: Book with ISBN {isbn_to_delete} does not exist in this library.")
            return

        confirm = input(
            f"Are you sure you want to delete the book with ISBN '{selected_book[1]}'? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Book deletion canceled.")
            return

        self.cursor.execute('''
        DELETE FROM LibraryBooks
        WHERE LibCode = %s AND ISBN = %s
        ''', (self.libCode, isbn_to_delete))

        print(f"Book with ISBN {isbn_to_delete} deleted successfully.")
        self.cursor.connection.commit()

    def get_all_library_books(self):
        self.cursor.execute("SELECT LibCode, ISBN, Vol, CallNumber FROM LibraryBooks WHERE LibCode = %s", (self.libCode,))
        return self.cursor.fetchall()

    def display_all_library_books(self, books):
        print("\n--- Library Books ---")
        for book in books:
            print(f"LibCode: {book[0]}, ISBN: {book[1]}, Volume: {book[2]}, Call Number: {book[3]}")

    def get_book_data_defaults(self):
        return {
            'ISBN': '',
            'Vol': '',
            'CallNumber': ''
        }

    def input_book_data(self, book_data, is_update=False):
        self.display_book_data(book_data)  # 현재 책 정보를 먼저 출력

        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1: ISBN")
            print("2: Volume")
            print("3: Call Number")
            print("4: Confirm and Add/Update Book")
            print("5: Cancel")

            choice = input("Select an option (1-5): ")

            if choice == '1':
                book_data['ISBN'] = input("Enter ISBN (13 characters): ")
            elif choice == '2':
                book_data['Vol'] = input("Enter volume (if applicable): ")
            elif choice == '3':
                book_data['CallNumber'] = input("Enter call number: ")
            elif choice == '4':
                break
            elif choice == '5':
                print("Book addition/update canceled.")
                return
            else:
                print("Invalid choice. Please try again.")

            # 현재 설정된 값을 다시 출력
            self.display_book_data(book_data)

    def display_book_data(self, book_data):
        print("\n--- Current Book Details ---")
        for key, value in book_data.items():
            print(f"{key}: {value}")

    def get_book_by_isbn(self, books, isbn):
        return next((book for book in books if book[1] == isbn), None)

    def validate_book_data(self, book_data):
        # ISBN 유효성 검사
        if not book_data['ISBN'] or len(book_data['ISBN']) != 13:
            print("Error: ISBN must be 13 characters long.")
            return False

        # ISBN이 Books 테이블에 존재하는지 확인
        self.cursor.execute("SELECT * FROM Books WHERE ISBN = %s", (book_data['ISBN'],))
        if self.cursor.fetchone() is None:
            print("Error: The ISBN does not exist in the Books table.")
            return False

        return True

    def get_book_data_from_selected(self, selected_book):
        return {
            'ISBN': selected_book[1],  # ISBN은 두 번째 인덱스
            'Vol': selected_book[2],  # Vol은 세 번째 인덱스
            'CallNumber': selected_book[3]  # CallNumber는 네 번째 인덱스
        }