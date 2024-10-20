import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import requests
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.sqlite_connection import SQLiteConnection
from database.utils import extract_whatsapp_number

db_conn = SQLiteConnection(database="./database/test_db.db")

TIGER_BEETLE_ENDPOINT_POOL_ENTITY = (
    "http://localhost:3001/tiger-beetle/createPoolEntities"
)


def insert_policy(pool_name: str, contribution_amount: int) -> None:

    with db_conn.connect() as conn:
        try:
            contribution_id = (
                requests.get(TIGER_BEETLE_ENDPOINT_POOL_ENTITY, timeout=10)
                .json()
                .get("poolEntityId")
            )
            print(contribution_id)
            payout_id = (
                requests.get(TIGER_BEETLE_ENDPOINT_POOL_ENTITY, timeout=10)
                .json()
                .get("poolEntityId")
            )

            conn.execute(
                text(
                    """
                INSERT INTO INSURANCE_POOLS (pool_name, pool_amount, contribution_pool_id, payout_pool_id) VALUES (:pool_name, :pool_amount, :contribution_pool_id, :payout_pool_id)
                """
                ),
                {
                    "pool_name": pool_name,
                    "pool_amount": contribution_amount,
                    "contribution_pool_id": contribution_id,
                    "payout_pool_id": payout_id,
                },
            )

            conn.commit()

        except SQLAlchemyError as e:
            conn.rollback()
            print(f"An error occurred during database query execution: {e}")
            raise e


def insert_insurance_member(
    user_id: str,
    policy_id: str,
    user_payment_token: str,
    user_payment_link: str,
    user_quote_id: str,
    pool_payment_token: str,
    pool_payment_link: str,
    pool_quote_id: str,
    adhoc_contribution_uri: str,
    adhoc_contribution_token: str,
    value: str,
) -> None:

    with db_conn.connect() as conn:

        try:
            conn.execute(
                text(
                    """
                    INSERT INTO INSURANCE_MEMBERS
                    (user_id, pool_id, user_payment_token, user_payment_URI, user_quote_id, pool_payment_token, pool_payment_URI, pool_quote_id, pool_initial_payment_needed, adhoc_contribution_uri, adhoc_contribution_token)
                    VALUES (:user_id, :policy_id, :user_payment_token, :user_payment_link, :user_quote_id, :pool_payment_token, :pool_payment_link, :pool_quote_id, :pool_initial_payment_needed, :adhoc_contribution_uri, :adhoc_contribution_token)
                    """
                ),
                {
                    "user_id": user_id,
                    "policy_id": policy_id,
                    "user_payment_token": user_payment_token,
                    "user_payment_link": user_payment_link,
                    "user_quote_id": user_quote_id,
                    "pool_payment_token": pool_payment_token,
                    "pool_payment_link": pool_payment_link,
                    "pool_quote_id": pool_quote_id,
                    "pool_initial_payment_needed": value,
                    "adhoc_contribution_uri": adhoc_contribution_uri,
                    "adhoc_contribution_token": adhoc_contribution_token,
                },
            )
            conn.commit()
        except SQLAlchemyError as e:
            conn.rollback()
            print(f"An error occurred during database query execution: {e}")
            raise e


def find_pool_id(pool_name: str):
    query = "SELECT id FROM INSURANCE_POOLS WHERE pool_name = :pool_name"
    with db_conn.connect() as conn:
        try:
            cursor = conn.execute(text(query), {"pool_name": pool_name})
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            print(f"An error occurred in find_pool_id: {e}")
            raise e


def get_insurance_member_details(pool_id, user_id):
    """
    Retrieve stokvel member details from the database given a stokvel ID and user ID.

    Args:
        stokvel_id (str): The ID of the stokvel to retrieve member details for.
        user_id (str): The user ID to filter the stokvel members by.

    Returns:
        dict: A dictionary containing the stokvel member's details, including
              the user ID, stokvel ID, contribution amount, payment token, payment
              URI, quote ID, and the creation date.
    """
    select_query = "SELECT * FROM INSURANCE_MEMBERS WHERE pool_id = :pool_id and user_id = :user_id"
    parameters = {"pool_id": pool_id, "user_id": user_id}
    with db_conn.connect() as conn:
        try:
            result = conn.execute(text(select_query), parameters)
            insurance_members_details = result.fetchone()  # Fetch one record

            if insurance_members_details is None:
                print(f"No stokvel found with id: {pool_id}")
                return None  # Return None if no record is found

            # Convert the result to a dictionary if necessary
            columns = result.keys()  # Extract column names from the result
            insurance_members_dict = dict(
                zip(columns, insurance_members_details)
            )  # Create a dictionary from column names and values

            return insurance_members_dict  # Return the details

        except sqlite3.Error as e:
            print(f"Error retrieving stokvel details: {e}")
            raise e
