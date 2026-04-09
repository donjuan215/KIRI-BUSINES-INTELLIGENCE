import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM")
TO_NUMBER   = os.getenv("TWILIO_TO")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp(message):
    msg = client.messages.create(
        from_=FROM_NUMBER,
        body=message,
        to=TO_NUMBER
    )
    print("✅ WhatsApp enviado SID:", msg.sid)
    return msg.sid