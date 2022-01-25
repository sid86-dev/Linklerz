<<<<<<< HEAD
data = {
    'name': 'SidDharth',
    'username': 'sid999'
}

import random

print(data['name'])

for item in data:
    data[item] = data[item].lower()


def createUsername(get_fullname):
    num = random.randint(11, 500)

    punctions = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    fullname = ''

    for letter in get_fullname:
        if letter not in punctions:
            fullname += letter

    fullname.replace(" ", "")

    username = f"{fullname[:4]}{fullname[-3:]}{num}"

    return username


print(createUsername('sidd%$harth    Ro**y'))
=======
from Auth.twilio_ import *
import threading
from app.builder import *


def code_verification(userid):
    code = gen_code()
    phone = '918389046987'
    # send sms code
    threading.Thread(target=send_sms_code, args=(code, phone,), name='thread_function').start()

    # add cache to redis
    threading.Thread(target=add_cache, args=(
        userid, code,), name='thread_function').start()

if __name__ == '__main__':
    link = buildqr('sid86_','sid86_')
    print(link)
>>>>>>> e86fff60b767e4a0990919c620b58519543824f2
