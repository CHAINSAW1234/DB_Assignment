import requests
import psycopg2
from psycopg2 import sql


# 데이터베이스 연결 정보 설정
def get_db_connection():
    conn = psycopg2.connect(
        database='Library',
        user='postgres',
        password='adqe1463!',
        host='::1',
        port='5432'
    )
    return conn

# 도서관정보나루 API 호출
def fetch_libraries():
    url = "http://data4library.kr/api/libSrch"
    params = {
        'authKey': '04b61cd0daf65764c58899ec97d7bc593d99e3af0f4cbbe7f95d7e865fc8eb55',  # API 키
        'dtl_region': '21100',
        'format': 'json'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # JSON 형식으로 반환
    else:
        print(f"API 호출 실패: {response.status_code}")
        return None


# 데이터베이스에 도서관 정보 저장
def save_libraries_to_db(libraries):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO Libraries (LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, OperatingTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)


        for library in libraries:
            Data = library.get('lib')
            # 필요한 데이터 추출
            LibCode = int(Data.get('libCode'))
            LibName = Data.get('libName')
            Address = Data.get('address')
            Tel = Data.get('tel')
            Fax = Data.get('fax')
            Latitude = Data.get('latitude')
            Longitude = Data.get('longitude')
            Homepage = Data.get('homepage')
            OperatingTime = Data.get('operatingTime')

            # 데이터 삽입
            cur.execute(insert_query,
                        (LibCode, LibName, Address, Tel, Fax, Latitude, Longitude, Homepage, OperatingTime))

        conn.commit()  # 변경 사항을 커밋
        print("도서관 정보가 성공적으로 저장되었습니다.")

    except Exception as e:
        print(f"데이터베이스 오류: {e}")

    finally:
        cur.close()
        conn.close()


def fetch_lib_codes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # SQL 쿼리 실행
        cur.execute("SELECT libCode FROM Libraries;")

        # 결과 가져오기
        lib_codes = cur.fetchall()  # 모든 결과를 가져옴
        return [lib_code[0] for lib_code in lib_codes]  # libCode만 추출하여 리스트로 반환

    except Exception as e:
        print(f"데이터베이스 오류: {e}")
        return []

    finally:
        cur.close()
        conn.close()

def fatch_books(libcode):
    url = "http://data4library.kr/api/itemSrch"
    params = {
        'authKey': '04b61cd0daf65764c58899ec97d7bc593d99e3af0f4cbbe7f95d7e865fc8eb55',  # API 키
        'type': 'ALL',
        'libCode': libcode,
        'PageNo': '1',
        'format': 'json'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # JSON 형식으로 반환
    else:
        print(f"API 호출 실패: {response.status_code}")
        return None


# 데이터베이스에 도서관 정보 저장
def save_books(LibCode, books):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_ISBN_query = sql.SQL("""
            INSERT INTO Books (ISBN, BookName, Authors, Publisher, PublicationYear, ClassNm, ClassNo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)

        insert_query = sql.SQL("""
            INSERT INTO LibraryBooks (LibCode, ISBN, Vol, CallNumber, RegistrationDate)
            VALUES (%s, %s, %s, %s, %s)
        """)


        for book in books:
            Data = book.get('doc')

            # ISBN 먼저 검색
            ISBN = Data.get('isbn13')

            # Books에 있는지 검색
            cur.execute("SELECT * FROM Books WHERE ISBN = %s;", (ISBN,))

            # 결과 가져오기
            book = cur.fetchone()  # 하나의 결과만 가져옴
            if not book:
                # ISBN을 먼저 DB에 등록
                BookName = Data.get('bookname')
                Authors = Data.get('authors')
                Publisher = Data.get('publisher')
                PublicationYear = Data.get('publication_year')
                ClassNm = Data.get('class_no')
                ClassNo = Data.get('class_nm')
                # 데이터 삽입
                cur.execute(insert_ISBN_query,
                            (int(ISBN), BookName, Authors, Publisher, int(PublicationYear), ClassNm, ClassNo))

            # 필요한 데이터 추출
            Vol = Data.get('vol')
            callNumbers = Data.get('callNumbers')
            for callNumber in callNumbers:
                data = callNumber.get('callNumber')
                separate_shelf_code = data.get('separate_shelf_code')
                separate_shelf_name = data.get('separate_shelf_name')
                book_code = data.get('book_code')
                shelf_loc_code = data.get('shelf_loc_code')
                shelf_loc_name = data.get('shelf_loc_name')
                copy_code = data.get('copy_code')

                # None이 아닌 값만 필터링하여 문자열 연결
                CallNumber_parts = [
                    part for part in [
                        separate_shelf_code,
                        separate_shelf_name,
                        book_code,
                        shelf_loc_code,
                        shelf_loc_name,
                        copy_code
                    ] if part is not None
                ]

                # CallNumber 생성
                CallNumber = ''.join(CallNumber_parts)

                RegistrationDate = Data.get('reg_date')

                # 데이터 삽입
                cur.execute(insert_query,
                            (LibCode, int(ISBN), Vol, CallNumber, RegistrationDate))


        conn.commit()  # 변경 사항을 커밋
        print("장서 정보가 성공적으로 저장되었습니다.")

    except Exception as e:
        print(f"데이터베이스 오류: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    libraries_data = fetch_libraries()
    save_libraries_to_db(libraries_data['response']['libs'])  # API 응답의 구조에 맞게 수정

    libCodeData = fetch_lib_codes()
    for libCode in libCodeData:
        save_books(libCode, fatch_books(libCode)['response']['docs'])


