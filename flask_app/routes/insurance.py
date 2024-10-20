import requests
from flask import Blueprint, render_template, request

from database.insurance.queries import (
    find_pool_id,
    get_insurance_member_details,
    insert_insurance_member,
    insert_policy,
)
from database.state_manager.queries import delete_employer_state, insert_employer_state
from database.users.queries import (
    find_user_by_number,
    find_wallet_by_userid,
    get_employer_number_from_user,
    update_user_contribution_token_uri,
)
from flask_app.utils.utils import calculate_number_periods
from whatsapp_utils.twilio_messenger import send_notification_message

insurance_bp = Blueprint("insurance", __name__)

NODE_SERVER_INITIATE_GRANT = "http://localhost:3001/payments/user_payment_setup"
NODE_SERVER_CREATE_INITIAL_PAYMENT = (
    "http://localhost:3001/payments/initial_outgoing_payment"
)

BASE_ROUTE = "/insurance"


@insurance_bp.route(BASE_ROUTE, methods=["GET"])
def users() -> str:

    return "USERS API ENDPOINT"


@insurance_bp.route(f"{BASE_ROUTE}/claim_insurance", methods=["POST"])
def claim_insurance() -> str:

    user_number = request.json.get("user_number")
    employer_number = get_employer_number_from_user(user_number=user_number)
    print(employer_number)
    insert_employer_state(employer_number=employer_number, employee_number=user_number)
    send_notification_message(
        to=f"whatsapp:{employer_number}",
        body=f"""Hi, an employee {user_number} is ready to claim their unemployment insurance. Please select one of the following options to proceed:
        1. Authorize claim
        2. Deny claim
        """,
    )

    return "Your claim has been sent to your Employer for verifcation"


@insurance_bp.route(f"{BASE_ROUTE}/process_claim", methods=["POST"])
def process_claim() -> str:

    employer_number = request.json.get("user_number")
    delete_employer_state(employer_number=employer_number)
    employee_number = request.json.get("current_pool")
    send_notification_message(
        to=f"whatsapp:{employee_number}",
        body="Your claim has been Approved by your employer!",
    )

    return "Thank you for your response. We will let your employee know of the outcome."


@insurance_bp.route(f"{BASE_ROUTE}/claim_revoke", methods=["POST"])
def claim_revoke() -> str:

    user_number = request.json.get("user_number")
    employer_number = get_employer_number_from_user(user_number=user_number)
    delete_employer_state(employer_number=employer_number)
    send_notification_message(
        to=f"whatsapp:{employer_number}",
        body="Your claim has been Denied by your employer!",
    )

    return "Thank you for your response. We will let your employee know of the outcome."


@insurance_bp.route(f"{BASE_ROUTE}/onboard_policy", methods=["POST"])
def onboard_policy() -> str:

    pool_name = request.form.get("industry")
    insert_policy(pool_name=pool_name, contribution_amount=50)
    print("STEP")

    employer_number = request.form.get("employer_number")
    user_number = request.form.get("phone_number")
    start_date = "2024-10-20"
    end_date = "2025-10-01"

    number_contribution_periods_between_start_end_date = calculate_number_periods(
        start_date=start_date, end_date=end_date
    )

    policy_amount = 25
    user_id = find_user_by_number(user_number)

    payload = {
        "value": "1",
        "user_contribution": str((policy_amount + 2) * 100),
        "pool_contributions_start_date": start_date,
        "walletAddressURL": "https://ilp.interledger-test.dev/insurance_pool_one",
        "sender_walletAddressURL": find_wallet_by_userid(user_id=user_id),
        "payment_periods": number_contribution_periods_between_start_end_date,  # how many contributions are going to be made
        "payment_period_length": "M",
        "number_of_periods": "1",
        "user_id": user_id,
        "pool_id": find_pool_id(pool_name=pool_name),
    }

    # Insert into poloicies table
    response = requests.post(NODE_SERVER_INITIATE_GRANT, json=payload, timeout=10)

    print(response.json())

    auth_link = response.json()["recurring_grant"]["interact"]["redirect"]
    notification_message = (
        f"Please Authorize the recurring grant using this link: {auth_link}"
    )

    print(notification_message)

    send_notification_message(
        to=f"whatsapp:{user_number}",
        body=notification_message,
    )

    # Extract initial continue URI and token for contributions
    initial_continue_uri_contribution = response.json()["continue_uri"]
    initial_continue_token_contribution = response.json()["continue_token"]["value"]
    initial_payment_quote_contribution = response.json()["quote_id"]

    insert_insurance_member(
        user_id=user_id,
        policy_id=find_pool_id(pool_name=pool_name),
        user_payment_token=initial_continue_token_contribution,
        user_payment_link=initial_continue_uri_contribution,
        user_quote_id=initial_payment_quote_contribution,
        pool_payment_token="",
        pool_payment_link="",
        pool_quote_id="",
        adhoc_contribution_uri="",
        adhoc_contribution_token="",
        value=policy_amount,
    )

    insert_employer_state(employer_number=employer_number, employee_number=user_number)


@insurance_bp.route(f"{BASE_ROUTE}/user_interactive_grant_response", methods=["GET"])
def user_interactive_grant_handle() -> str:

    # Extract query parameters
    result = request.args.get("result")  # For grant_rejected
    hash_value = request.args.get("hash")  # For the confirmation hash
    interact_ref = request.args.get(
        "interact_ref"
    )  # For the interact_ref when confirmed
    user_id = request.args.get("user_id")
    pool_id = request.args.get("pool_id")

    if result == "grant_rejected":

        return "Thank you for your response. We will not continue with contributions"

    if hash_value and interact_ref:

        insurance_members_details = get_insurance_member_details(pool_id, user_id)

        payload = {
            "quote_id": insurance_members_details.get("user_quote_id"),
            "continueUri": insurance_members_details.get("user_payment_URI"),
            "continueAccessToken": insurance_members_details.get("user_payment_token"),
            "walletAddressURL": find_wallet_by_userid(user_id=user_id),
            "interact_ref": interact_ref,
        }

        print("USER PAYLOAD: \n", payload)

        response = requests.post(
            NODE_SERVER_CREATE_INITIAL_PAYMENT, json=payload, timeout=10
        )

        print("USER RESPONSE: \n", response.json())

        new_token = response.json()["token"]
        new_uri = response.json()["manageurl"]

        update_user_contribution_token_uri(pool_id, user_id, new_token, new_uri)

        return "Thank you for your response. We continue with your contributions."


@insurance_bp.route(f"{BASE_ROUTE}/claims", methods=["GET"])
def claims_template():
    return render_template("items.html")
