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


def create_insurance_pools_table() -> None:

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS INSURANCE_POOLS (
            id INTEGER PRIMARY KEY,
            pool_name TEXT,
            pool_amount INTEGER,
            contribution_pool_id TEXT,
            payout_pool_id TEXT
            start_date DATETIME,
            end_date DATETIME
        );
        """
            )
        )


def create_insurance_members_table() -> None:

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS INSURANCE_MEMBERS (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            pool_id TEXT,
            user_payment_token,
            user_payment_URI,
            user_quote_id,
            pool_payment_token,
            pool_payment_URI,
            pool_quote_id,
            pool_initial_payment_needed,
            adhoc_contribution_uri,
            adhoc_contribution_token
        );
        """
            )
        )


def create_employers_table() -> None:

    with sqlite_conn.connect() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS EMPLOYERS (
            id INTEGER PRIMARY KEY,
            employer_number TEXT,
            user_id TEXT
        );
        """
            )
        )


if __name__ == "__main__":
    create_state_management_table()
    create_users_table()
    create_employers_table()
    create_insurance_pools_table()
    create_insurance_members_table()
