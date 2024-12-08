import psycopg2

# 데이터베이스 연결 정보 설정
conn = psycopg2.connect(
    database='Library',
    user='postgres',
    password='adqe1463!',
    host='::1',
    port='5432'
)

# 커서 생성
cur = conn.cursor()

# SQL 파일 읽기
with open('Create_Table.sql', 'r', encoding='utf-8') as sql_file1:
    sql_script_create = sql_file1.read()

with open('Trigger_Table.sql', 'r', encoding='utf-8') as sql_file2:
    sql_script_trigger = sql_file2.read()


# SQL 실행
try:
    cur.execute(sql_script_create)
    cur.execute(sql_script_trigger)
    conn.commit()  # 변경 사항을 커밋
    print("SQL 파일이 성공적으로 실행되었습니다.")
except Exception as e:
    print(f"SQL 실행 중 오류가 발생했습니다: {e}")
    conn.rollback()  # 오류 발생 시 롤백
finally:
    # 리소스 정리
    cur.close()
    conn.close()