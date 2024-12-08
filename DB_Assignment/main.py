from base64 import decode

import psycopg2
from User.user import User

if __name__ == '__main__':
    user = User()

    try:
        con = psycopg2.connect(
            database='Library',
            user='postgres',
            password='adqe1463!',
            host='::1',
            port='5432'
        )

        cursor = con.cursor()

        while not user.login(cursor):
            print("Wrong ID and Password!")

        while True:
            user.get_menu()  # display menu
            while not user.login(cursor):
                print("Wrong ID and Password!")

    except psycopg2.OperationalError as e:
        print('Error: Unable to connect to the database.')
        print('Error message: ')
        print(e)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if con:
            con.close()
            print('Connection closed.')