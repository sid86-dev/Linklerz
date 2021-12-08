from Test.twilio_ import *
import threading


def code_verification(userid):
    code = gen_code()
    phone = '918389046987'
    # send sms code
    threading.Thread(target=send_sms_code, args=(code, phone,), name='thread_function').start()

    # add cache to redis
    threading.Thread(target=add_cache, args=(
        userid, code,), name='thread_function').start()


if __name__ == '__main__':
    user_id = 'sdc11s44'

    code_verification(user_id)

    while True:
        code = get_cache(user_id)
        i = input("Enter the code: ")

        try:
            if int(code.decode('ascii')) == int(i):
                print("Verification Successfull")

            elif code == 'Code Expired':
                print('Code Expired')

            else:
                print('Verification Failed')


        except:
            print('Verification Failed')
