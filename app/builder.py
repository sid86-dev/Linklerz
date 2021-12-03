from app.db import *
from app.modules import *
# Auth
from Auth.facebook import *
from Auth.twilio_ import *
from Auth.google import *
from Auth.redis_ import *

s = URLSafeTimedSerializer('Linklerz.li')


# global functions
def encrypt(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash


@lru_cache(maxsize=5)
def get_credentials(variable):
    credentials = Users.query.filter_by(username=variable).first()

    return credentials


def entry(username_get, userpass_encrypt, useremail_get):
    w = gen_word()
    userid = f"{w}{random.randint(1000, 9999)}"
    entry = Users(username=username_get,
                  password=userpass_encrypt,
                  email=useremail_get,
                  plan='free',
                  confirmation='no',
                  linktype="",
                  linkurl="",
                  userid=userid,
                  theme='DEFAULT THEME',
                  auth='no',
                  phone="")
    db.session.add(entry)
    db.session.commit()


def verify_user(userid, phone):
    N = 80
    authid = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=N))
    code = gen_code()

    # send sms code
    threading.Thread(target=send_sms_code,
                     args=(
                         code,
                         phone,
                     ),
                     name='thread_function').start()

    # add cache to redis
    threading.Thread(target=add_authid,
                     args=(
                         userid,
                         authid,
                     ),
                     name='thread_function').start()
    return redirect(f"/login?auth={authid}&userid={userid}&phone={phone}")


def get_linktype(linktype):
    list_lintype = linktype.split(">")
    return list_lintype


def gen_token(email):
    token = s.dumps(email, salt='email-confirm')
    return token


def gen_word():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=4)
        rand_letters = "".join(rand_letters)
        return rand_letters


def cache_details(userid):
    r = redis.Redis(host=params['redis_host'],
                    port=params['redis_port'],
                    password=params['redis_password'])

    r.mset({'id': userid})

    # r.psetex('name', 1000, "siddharth")  # milisecond

    # print(r.get('name'))
    # print(r.get('age'))

    if (r.exists('id')):
        return r.get('id')
    else:
        return "cannot find the key"
