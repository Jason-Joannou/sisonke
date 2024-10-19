from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from database.utils import extract_whatsapp_number

employer_bp = Blueprint("employer", __name__)
BASE_ROUTE = "/employer"


@employer_bp.route(f"{BASE_ROUTE}/employer_state", methods=["POST"])
def employers() -> str:

    user_number = request.json.get("user_number")
    user_number = extract_whatsapp_number(from_number=user_number)

    state = {
        "tag": "employer_state",
        "message": f"""
        Your employee is claiming their unemployment insurance. Please select one of the following options to proceed:
        1. Confirm {user_number}
        2. Revoke {user_number}
        """,
        "valid_actions": ["1", "2"],
        "action_requests": {
            "1": "/insurance/process_claim",
            "2": "/insurance/claim_revoke",
        },
    }

    return state
