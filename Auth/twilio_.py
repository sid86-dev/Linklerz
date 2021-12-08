from twilio.rest import Client
from Test.redis_ import *
import random

twilio_recover_code = 'FvSlfeiRjbH600qcyq2CtikudV1Ad2oFS6UOtXKt'
account_sid = "AC27a055842d8fbdbc2943caf2d5962165"
auth_token = "271e96871fffe116253bd65620fddb4f"
twilio_number = '+18504077760'


def send_sms_code(code, phone):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your Linklerz security code is {code}",
        from_=twilio_number,
        to=f'+{phone}'
    )

    return message.sid


def gen_code():
    code = ''
    for i in range(4):
        n = str(random.randrange(0, 9))
        code += n
    return code


if __name__ == '__main__':
    user_id = 'sdc8s44'
    phone = '918389046987'

    code = gen_code()
    send_sms_code(code, phone)

    # add_cache(user_id, code)
