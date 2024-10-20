from flask import Blueprint, request

from database.state_manager.queries import delete_employer_state, insert_employer_state
from database.users.queries import get_employer_number_from_user
from whatsapp_utils.twilio_messenger import send_notification_message

insurance_bp = Blueprint("insurance", __name__)


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
