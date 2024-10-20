import threading
import time
from datetime import datetime

import requests

from database.demo_queries import (
    update_next_contributions_dates,
    update_next_payout_dates,
    update_pool_token_uri,
    update_user_contribution_token_uri,
)
from database.insurance.queries import get_insurance_member_details

# Define the first method

node_server_initiate_grant = "http://localhost:3001/incoming-payment-setup"
node_server_initiate_stokvelpayout_grant = (
    "http://localhost:3001/incoming-payment-setup-stokvel-payout"
)

node_server_create_initial_payment = (
    "http://localhost:3001/create-initial-outgoing-payment"
)

node_server_recurring_payment = (
    "http://localhost:3001/payments/process-recurring-payments"
)
node_server_recurring_payment_with_interest = (
    "http://localhost:3001/process-recurring-winterest-payment"
)


def run_contribution_simulation(pool_id: int, user_id_wallets: dict):
    contributions = {}
    current_next_date = datetime.now()
    for j in range(1, 12):
        print(f"Month: {j}")
        for userid, wallet in user_id_wallets.items():

            if userid not in contributions:
                contributions[userid] = 0

            stokvel_members_details = get_insurance_member_details(pool_id, userid)
            print("add recurring payment")
            payload = {
                "sender_wallet_address": wallet,
                "receiving_wallet_address": "https://ilp.interledger-test.dev/insurance_pool_one",
                "manageUrl": stokvel_members_details.get("user_payment_URI"),
                "previousToken": stokvel_members_details.get("user_payment_token"),
                "contributionValue": str(
                    stokvel_members_details.get("pool_initial_payment_needed")
                ),
            }

            response = requests.post(
                node_server_recurring_payment, json=payload, timeout=10
            )

            print(response)
            print("RESPONSE: \n", response.json())

            new_token = response.json()["token"]
            new_uri = response.json()["manageurl"]

            update_user_contribution_token_uri(pool_id, userid, new_token, new_uri)

            # contributions[userid] += stokvel_members_details.get("contribution_amount")
            # current_next_date = update_next_contributions_dates(current_next_date, pool_id, "Months")
        time.sleep(30)


def run_payout_simulation(
    pool_id: int, user_id_wallets: dict
):  # this will be a dict of all of the users that we need to pay out
    current_next_date = "2024-10-10"
    for j in range(0, 5):
        for userid, wallet in user_id_wallets.items():
            stokvel_members_details = get_insurance_member_details(pool_id, userid)

            print("add recurring payment")
            payload = {
                "sender_wallet_address": "https://ilp.rafiki.money/alices_stokvel",
                "receiving_wallet_address": wallet,
                "manageUrl": stokvel_members_details.get("stokvel_payment_URI"),
                "previousToken": stokvel_members_details.get("stokvel_payment_token"),
                "payout_value": str(1589 + j),
            }

            response = requests.post(
                node_server_recurring_payment_with_interest, json=payload
            )

            print("RESPONSE: \n", response.json())

            new_token = response.json()["token"]
            new_uri = response.json()["manageurl"]

            update_pool_token_uri(pool_id, userid, new_token, new_uri)
            current_next_date = update_next_contributions_dates(
                current_next_date, pool_id, "Months"
            )
        time.sleep(30)


if __name__ == "__main__":

    # arguments
    pool_id = 1
    user_id_wallets = {
        "1": "https://ilp.interledger-test.dev/test_account",
    }

    run_contribution_simulation(pool_id, user_id_wallets)

    time.sleep(30)

    print("Both methods have completed.")
