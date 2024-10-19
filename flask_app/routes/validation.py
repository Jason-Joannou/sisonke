import requests
from flask import Blueprint, request

validation_bp = Blueprint("validation", __name__)

BASE_ROUTE = "/validation"
ILP_VALIDATION_ENDPOINT = "http://localhost:3001/validation/wallet"


@validation_bp.route(f"{BASE_ROUTE}/wallet", methods=["POST"])
def validate_wallet() -> str:

    wallet_address = request.json.get(
        "user_input",
    )
    response = requests.post(
        ILP_VALIDATION_ENDPOINT, json={"wallet_address": wallet_address}, timeout=10
    )
    print(response)
    msg = response.json().get("message")
    return str(msg)
