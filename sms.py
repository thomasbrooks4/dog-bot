from private_constants import *
from constants import *
from twilio.rest import Client

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send(to_number, message_body):
    message = client.messages.create(
        to = to_number,
        from_ = BOT_NUMBER,
        body = SMS_HEADER + message_body + SMS_FOOTER
    )
