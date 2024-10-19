from sqlalchemy import text

from .sqlite_connection import SQLiteConnection

sqlite_conn = SQLiteConnection(database="./database/test_db.db")


def create_state_management_table() -> None:
    """
    docstring
    """

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS STATE_MANAGEMENT (
            id INTEGER PRIMARY KEY,
            user_number TEXT,
            last_interaction DATETIME,
            current_pool Text,
            stack_state TEXT
        );
        """
            )
        )


if __name__ == "__main__":
    create_state_management_table()
