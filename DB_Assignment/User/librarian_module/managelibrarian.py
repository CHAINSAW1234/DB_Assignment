import psycopg2

class ManageLibrarian:
    def __init__(self, cursor, usercode, libcode):
        self.cursor = cursor
        self.usercode = usercode  # UserCode
        self.libCode = libcode     # LibCode

    def manage_librarian(self):
        while True:
            print("\n--- Librarian Management ---")
            print("1. Update My Information")
            print("2. Update My Library Information")
            print("3. Back to Main Menu")

            choice = int(input("Select an option (1-3): "))

            if choice == 1:
                self.update_my_information()
            elif choice == 2:
                self.update_my_library_information()
            elif choice == 3:
                break
            else:
                print("Invalid choice. Please try again.")

    def update_my_information(self):
        # 현재 정보 조회
        self.cursor.execute("SELECT * FROM Users WHERE UserCode = %s", (self.usercode,))
        user = self.cursor.fetchone()

        if user:
            user_data = self.get_user_data_from_selected(user)
            self.input_user_data(user_data, is_update=True)

            # 유효성 검사
            if not self.validate_user_data(user_data):
                print("User update failed due to invalid data.")
                return

            # 데이터베이스에 사용자 정보 업데이트
            self.cursor.execute('''
            UPDATE Users
            SET ID = %s, Password = %s, Name = %s, Age = %s, Gender = %s, PhoneNumber = %s, Email = %s
            WHERE UserCode = %s
            ''', (user_data['ID'], user_data['Password'], user_data['Name'],
                  user_data['Age'], user_data['Gender'], user_data['PhoneNumber'],
                  user_data['Email'], self.usercode))

            self.cursor.connection.commit()
            print("Your information has been updated successfully.")
        else:
            print("Error: User not found.")

    def input_user_data(self, user_data, is_update=False):
        print("\n--- Current User Details ---")
        self.display_user_data(user_data)

        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1. ID")
            print("2. Password")
            print("3. Name")
            print("4. Age")
            print("5. Gender")
            print("6. PhoneNumber")
            print("7. Email")
            print("8. Confirm and Update")
            print("9. Cancel")

            choice = input("Select an option (1-9): ")

            if choice == '1':
                user_data['ID'] = input("Enter new user ID: ")
            elif choice == '2':
                user_data['Password'] = input("Enter new password: ")
            elif choice == '3':
                user_data['Name'] = input("Enter new name: ")
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
                user_data['PhoneNumber'] = input("Enter new phone number: ")
            elif choice == '7':
                user_data['Email'] = input("Enter new email: ")
            elif choice == '8':
                break
            elif choice == '9':
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

    def get_user_data_from_selected(self, selected_user):
        return {
            'UserCode': selected_user[0],
            'ID': selected_user[1],
            'Password': selected_user[2],
            'AuthorCode': selected_user[3],
            'LibCode': selected_user[4],
            'Name': selected_user[5],
            'Age': selected_user[6],
            'Gender': selected_user[7],
            'PhoneNumber': selected_user[8],
            'Email': selected_user[9]
        }

    def validate_user_data(self, user_data):
        # Name 유효성 검사
        if not user_data['Name']:
            print("Error: Name cannot be empty.")
            return False

        # Email 유효성 검사 (간단한 형식 체크)
        if user_data['Email'] and '@' not in user_data['Email']:
            print("Error: Email must be valid.")
            return False

        # PhoneNumber 유효성 검사 (간단한 형식 체크)
        if user_data['PhoneNumber'] and len(user_data['PhoneNumber']) < 10:
            print("Error: Phone number must be at least 10 characters long.")
            return False

        return True

    def update_my_library_information(self):
        # 현재 도서관 정보 조회
        self.cursor.execute('''
        SELECT * FROM Libraries WHERE LibCode = %s
        ''', (self.libCode,))

        library = self.cursor.fetchone()

        if library:
            library_data = self.get_library_data_from_selected(library)
            self.input_lib_data(library_data)

            # 데이터베이스에 도서관 정보 업데이트 (BookCount는 제외)
            self.cursor.execute('''
            UPDATE Libraries
            SET LibName = %s, Address = %s, Tel = %s, Fax = %s, Latitude = %s, Longitude = %s, Homepage = %s, Closed = %s, OperatingTime = %s
            WHERE LibCode = %s
            ''', (library_data['LibName'], library_data['Address'], library_data['Tel'],
                  library_data['Fax'], library_data['Latitude'], library_data['Longitude'],
                  library_data['Homepage'], library_data['Closed'], library_data['OperatingTime'],
                  library_data['LibCode']))

            self.cursor.connection.commit()
            print("Your library information has been updated successfully.")
        else:
            print("Error: Library not found.")

    def get_library_data_from_selected(self, selected_library):
        return {
            'LibCode': selected_library[0],
            'LibName': selected_library[1],
            'Address': selected_library[2],
            'Tel': selected_library[3],
            'Fax': selected_library[4],
            'Latitude': selected_library[5],
            'Longitude': selected_library[6],
            'Homepage': selected_library[7],
            'Closed': selected_library[8],
            'OperatingTime': selected_library[9],
            'BookCount': selected_library[10]  # BookCount는 수정을 하지 않음
        }

    def input_lib_data(self, library_data):
        print("\n--- Current Library Details ---")
        self.display_lib_data(library_data)

        while True:
            print("\n--- Select a field to update or confirm your library details ---")
            print("1. LibName")
            print("2. Address")
            print("3. Tel")
            print("4. Fax")
            print("5. Latitude")
            print("6. Longitude")
            print("7. Homepage")
            print("8. Closed")
            print("9. OperatingTime")
            print("10. Confirm and Update")
            print("11. Cancel")

            choice = input("Select an option (1-11): ")

            if choice == '1':
                library_data['LibName'] = input("Enter new library name: ")
            elif choice == '2':
                library_data['Address'] = input("Enter new address: ")
            elif choice == '3':
                library_data['Tel'] = input("Enter new telephone number: ")
            elif choice == '4':
                library_data['Fax'] = input("Enter new fax number: ")
            elif choice == '5':
                library_data['Latitude'] = float(input("Enter new latitude: "))
            elif choice == '6':
                library_data['Longitude'] = float(input("Enter new longitude: "))
            elif choice == '7':
                library_data['Homepage'] = input("Enter new homepage: ")
            elif choice == '8':
                library_data['Closed'] = input("Is the library closed? (True/False): ") == 'True'
            elif choice == '9':
                library_data['OperatingTime'] = input("Enter new operating time: ")
            elif choice == '10':
                break
            elif choice == '11':
                print("Update canceled.")
                return
            else:
                print("Invalid choice. Please try again.")

            # 현재 설정된 값을 다시 출력
            print("\n--- Current Library Details ---")
            self.display_lib_data(library_data)

    def display_lib_data(self, library_data):
        for key, value in library_data.items():
            print(f"{key}: {value}")

