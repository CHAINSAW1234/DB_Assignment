import msvcrt
import sys
import getpass
import psycopg2

from User.userinterface import UserInterface
from User.admin import Admin
from User.librarian import Librarian
from User.regularuser import RegularUser

def get_masked_input(prompt="Enter password: "):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    password = []
    while True:
        char = msvcrt.getch()
        if char == b'\r' or char == b'\n':
            break
        elif char == b'\x08':  # Backspace
            if password:
                del password[-1]
                sys.stdout.write('\b \b')  # Erase the last asterisk
        else:
            password.append(char)
            sys.stdout.write('*')
            sys.stdout.write('\n')
    return b''.join(password).decode('utf-8')

class User:
    def __init__(self, user_interface: UserInterface = None):
        self.id = ""
        self.password = ""
        self.user_type = ""
        self.libCode = 0
        self.user_interface = user_interface  # using Dependency Injection

    def login(self, cursor: psycopg2.extensions.cursor):
        id = input("ID: ")
        password = input("Password: ")
        #password = get_masked_input()
        cursor.execute(f'select * from Users where ID = \'{id}\' and Password = \'{password}\'')

        result = cursor.fetchone()

        if result is None:
            return False

        user_type = ""
        if result[3] == 0:
            user_type = 'Admin'
        elif result[3] == 1:
            user_type = 'Library Manager'
        elif result[3] == 2:
            user_type = 'User'


        if user_type == 'Library Manager':
            self.libCode = result[4]

        print(f'You logged in as a {user_type}')

        if user_type == 'Admin':
            self.set_user_type(Admin(cursor))
        elif user_type == 'Library Manager':
            self.set_user_type(Librarian(cursor, result[0], self.libCode))
        elif user_type == 'User':
            self.set_user_type(RegularUser(cursor, result[0])) # result[0] : usercode
        else:
            print('Fatal Error. Database User schema user_type is contaminated')
            return False

        return True

    # used for dependency injection
    # setter for user_interface
    def set_user_type(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def debug(self):
        print(f"debug type : {self.user_type}")

    def get_menu(self):
        if self.user_interface :
            self.user_interface.get_menu()
