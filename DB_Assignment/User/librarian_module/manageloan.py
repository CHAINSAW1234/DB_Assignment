import psycopg2

class ManageLoanProposals:
    def __init__(self, cursor, libcode):
        self.cursor = cursor
        self.libCode = libcode
    def manage_loan_proposals(self):
        while True:
            print("\n--- Loan Proposal Management ---")
            print("1. View Loan Proposals")
            print("2. Approve a Proposal")
            print("3. Reject a Proposal")
            print("4. Back to Main Menu")

            choice = int(input("Select an option (1-4): "))

            if choice == 1:
                self.view_proposals()
            elif choice == 2:
                self.approve_proposal()
            elif choice == 3:
                self.reject_proposal()
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again.")

    def view_proposals(self):
        self.cursor.execute("""SELECT * FROM LoanProposals WHERE LibCode = %s""", (self.libCode,))
        proposals = self.cursor.fetchall()

        print("\n--- Current Loan Proposals ---")
        for proposal in proposals:
            print(
                f"Proposal ID: {proposal[0]}, LibCode: {proposal[1]}, ISBN: {proposal[2]}, Volume: {proposal[3]}, Call Number: {proposal[4]}, User Code: {proposal[5]}, Loan Classification: {proposal[6]}")

    def approve_proposal(self):
        proposal_id = int(input("Enter the Proposal ID to approve: "))

        # 대출 제안 조회
        self.cursor.execute("SELECT * FROM LoanProposals WHERE ProposalID = %s", (proposal_id,))
        proposal = self.cursor.fetchone()

        if proposal:
            loan_classification = proposal[6]  # LoanClassification

            if loan_classification == 0:
                # LoanClassification이 0이면 Loans 테이블에 추가
                self.cursor.execute('''
                    INSERT INTO Loans (LibCode, ISBN, Vol, CallNumber, UserCode, LoanDate, ReturnDate)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_DATE + INTERVAL '14 days')
                    ''', (proposal[1], proposal[2], proposal[3], proposal[4], proposal[5]))  # 기본 대출 기간 14일

                print(f"Loan proposal with ID {proposal_id} has been approved and added to Loans table.")
            elif loan_classification == 1:
                # LoanClassification이 1이면 LoanProposals에서 삭제
                self.cursor.execute('''
                DELETE FROM Loans
                WHERE LibCode = %s AND ISBN = %s AND Vol = %s AND CallNumber = %s AND UserCode = %s
                ''', (proposal[1], proposal[2], proposal[3], proposal[4], proposal[5]))
                print(f"Loan proposal with ID {proposal_id} has been approved and will be deleted from proposals.")

            self.cursor.execute('DELETE FROM LoanProposals WHERE ProposalID = %s', (proposal_id,))
            self.cursor.connection.commit()
        else:
            print("Error: Proposal ID not found.")

    def reject_proposal(self):
        proposal_id = int(input("Enter the Proposal ID to reject: "))
        self.cursor.execute('''
        DELETE FROM LoanProposals WHERE ProposalID = %s
        ''', (proposal_id,))

        print(f"Loan proposal with ID {proposal_id} has been rejected and removed from proposals.")
        self.cursor.connection.commit()