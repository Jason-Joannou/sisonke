from flask import Blueprint, request

insurance_bp = Blueprint("insurance", __name__)


BASE_ROUTE = "/insurance"


@insurance_bp.route(BASE_ROUTE, methods=["GET"])
def users() -> str:

    return "USERS API ENDPOINT"
