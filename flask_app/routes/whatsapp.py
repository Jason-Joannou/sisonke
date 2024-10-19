from flask import Blueprint, request

from whatsapp_utils.state_manager import MessageStateManager

whatsapp_bp = Blueprint("whatsapp", __name__)

BASE_ROUTE = "/whatsapp"


@whatsapp_bp.route(BASE_ROUTE, methods=["POST"])
def whatsapp() -> str:
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From", "")

    state_manager = MessageStateManager(user_number=from_number)
    msg = state_manager.processes_user_request(user_action=incoming_msg)

    return str(msg)
