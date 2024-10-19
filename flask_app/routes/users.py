from flask import Blueprint, request

users_bp = Blueprint("users", __name__)

TIGER_BEETLE_ENDPOINT = "http://localhost:3001/tiger-beetle"

BASE_ROUTE = "/users"


@users_bp.route(BASE_ROUTE, methods=["GET"])
def users() -> str:

    return "USERS API ENDPOINT"
