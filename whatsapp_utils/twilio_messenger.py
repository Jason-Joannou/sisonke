from whatsapp_utils.twilio_client import TwilioClient

twilio_client = TwilioClient()


def send_notification_message(to: str, body: str):
    twilio_client.send_mesage_notification(to, body)


def send_conversational_message(message: str):
    return twilio_client.send_conversational_message(message)
