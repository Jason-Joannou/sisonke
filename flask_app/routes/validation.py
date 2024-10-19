import requests
from flask import Blueprint, request

from database.users.queries import insert_user

validation_bp = Blueprint("validation", __name__)

BASE_ROUTE = "/validation"
EXPRESS_VALIDATION_ENDPOINT = "http://localhost:3001/validation/wallet"
TIGER_BEETLE_ENDPOINT_PERSON_ENTITY = (
    "http://localhost:3001/tiger-beetle/createPersonEntity"
)


@validation_bp.route(f"{BASE_ROUTE}/wallet", methods=["POST"])
def validate_wallet() -> str:

    wallet_address = request.json.get(
        "user_input",
    )
    user_number = request.json.get("user_number")
    response = requests.post(
        EXPRESS_VALIDATION_ENDPOINT, json={"wallet_address": wallet_address}, timeout=10
    )

    if response.status_code == 200:
        # Tiger Beetle Account
        response = requests.get(TIGER_BEETLE_ENDPOINT_PERSON_ENTITY, timeout=10)
        if response.status_code != 200:
            return "Something went wrong, please try sending the action again."

        person_entity_id = response.json().get("personEntityId")
        insert_user(
            user_number=user_number,
            user_wallet=wallet_address,
            tiger_beetle_id=person_entity_id,
        )

        return "Thank you for your submission! You have been added to the system"

    msg = response.json().get("message")
    return str(msg)
