from twilio.rest import Client
import config

def main(body_text):
    ACCOUNT_SID = config.twilio_sid
    AUTH_TOKEN = config.twilio_auth
    sms_from = config.twilio_from
    sms_to = config.twilio_to
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms():
        message = client.messages.create(
            to=sms_to,
            from_=sms_from,
            body=body_text)
        print("Sending text. ID:", message.sid)

    return send_sms()
