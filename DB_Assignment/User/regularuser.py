from User.userinterface import UserInterface
from User.regularuser_module.manageregularuserloan import ManageRegularUserLoan

class RegularUser(UserInterface):
    def __init__(self, cursor, usercode):
        self.Manage_RegularUser_Loan = ManageRegularUserLoan(cursor, usercode)
        self.cursor = cursor
        self.usercode = usercode  # 이용자의 고유 ID

    def get_menu(self):
        while True:
            print("\n--- User Menu ---")
            print('1. Manage Information')
            print('2. View Library Collections')
            print('3. Manage Loan')
            print('4. Exit')

            choice = int(input("Select an option (1-6): "))

            if choice == 1:
                self.update_my_information()  # 이용자 정보 수정 기능 호출
            elif choice == 2:
                self.view_library_collections() # 도서관 장서 조회 기능 호출
            elif choice == 3:
                self.Manage_RegularUser_Loan.manage_loans()  # 대출 요청 기능 호출
            elif choice == 4:
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

    def update_my_information(self):
        # 현재 정보 조회
        self.cursor.execute("SELECT * FROM Users WHERE UserCode = %s", (self.usercode,))
        user = self.cursor.fetchone()

        if user:
            user_data = {
                'UserCode': user[0],  # UserCode는 수정 불가능
                'ID': user[1],
                'Password': user[2],  # 비밀번호는 수정하지 않음
                'Name': user[3],
                'Email': user[4],
                'PhoneNumber': user[5],
                'Age': user[6],
                'Gender': user[7]
            }
            print("\n--- Current My Information ---")
            self.display_user_data(user_data)

            self.input_user_data(user_data)

            # 데이터베이스에 이용자 정보 업데이트 (UserCode는 수정하지 않음)
            self.cursor.execute('''
            UPDATE Users
            SET Name = %s, Email = %s, PhoneNumber = %s, Age = %s, Gender = %s
            WHERE UserCode = %s
            ''', (user_data['Name'], user_data['Email'], user_data['PhoneNumber'],
                  user_data['Age'], user_data['Gender'], self.usercode))

            self.cursor.connection.commit()
            print("Your information has been updated successfully.")
        else:
            print("Error: User not found.")

    def input_user_data(self, user_data):
        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1. Name")
            print("2. Email")
            print("3. PhoneNumber")
            print("4. Age")
            print("5. Gender")
            print("6. Confirm and Update")
            print("7. Cancel")

            choice = input("Select an option (1-7): ")

            if choice == '1':
                user_data['Name'] = input("Enter new name: ")
            elif choice == '2':
                user_data['Email'] = input("Enter new email: ")
            elif choice == '3':
                user_data['PhoneNumber'] = input("Enter new phone number: ")
            elif choice == '4':
                user_data['Age'] = int(input("Enter new age: "))
            elif choice == '5':
                while True:
                    gender_input = input("Enter gender (M/F): ").upper()
                    if gender_input in ['M', 'F']:
                        user_data['Gender'] = gender_input
                        break
                    else:
                        print("Invalid input. Please enter 'M' for Male or 'F' for Female.")
            elif choice == '6':
                break
            elif choice == '7':
                print("Update canceled.")
                return
            else:
                print("Invalid choice. Please try again.")

            # 현재 설정된 값을 다시 출력
            print("\n--- Current User Details ---")
            self.display_user_data(user_data)

    def display_user_data(self, user_data):
        for key, value in user_data.items():
            print(f"{key}: {value}")

    def view_library_collections(self):
        # 도서관 code 보여주기
        self.display_all_libraries()
        libcode = int(input("Enter the Library Code to view collections: "))

        # 도서관 장서 조회 로직 구현
        self.cursor.execute("""
            SELECT b.ISBN, b.BookName, b.Authors, lb.Vol, lb.CallNumber, lb.RegistrationDate, lb.ISLoan
            FROM LibraryBooks lb
            JOIN Books b ON lb.ISBN = b.ISBN
            WHERE lb.LibCode = %s
        """, (libcode,))
        books = self.cursor.fetchall()

        print("\n--- Library Collections ---")
        for book in books:
            print(
                f"ISBN: {book[0]}, BookName: {book[1]}, Authors: {book[2]}, Volume: {book[3]}, Call Number: {book[4]}, Registration Date: {book[5]}, Is Loaned: {'Yes' if book[6] else 'No'}")

    def display_all_libraries(self):
        self.cursor.execute(
            "SELECT LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, Closed, OperatingTime, BookCount FROM Libraries")
        libraries = self.cursor.fetchall()

        print("\n--- Registered Libraries ---")
        for lib in libraries:
            print(f"LibCode: {lib[0]}, Name: {lib[1]}, Address: {lib[2]}, Tel: {lib[3]}, Fax: {lib[4]}, "
                  f"Latitude: {lib[5]}, Longitude: {lib[6]}, Homepage: {lib[7]}, Closed: {lib[8]}, "
                  f"Operating Time: {lib[9]}, Book Count: {lib[10]}")
