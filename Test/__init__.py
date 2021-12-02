from Test.redis_ import*
from Test.twilio_ import*

if __name__ == '__main__':
   user_id = 'sdc8s44'

   code = gen_code()
   send_sms_code(code)

   add_cache(user_id, code)