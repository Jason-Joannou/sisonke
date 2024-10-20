import os

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()


import os

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()


class TwilioClient:

    def __init__(self):
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_TOKEN"))
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def send_mesage_notification(self, to: str, body: str) -> None:
        self.client.messages.create(to=to, from_=self.from_number, body=body)

    def send_conversational_message(self, message: str) -> str:
        twiml = MessagingResponse()
        twiml.message(message)  # Create the TwiML message.
        return str(twiml)  # Return the entire TwiML response as a string.
