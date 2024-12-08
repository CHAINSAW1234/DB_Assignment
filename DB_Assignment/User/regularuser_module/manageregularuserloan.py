import psycopg2


class ManageRegularUserLoan:
    def __init__(self, cursor, usercode):
        self.cursor = cursor
        self.usercode = usercode  # 이용자의 고유 ID

    def manage_loans(self):
        while True:
            self.view_my_loans()
            print("\n--- Loan Management ---")
            print("1. Request Loan")
            print("2. Update Loans")
            print("3. Request Return")
            print("4. Back to Main Menu")

            choice = int(input("Select an option (1-4): "))

            if choice == 1:
                self.request_loan()
            elif choice == 2:
                self.update_loans()
            elif choice == 3:
                self.request_return()
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again.")

    def request_loan(self):

        # 1. libcode를 보여주고 선택
        self.display_all_libraries()
        libcode = int(input("Enter the Library Code to view collections: "))

        # 2. 해당 도서관이 보유중인 장서 출력
        self.cursor.execute("""
            SELECT b.ISBN, b.BookName, b.Authors, lb.Vol, lb.CallNumber, lb.RegistrationDate, lb.ISLoan
            FROM LibraryBooks lb
            JOIN Books b ON lb.ISBN = b.ISBN
            WHERE lb.LibCode = %s
        """, (libcode,))
        books = self.cursor.fetchall()

        print(f"\n--- Available Books in Library Code: {libcode} ---")
        if books:
            for idx, book in enumerate(books):
                print(
                    f"{idx + 1}. ISBN: {book[0]}, BookName: {book[1]}, Authors: {book[2]}, Volume: {book[3]}, Call Number: {book[4]}, Is Loaned: {'Yes' if book[6] else 'No'}")

        # 3. 보유 장서중에서 대출할 책 선택
        choice = int(input("Select a book to loan (enter the number): ")) - 1

        if 0 <= choice < len(books):
            selected_book = books[choice]
            if not selected_book[6]:  # 선택한 책이 대출 중이지 않은 경우
                self.cursor.execute('''
                INSERT INTO LoanProposals (LibCode, ISBN, Vol, CallNumber, UserCode, LoanClassification)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''', (libcode, selected_book[0], selected_book[3], selected_book[4], self.usercode, 0))  # LibCode와 ISBN 설정

                print(f"Loan request for book with ISBN {selected_book[0]} has been successfully submitted.")
                self.cursor.connection.commit()
            else:
                print("Error: Selected book is currently loaned out.")
        else:
            print("Error: Invalid selection.")

    def view_my_loans(self):
        # 자신의 대출 조회
        self.cursor.execute('''
        SELECT LoanCode, LibCode, ISBN, Vol, CallNumber, LoanDate, ReturnDate, LoanExtensions 
        FROM Loans 
        WHERE UserCode = %s
        ''', (self.usercode,))
        loans = self.cursor.fetchall()

        if loans:
            print("\n--- My Loans ---")
            for loan in loans:
                print(
                    f"LoanCode: {loan[0]}, LibCode: {loan[1]}, ISBN: {loan[2]}, Volume: {loan[3]}, Call Number: {loan[4]}, "
                    f"Loan Date: {loan[5]}, Return Date: {loan[6]}, Loan Extensions: {loan[7]}")
        else:
            print("You have no active loans.")

    def request_return(self):
        # 1. 자신의 대출 조회
        self.cursor.execute('''
        SELECT LoanCode, LibCode, ISBN, Vol, CallNumber, LoanDate, ReturnDate 
        FROM Loans 
        WHERE UserCode = %s
        ''', (self.usercode,))
        loans = self.cursor.fetchall()

        if loans:
            print("\n--- My Loans ---")
            for loan in loans:
                print(
                    f"LoanCode: {loan[0]}, LibCode: {loan[1]}, ISBN: {loan[2]}, Volume: {loan[3]}, Call Number: {loan[4]}, "
                    f"Loan Date: {loan[5]}, Return Date: {loan[6]}")

            # 2. 반납할 대출 선택
            loan_code = int(input("Enter the Loan Code of the loan you want to return: "))

            # 선택한 대출이 존재하는지 확인
            selected_loan = next((loan for loan in loans if loan[0] == loan_code), None)

            if selected_loan:
                # 3. LoanProposals 테이블에 반납 요청 추가
                self.cursor.execute('''
                INSERT INTO LoanProposals (LibCode, ISBN, Vol, CallNumber, UserCode, LoanClassification)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''', (selected_loan[1], selected_loan[2], selected_loan[3], selected_loan[4], self.usercode, 1))

                print(f"Return request for LoanCode {loan_code} has been successfully submitted.")
                self.cursor.connection.commit()
            else:
                print("Error: Invalid Loan Code.")
        else:
            print("You have no active loans.")

    def display_all_libraries(self):
        self.cursor.execute(
            "SELECT LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, Closed, OperatingTime, BookCount FROM Libraries")
        libraries = self.cursor.fetchall()

        print("\n--- Registered Libraries ---")
        for lib in libraries:
            print(f"LibCode: {lib[0]}, Name: {lib[1]}, Address: {lib[2]}, Tel: {lib[3]}, Fax: {lib[4]}, "
                  f"Latitude: {lib[5]}, Longitude: {lib[6]}, Homepage: {lib[7]}, Closed: {lib[8]}, "
                  f"Operating Time: {lib[9]}, Book Count: {lib[10]}")

    def update_loans(self):
        # 대출 연장 로직을 구현합니다.
        self.cursor.execute('''
                SELECT LoanCode, LibCode, ISBN, Vol, CallNumber, LoanDate, ReturnDate, LoanExtensions 
                FROM Loans 
                WHERE UserCode = %s
                ''', (self.usercode,))
        loans = self.cursor.fetchall()

        if loans:
            loan_code = input("Enter the Loan Code of the loan you want to extend: ")
            if not loan_code.isdigit():
                print("Invalid Loan Code.")
                return
            loan_code = int(loan_code)

            # 선택한 대출이 존재하는지 확인
            selected_loan = next((loan for loan in loans if loan[0] == loan_code), None)

            if selected_loan:
                # 연장 가능 여부 확인
                if selected_loan[7] >= 2:  # LoanExtensions가 2 이상인 경우
                    print("Error: You cannot extend this loan any further.")
                    return

                # 대출 연장 요청 처리
                self.cursor.execute('''
                UPDATE Loans
                SET LoanExtensions = LoanExtensions + 1,
                    ReturnDate = CURRENT_DATE + INTERVAL '14 days'
                WHERE LoanCode = %s
                ''', (loan_code,))
                self.cursor.connection.commit()
                print(f"Loan extension request for LoanCode {loan_code} has been successfully submitted.")
            else:
                print("Error: Invalid Loan Code.")
        else:
            print("You have no active loans.")

