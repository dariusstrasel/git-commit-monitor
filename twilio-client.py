import twilio.rest
import config


def main():
    ACCOUNT_SID = config.twilio_sid
    AUTH_TOKEN = config.twilio_auth
    sms_from = config.twilio_from
    sms_to = config.twilio_to
    client = twilio.rest.TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(body_text):
        message = client.messages.create(
            to=sms_to,
            from_=sms_from,
            body=body_text)
        print(message.sid)

    return send_sms("Hello world!")

if __name__ == '__main__':
    main()