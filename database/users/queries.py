import sqlite3

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


def find_wallet_by_userid(user_id: str):
    query = "SELECT user_wallet FROM USERS WHERE id = :user_id"
    with sqlite_conn.connect() as conn:
        try:

            cursor = conn.execute(text(query), {"user_id": user_id})
            result = cursor.fetchone()[0]
            if result:
                return result
        except Exception as e:
            print("Exception occured in find_wallet_by_userid: ", e)
            raise e


def find_user_by_number(from_number: str):
    query = "SELECT id FROM USERS WHERE user_number = :from_number"
    from_number = extract_whatsapp_number(from_number=from_number)
    with sqlite_conn.connect() as conn:
        try:
            cursor = conn.execute(text(query), {"from_number": from_number})
            result = cursor.fetchone()[0]
            print(result)
            if result:
                return result

            return None
        except Exception as e:
            print(f"An error occurred in find_user_by_number: {e}")
            raise e


def update_user_contribution_token_uri(pool_id, user_id, new_token, new_uri):
    try:
        with sqlite_conn.connect() as conn:
            # Update query to modify user_payment_token and user_payment_URI
            update_query = """
            UPDATE INSURANCE_MEMBERS
            SET user_payment_token = :new_token,
                user_payment_URI = :new_uri
            WHERE pool_id = :pool_id AND id = :user_id
            """

            # Execute the update query with the provided parameters
            conn.execute(
                text(update_query),
                {
                    "new_token": new_token,
                    "new_uri": new_uri,
                    "pool_id": pool_id,
                    "user_id": user_id,
                },
            )

            # Commit the transaction
            conn.commit()

            print(
                f"User payment token and URI updated successfully for user_id {user_id} in pool_id {pool_id}"
            )

    except sqlite3.Error as e:
        print(f"SQLite error during update: {e}")
        raise e
    except Exception as e:
        print(f"Error during token/URI update: {e}")
        raise e


def insert_into_employers(employer_number, user_id):
    query = "INSERT INTO EMPLOYERS (employer_number, user_id) VALUES (:employer_number, :user_id)"
    with sqlite_conn.connect() as conn:
        try:
            conn.execute(
                text(query),
                {"employer_number": employer_number, "user_id": user_id},
            )
            conn.commit()
        except Exception as e:
            print(f"An error occurred in insert_into_employers: {e}")
            conn.rollback()
            raise e
