import sqlite3

class ManageBooks:
    def __init__(self, cursor):
        self.cursor = cursor

    def manage_books(self):
        while True:
            print("\n--- Book Management ---")
            print("1. Create Book")
            print("2. Read Books")
            print("3. Update Book")
            print("4. Delete Book")
            print("5. Back to Main Menu")

            choice = int(input("Select an option (1-5): "))

            if choice == 1:
                self.create_book()
            elif choice == 2:
                self.read_books()
            elif choice == 3:
                self.update_book()
            elif choice == 4:
                self.delete_book()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    def create_book(self):
        book_data = self.get_book_data_defaults()
        self.input_book_data(book_data)

        # 유효성 검사
        if not self.validate_book_data(book_data):
            print("Book registration failed due to invalid data.")
            return

        # 데이터베이스에 책 정보 등록
        self.cursor.execute('''
        INSERT INTO Books (ISBN, BookName, Authors, Publisher, PublicationYear, ClassNm, ClassNo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_data['ISBN'], book_data['BookName'], book_data['Authors'],
              book_data['Publisher'], book_data['PublicationYear'],
              book_data['ClassNm'], book_data['ClassNo']))

        print(f"Book '{book_data['BookName']}' registered successfully.")
        self.cursor.connection.commit()

    def read_books(self):
        self.cursor.execute("SELECT * FROM Books")
        books = self.cursor.fetchall()

        print("\n--- Registered Books ---")
        for book in books:
            print(f"ISBN: {book[0]}, Book Name: {book[1]}, Authors: {book[2]}, Publisher: {book[3]}, "
                  f"Publication Year: {book[4]}, Class Name: {book[5]}, Class No: {book[6]}")

    def update_book(self):
        books = self.get_all_books()
        if not books:
            print("No books available to update.")
            return

        self.display_all_books(books)
        isbn_to_update = input("Enter the ISBN of the book you want to update: ")
        selected_book = self.get_book_by_isbn(books, isbn_to_update)

        if not selected_book:
            print(f"Error: Book with ISBN {isbn_to_update} does not exist.")
            return

        book_data = self.get_book_data_from_selected(selected_book)
        self.input_book_data(book_data, is_update=True)

        # 유효성 검사
        if not self.validate_book_data(book_data):
            print("Book update failed due to invalid data.")
            return

        # 데이터베이스에 책 정보 업데이트
        self.cursor.execute('''
        UPDATE Books
        SET BookName = %s, Authors = %s, Publisher = %s, PublicationYear = %s, ClassNm = %s, ClassNo = %s
        WHERE ISBN = %s
        ''', (book_data['BookName'], book_data['Authors'], book_data['Publisher'],
              book_data['PublicationYear'], book_data['ClassNm'], book_data['ClassNo'], book_data['ISBN']))

        print(f"Book with ISBN {isbn_to_update} updated successfully.")
        self.cursor.connection.commit()

    def delete_book(self):
        books = self.get_all_books()
        if not books:
            print("No books available to delete.")
            return

        self.display_all_books(books)
        isbn_to_delete = input("Enter the ISBN of the book you want to delete: ")
        selected_book = self.get_book_by_isbn(books, isbn_to_delete)

        if not selected_book:
            print(f"Error: Book with ISBN {isbn_to_delete} does not exist.")
            return

        confirm = input(
            f"Are you sure you want to delete the book '{selected_book[1]}' (Authors: {selected_book[2]})? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Book deletion canceled.")
            return

        self.cursor.execute('''
        DELETE FROM Books
        WHERE ISBN = %s
        ''', (isbn_to_delete,))

        print(f"Book with ISBN {isbn_to_delete} deleted successfully.")
        self.cursor.connection.commit()

    def get_all_books(self):
        self.cursor.execute("SELECT ISBN, BookName, Authors, Publisher, PublicationYear, ClassNm, ClassNo FROM Books")
        return self.cursor.fetchall()

    def display_all_books(self, books):
        print("\n--- Registered Books ---")
        for book in books:
            print(f"ISBN: {book[0]}, Book Name: {book[1]}, Authors: {book[2]}, Publisher: {book[3]}, "
                  f"Publication Year: {book[4]}, Class Name: {book[5]}, Class No: {book[6]}")

    def get_book_data_defaults(self):
        return {
            'ISBN': '',
            'BookName': '',
            'Authors': '',
            'Publisher': '',
            'PublicationYear': 0,
            'ClassNm': '',
            'ClassNo': ''
        }

    def input_book_data(self, book_data, is_update=False):
        self.display_book_data(book_data)  # 현재 책 정보를 먼저 출력

        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1: ISBN")
            print("2: Book Name")
            print("3: Authors")
            print("4: Publisher")
            print("5: Publication Year")
            print("6: Class Name")
            print("7: Class No")
            print("8: Confirm and Register/Update Book")
            print("9: Cancel")

            choice = input("Select an option (1-9): ")

            if choice == '1':
                book_data['ISBN'] = input("Enter ISBN (13 characters): ")
            elif choice == '2':
                book_data['BookName'] = input("Enter book name: ")
            elif choice == '3':
                book_data['Authors'] = input("Enter authors: ")
            elif choice == '4':
                book_data['Publisher'] = input("Enter publisher: ")
            elif choice == '5':
                book_data['PublicationYear'] = int(input("Enter publication year: "))
            elif choice == '6':
                book_data['ClassNm'] = input("Enter class name: ")
            elif choice == '7':
                book_data['ClassNo'] = input("Enter class number: ")
            elif choice == '8':
                break
            elif choice == '9':
                print("Book registration/update canceled.")
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
        return next((book for book in books if book[0] == isbn), None)

    def get_book_data_from_selected(self, selected_book):
        return {
            'ISBN': selected_book[0],
            'BookName': selected_book[1],
            'Authors': selected_book[2],
            'Publisher': selected_book[3],
            'PublicationYear': selected_book[4],
            'ClassNm': selected_book[5],
            'ClassNo': selected_book[6]
        }

    def validate_book_data(self, book_data):
        # ISBN 유효성 검사
        if not book_data['ISBN'] or len(book_data['ISBN']) != 13:
            print("Error: ISBN must be 13 characters long.")
            return False

        # BookName 유효성 검사
        if not book_data['BookName']:
            print("Error: Book name cannot be empty.")
            return False

        # Authors 유효성 검사
        if not book_data['Authors']:
            print("Error: Authors cannot be empty.")
            return False

        # PublicationYear 유효성 검사
        if book_data['PublicationYear'] <= 0:
            print("Error: Publication Year must be a positive integer.")
            return False

        return True