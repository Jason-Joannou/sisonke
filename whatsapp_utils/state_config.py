from whatsapp_utils.message_config import (
    INSURANCE_SERVICES,
    REGISTERED_NUMBER,
    UNREGISTERED_NUMBER,
)

MESSAGE_STATES = {
    "base_state": ["Hi", "Hello", "hi", "hello"],
    "unrecognized_state": "Sorry, I don't understand that action. The following actions are allowed in this state:\n",
    UNREGISTERED_NUMBER["tag"]: UNREGISTERED_NUMBER,
    REGISTERED_NUMBER["tag"]: REGISTERED_NUMBER,
    INSURANCE_SERVICES["tag"]: INSURANCE_SERVICES,
}
