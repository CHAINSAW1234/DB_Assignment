import sqlite3

class ManageUser:
    def __init__(self, cursor):
        self.cursor = cursor

    def manage_user(self):
        while True:
            print("\n--- User Management ---")
            print("1. Create User")
            print("2. Read Users")
            print("3. Update User")
            print("4. Delete User")
            print("5. Back to Main Menu")

            choice = int(input("Select an option (1-5): "))

            if choice == 1:
                self.create_user()
            elif choice == 2:
                self.read_users()
            elif choice == 3:
                self.update_user()
            elif choice == 4:
                self.delete_user()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    def create_user(self):
        user_data = self.get_user_data_defaults()
        self.input_user_data(user_data)

        # 유효성 검사
        if not self.validate_user_data(user_data):
            print("User registration failed due to invalid data.")
            return

        # 데이터베이스에 사용자 정보 등록
        self.cursor.execute('''
        INSERT INTO Users (ID, Password, AuthorCode, LibCode, Name, Age, Gender, PhoneNumber, Email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_data['ID'], user_data['Password'], user_data['AuthorCode'], user_data['LibCode'],
              user_data['Name'], user_data['Age'], user_data['Gender'], user_data['PhoneNumber'],
              user_data['Email']))


        print(f"User '{user_data['Name']}' registered successfully.")
        self.cursor.connection.commit()

    def read_users(self):
        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()

        print("\n--- Registered Users ---")
        for user in users:
            print(
                f"UserCode: {user[0]}, ID: {user[1]}, Name: {user[5]}, Age: {user[6]}, Gender: {user[7]}, Phone: {user[8]}, Email: {user[9]}")

    def update_user(self):
        users = self.get_all_users()
        if not users:
            print("No users available to update.")
            return

        self.display_all_users(users)
        user_code_to_update = int(input("Enter the UserCode of the user you want to update: "))
        selected_user = self.get_user_by_code(users, user_code_to_update)

        if not selected_user:
            print(f"Error: User with UserCode {user_code_to_update} does not exist.")
            return

        user_data = self.get_user_data_from_selected(selected_user)
        self.input_user_data(user_data, is_update=True)

        # 유효성 검사
        if not self.validate_user_data(user_data):
            print("User update failed due to invalid data.")
            return

        # 데이터베이스에 사용자 정보 업데이트
        self.cursor.execute('''
            UPDATE Users
            SET ID = %s, Password = %s, AuthorCode = %s, LibCode = %s, Name = %s, Age = %s, Gender = %s, PhoneNumber = %s, Email = %s
            WHERE UserCode = %s
        ''', (user_data['ID'], user_data['Password'], user_data['AuthorCode'], user_data['LibCode'],
              user_data['Name'], user_data['Age'], user_data['Gender'], user_data['PhoneNumber'],
              user_data['Email'], user_code_to_update))

        print(f"User with UserCode {user_code_to_update} updated successfully.")
        self.cursor.connection.commit()

    def delete_user(self):
        users = self.get_all_users()
        if not users:
            print("No users available to delete.")
            return

        self.display_all_users(users)
        user_code_to_delete = int(input("Enter the UserCode of the user you want to delete: "))
        selected_user = self.get_user_by_code(users, user_code_to_delete)

        if not selected_user:
            print(f"Error: User with UserCode {user_code_to_delete} does not exist.")
            return

        confirm = input(
            f"Are you sure you want to delete the UserCode '{user_code_to_delete}' (ID: {selected_user[1]})? (yes/no): ")
        if confirm.lower() != 'yes':
            print("User deletion canceled.")
            return

        self.cursor.execute('''
            DELETE FROM Users
            WHERE UserCode = %s
        ''', (user_code_to_delete,))  # 튜플로 전달

        print(f"User with UserCode {user_code_to_delete} deleted successfully.")
        self.cursor.connection.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

    def display_all_users(self, users):
        print("\n--- Registered Users ---")
        for user in users:
            print(
                f"UserCode: {user[0]}, ID: {user[1]}, Name: {user[5]}, Age: {user[6]}, Gender: {user[7]}, Phone: {user[8]}, Email: {user[9]}, AuthorCode: {user[3]}, LibCode: {user[4]}")

    def get_user_data_defaults(self):
        return {
            'ID': '',
            'Password': '',
            'AuthorCode': 0,  # 기본값: User
            'LibCode': None,
            'Name': '',
            'Age': 0,
            'Gender': 'M',  # 기본값: Male
            'PhoneNumber': '',
            'Email': ''
        }

    def input_user_data(self, user_data, is_update=False):
        print("\n--- Current User Details ---")
        self.display_user_data(user_data)

        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1. ID")
            print("2. Password")
            print("3. AuthorCode")
            print("4. LibCode")
            print("5. Name")
            print("6. Age")
            print("7. Gender")
            print("8. PhoneNumber")
            print("9. Email")
            print("10. Confirm and Register/Update User")
            print("11. Cancel")

            choice = input("Select an option (1-11): ")

            if choice == '1':
                user_data['ID'] = input("Enter user ID: ")
            elif choice == '2':
                user_data['Password'] = input("Enter password: ")
            elif choice == '3':
                user_data['AuthorCode'] = int(input("Enter author code (0: Admin, 1: Librarian, 2: User): "))
                if user_data['AuthorCode'] == 1:  # Librarian
                    self.display_libcodes()
                    user_data['LibCode'] = int(input("Enter library code: "))
                else:
                    user_data['LibCode'] = None
            elif choice == '4':
                if user_data['AuthorCode'] == 1:
                    self.display_libcodes()
                    user_data['LibCode'] = int(input("Enter library code: "))
                else:
                    print("You need to set AuthorCode to Admin first.")
            elif choice == '5':
                user_data['Name'] = input("Enter user name: ")
            elif choice == '6':
                user_data['Age'] = int(input("Enter age: "))
            elif choice == '7':
                while True:
                    gender_input = input("Enter gender (M/F): ").upper()
                    if gender_input in ['M', 'F']:
                        user_data['Gender'] = gender_input
                        break
                    else:
                        print("Invalid input. Please enter 'M' for Male or 'F' for Female.")
            elif choice == '8':
                user_data['PhoneNumber'] = input("Enter phone number: ")
            elif choice == '9':
                user_data['Email'] = input("Enter email: ")
            elif choice == '10':
                break
            elif choice == '11':
                print("User registration/update canceled.")
                return
            else:
                print("Invalid choice. Please try again.")

            # 현재 설정된 값을 다시 출력
            print("\n--- Current User Details ---")
            self.display_user_data(user_data)

    def display_user_data(self, user_data):
        for key, value in user_data.items():
            print(f"{key}: {value}")

    def display_libcodes(self):
        # 도서관 정보 조회
        self.cursor.execute("SELECT LibCode, LibName FROM Libraries")
        libraries = self.cursor.fetchall()

        print("\n--- Library Codes ---")
        for library in libraries:
            print(f"LibCode: {library[0]}, Library Name: {library[1]}")

    def get_user_by_code(self, users, user_code):
        return next((user for user in users if user[0] == user_code), None)

    def get_user_data_from_selected(self, selected_user):
        return {
            'ID': selected_user[1],
            'Password': selected_user[2],  # 비밀번호는 변경할 경우 새로 입력
            'AuthorCode': selected_user[3],  # AuthorCode는 사용자가 직접 입력해야 함
            'LibCode': selected_user[4],
            'Name': selected_user[5],
            'Age': selected_user[6],
            'Gender': selected_user[7],
            'PhoneNumber': selected_user[8],
            'Email': selected_user[9]
        }

    def validate_user_data(self, user_data):
        # ID 유효성 검사
        if not user_data['ID']:
            print("Error: User ID cannot be empty.")
            return False

        # Password 유효성 검사
        if not user_data['Password']:
            print("Error: Password cannot be empty.")
            return False

        # AuthorCode 유효성 검사
        if user_data['AuthorCode'] not in [0, 1, 2]:
            print("Error: AuthorCode must be 0, 1, or 2.")
            return False

        # LibCode 유효성 검사 (Librarian의 경우)
        if user_data['AuthorCode'] == 1 and user_data['LibCode'] is None:
            print("Error: LibCode must be provided for Admin users.")
            return False

        # Name 유효성 검사
        if not user_data['Name']:
            print("Error: Name cannot be empty.")
            return False

        # Age 유효성 검사
        if user_data['Age'] <= 0:
            print("Error: Age must be a positive integer.")
            return False

        # Gender 유효성 검사
        if user_data['Gender'] not in ['M', 'F']:
            print("Error: Gender must be 'M' or 'F'.")
            return False

        # PhoneNumber 유효성 검사 (간단한 형식 체크)
        if user_data['PhoneNumber'] and len(user_data['PhoneNumber']) < 10:
            print("Error: Phone number must be at least 10 characters long.")
            return False

        # Email 유효성 검사 (간단한 형식 체크)
        if user_data['Email'] and '@' not in user_data['Email']:
            print("Error: Email must be valid.")
            return False

        return True


