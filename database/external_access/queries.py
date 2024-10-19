from typing import Dict, List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.sqlite_connection import SQLiteConnection

db_conn = SQLiteConnection(database="./database/test_db.db")


def dynamic_read_operation(query: str, params: Dict) -> List[Dict]:
    try:
        with db_conn.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()
            # Convert each row to a dictionary using column names
            data = [dict(row._mapping) for row in rows]
            return data
    except SQLAlchemyError as e:
        print(f"An error occurred during database query execution: {e}")
        return []


def dynamic_write_operation(query: str, params: Dict) -> None:
    try:
        with db_conn.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
    except SQLAlchemyError as e:
        print(f"An error occurred during database query execution: {e}")
        conn.rollback()
        raise e
