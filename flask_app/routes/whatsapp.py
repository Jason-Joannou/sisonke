from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

whatsapp_bp = Blueprint("whatsapp", __name__)

BASE_ROUTE = "/whatsapp"


@whatsapp_bp.route(BASE_ROUTE, methods=["POST"])
def whatsapp() -> str:
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From", "")

    twiml = MessagingResponse()
    twiml.message(incoming_msg)  # Create the TwiML message.

    return str(twiml)
