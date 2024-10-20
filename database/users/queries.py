from sqlalchemy import text

from database.sqlite_connection import SQLiteConnection
from database.utils import extract_whatsapp_number

sqlite_conn = SQLiteConnection(database="./database/test_db.db")


def check_if_number_exists_sqlite(from_number: str) -> bool:
    from_number = extract_whatsapp_number(from_number=from_number)
    query = "SELECT * FROM USERS WHERE user_number = :from_number"
    with sqlite_conn.connect() as conn:
        try:
            cursor = conn.execute(text(query), {"from_number": from_number})
            result = cursor.fetchone()
            if result:
                return True

            return False
        except Exception as e:
            print(f"An error occurred in check_if_number_exists: {e}")
            raise e


def insert_user(user_number: str, user_wallet: str, tiger_beetle_id: str) -> None:
    from_number = extract_whatsapp_number(from_number=user_number)
    query = "INSERT INTO USERS (user_number, user_wallet, tiger_beetle_id) VALUES (:from_number, :user_wallet, :tiger_beetle_id)"
    with sqlite_conn.connect() as conn:
        try:
            conn.execute(
                text(query),
                {
                    "from_number": from_number,
                    "user_wallet": user_wallet,
                    "tiger_beetle_id": tiger_beetle_id,
                },
            )
            conn.commit()
        except Exception as e:
            print(f"An error occurred in insert_user: {e}")
            conn.rollback()
            raise e


def get_employer_number_from_user(user_number: str) -> str:
    from_number = extract_whatsapp_number(from_number=user_number)
    employee_query = "SELECT id FROM USERS WHERE user_number = :from_number"
    employer_query = "SELECT employer_number FROM EMPLOYERS WHERE user_id= :user_id"
    with sqlite_conn.connect() as conn:
        try:
            result = conn.execute(
                text(employee_query), {"from_number": from_number}
            ).fetchone()
            employer_number = conn.execute(
                text(employer_query), {"user_id": result[0]}
            ).fetchone()

            if employer_number:
                return employer_number[0]

            return None
        except Exception as e:
            print(f"An error occurred in get_employer_id_from_user: {e}")
            raise e
