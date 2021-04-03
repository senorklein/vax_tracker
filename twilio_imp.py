import os
from twilio.rest import Client
from config import config


def send_sms(number, message):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = config["twilio_account_sid"]
    auth_token = config["twilio_auth_token"]
    from_number = config["twilio_sms_number"]
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=message,
                         from_=from_number,
                         to=number
                     )

