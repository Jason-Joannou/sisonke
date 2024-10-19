from sqlalchemy import text

from database.sqlite_connection import SQLiteConnection

sqlite_conn = SQLiteConnection(database="./database/test_db.db")


def create_state_management_table() -> None:

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS STATE_MANAGEMENT (
            id INTEGER PRIMARY KEY,
            user_number TEXT,
            last_interaction DATETIME,
            current_pool TEXT,
            stack_state TEXT
        );
        """
            )
        )


def create_users_table() -> None:

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY,
            user_number TEXT,
            user_wallet TEXT,
            tiger_beetle_id TEXT
        );
        """
            )
        )


if __name__ == "__main__":
    create_state_management_table()
    create_users_table()
