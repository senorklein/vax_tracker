import json

###
"""
Create a config.json file with the actual values of each the below settings
"""
#
config = {
        "twilio_account_sid": "unknown",
        "twilio_auth_token": "unknown",
        "twilio_sms_number": "unknown",
}


try:
    f = open("./config.json", "+r")
    config_txt = f.readlines()
    config_dict = json.loads(" ".join(config_txt))

    config.update(config_dict)
except Exception as e:
    print(f"error {e}")
    print("config.json not found")
    exit()


