import sqlite3

class ManageLibraries:
    def __init__(self, cursor):
        self.cursor = cursor

    def manage_libraries(self):
        while True:
            print("\n--- Library Management ---")
            print("1. Create Library")
            print("2. Read Libraries")
            print("3. Update Library")
            print("4. Delete Library")
            print("5. Back to Main Menu")

            choice = int(input("Select an option (1-5): "))

            if choice == 1:
                self.create_library()
            elif choice == 2:
                self.read_libraries()
            elif choice == 3:
                self.update_library()
            elif choice == 4:
                self.delete_library()
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    def create_library(self):
        library_data = self.get_library_data_defaults()
        self.input_library_data(library_data)

        # 유효성 검사
        if not self.validate_library_data(library_data):
            print("Library registration failed due to invalid data.")
            return

        # 데이터베이스에 라이브러리 정보 등록
        self.cursor.execute('''
        INSERT INTO Libraries (LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, Closed, OperatingTime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (library_data['LibCode'], library_data['LibName'], library_data['Address'],
              library_data['Tel'], library_data['Fax'], library_data['Latitude'],
              library_data['Longitude'], library_data['Homepage'], library_data['Closed'],
              library_data['OperatingTime']))

        print(f"Library '{library_data['LibName']}' registered successfully.")
        self.cursor.connection.commit()

    def read_libraries(self):
        self.cursor.execute("SELECT * FROM Libraries")
        libraries = self.cursor.fetchall()

        print("\n--- Registered Libraries ---")
        for lib in libraries:
            print(f"LibCode: {lib[0]}, Name: {lib[1]}, Address: {lib[2]}, Tel: {lib[3]}, Fax: {lib[4]}, "
                  f"Latitude: {lib[5]}, Longitude: {lib[6]}, Homepage: {lib[7]}, Closed: {lib[8]}, "
                  f"Operating Time: {lib[9]}, Book Count: {lib[10]}")

    def update_library(self):
        libraries = self.get_all_libraries()
        if not libraries:
            print("No libraries available to update.")
            return

        self.display_all_libraries(libraries)
        lib_code_to_update = int(input("Enter the LibCode of the library you want to update: "))
        selected_library = self.get_library_by_code(libraries, lib_code_to_update)

        if not selected_library:
            print(f"Error: Library with LibCode {lib_code_to_update} does not exist.")
            return

        library_data = self.get_library_data_from_selected(selected_library)
        self.input_library_data(library_data, is_update=True)

        # 유효성 검사
        if not self.validate_library_data(library_data):
            print("Library update failed due to invalid data.")
            return

        # 데이터베이스에 라이브러리 정보 업데이트
        self.cursor.execute('''
        UPDATE Libraries
        SET LibName = %s, Address = %s, Tel = %s, Fax = %s, Latitude = %s, Longitude = %s, Homepage = %s, Closed = %s, OperatingTime = %s
        WHERE LibCode = %s
        ''', (library_data['LibName'], library_data['Address'], library_data['Tel'],
              library_data['Fax'], library_data['Latitude'], library_data['Longitude'],
              library_data['Homepage'], library_data['Closed'], library_data['OperatingTime'],
              lib_code_to_update))

        print(f"Library with LibCode {lib_code_to_update} updated successfully.")
        self.cursor.connection.commit()

    def delete_library(self):
        libraries = self.get_all_libraries()
        if not libraries:
            print("No libraries available to delete.")
            return

        self.display_all_libraries(libraries)
        lib_code_to_delete = int(input("Enter the LibCode of the library you want to delete: "))
        selected_library = self.get_library_by_code(libraries, lib_code_to_delete)

        if not selected_library:
            print(f"Error: Library with LibCode {lib_code_to_delete} does not exist.")
            return

        confirm = input(
            f"Are you sure you want to delete the library '{selected_library[1]}'? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Library deletion canceled.")
            return

        self.cursor.execute('''
        DELETE FROM Libraries
        WHERE LibCode = %s
        ''', (lib_code_to_delete,))

        print(f"Library with LibCode {lib_code_to_delete} deleted successfully.")
        self.cursor.connection.commit()

    def get_all_libraries(self):
        self.cursor.execute("SELECT LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, Closed, OperatingTime, BookCount FROM Libraries")
        return self.cursor.fetchall()

    def display_all_libraries(self, libraries):
        print("\n--- Registered Libraries ---")
        for lib in libraries:
            print(f"LibCode: {lib[0]}, Name: {lib[1]}, Address: {lib[2]}, Tel: {lib[3]}, Fax: {lib[4]}, "
                  f"Latitude: {lib[5]}, Longitude: {lib[6]}, Homepage: {lib[7]}, Closed: {lib[8]}, "
                  f"Operating Time: {lib[9]}, Book Count: {lib[10]}")

    def get_library_data_defaults(self):
        return {
            'LibCode': 0,
            'LibName': '',
            'Address': '',
            'Tel': '',
            'Fax': '',
            'Latitude': 0.0,
            'Longitude': 0.0,
            'Homepage': '',
            'Closed': False,
            'OperatingTime': '',
            'BookCount': 0
        }

    def input_library_data(self, library_data, is_update=False):
        self.display_library_data(library_data)  # 현재 라이브러리 정보를 먼저 출력

        while True:
            print("\n--- Select a field to update or confirm your details ---")
            print("1: LibCode")
            print("2: LibName")
            print("3: Address")
            print("4: Tel")
            print("5: Fax")
            print("6: Latitude")
            print("7: Longitude")
            print("8: Homepage")
            print("9: Closed (True/False)")
            print("10: Operating Time")
            print("11: Confirm and Register/Update Library")
            print("12: Cancel")

            choice = input("Select an option (1-13): ")

            if choice == '1':
                library_data['LibCode'] = int(input("Enter LibCode: "))
            elif choice == '2':
                library_data['LibName'] = input("Enter library name: ")
            elif choice == '3':
                library_data['Address'] = input("Enter address: ")
            elif choice == '4':
                library_data['Tel'] = input("Enter telephone number: ")
            elif choice == '5':
                library_data['Fax'] = input("Enter fax number: ")
            elif choice == '6':
                library_data['Latitude'] = float(input("Enter latitude: "))
            elif choice == '7':
                library_data['Longitude'] = float(input("Enter longitude: "))
            elif choice == '8':
                library_data['Homepage'] = input("Enter homepage URL: ")
            elif choice == '9':
                library_data['Closed'] = input("Is the library closed? (True/False): ").strip().lower() == 'true'
            elif choice == '10':
                library_data['OperatingTime'] = input("Enter operating time: ")
            elif choice == '11':
                break
            elif choice == '12':
                print("Library registration/update canceled.")
                return
            else:
                print("Invalid choice. Please try again.")

            # 현재 설정된 값을 다시 출력
            self.display_library_data(library_data)

    def display_library_data(self, library_data):
        print("\n--- Current Library Details ---")
        for key, value in library_data.items():
            print(f"{key}: {value}")

    def get_library_by_code(self, libraries, lib_code):
        return next((lib for lib in libraries if lib[0] == lib_code), None)

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
            'OperatingTime': selected_library[9]
        }

    def validate_library_data(self, library_data):
        # LibCode 유효성 검사
        if library_data['LibCode'] <= 0:
            print("Error: LibCode must be a positive integer.")
            return False

        # LibName 유효성 검사
        if not library_data['LibName']:
            print("Error: Library name cannot be empty.")
            return False

        # Address 유효성 검사
        if not library_data['Address']:
            print("Error: Address cannot be empty.")
            return False

        # Tel 유효성 검사 (선택적)
        if library_data['Tel'] and len(library_data['Tel']) < 5:
            print("Error: Telephone number must be at least 5 characters long.")
            return False

        # Fax 유효성 검사 (선택적)
        if library_data['Fax'] and len(library_data['Fax']) < 5:
            print("Error: Fax number must be at least 5 characters long.")
            return False

        # Latitude 유효성 검사
        if not (-90 <= library_data['Latitude'] <= 90):
            print("Error: Latitude must be between -90 and 90.")
            return False

        # Longitude 유효성 검사
        if not (-180 <= library_data['Longitude'] <= 180):
            print("Error: Longitude must be between -180 and 180.")
            return False

        # Homepage 유효성 검사 (선택적)
        if library_data['Homepage'] and not library_data['Homepage'].startswith('http'):
            print("Error: Homepage must be a valid URL starting with 'http'.")
            return False

        return True

