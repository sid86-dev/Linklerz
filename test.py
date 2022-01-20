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