from app.db import *
from app.modules import *
# Auth
from Auth.facebook import *
from Auth.twilio_ import *
from Auth.google import *
from Auth.redis_ import *
from qr_code.genqr import *

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

    link = buildqr(userid, username_get)

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
                  phone="",
                  qrlink=link)
    db.session.add(entry)
    db.session.commit()


def createUsername(get_fullname):
    num = random.randint(11, 500)

    punctions = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    fullname = ''

    for letter in get_fullname:
        if letter not in punctions:
            fullname += letter

    fullname.replace(" ", "")

    username = f"{fullname[:4]}{fullname[-3:]}{num}"

    username.replace(" ", "")

    return username

# async def getUserData(credentials):
#     await asyncio.gather(
#         userid = getUserid(credentials),
#         userpass = getUserpass(credentials),
#     )  # 1s + 1s = over 1s
#     print(userid, userpass)
#     # return {'userid':userid, 'userpass':userpass}

def verify_phone(phone):
    code = gen_code()
    
    # send sms code
    send_sms_code(code,phone)

    # add cache to redis
    threading.Thread(target=phoneCode,
                     args=(
                         phone,
                         code,
                     ),
                     name='thread_function').start()




def verify_user(userid, phone):
    N = 110
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

    # add cache to redis
    threading.Thread(target=add_cache,
                     args=(
                         authid[:5],
                         code,
                     ),
                     name='thread_function').start()

    return authid

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


def uploadimage(title):

    CLIENT_ID = "b53e11fbba52bc8"
    PATH = './qr_code/qr.png'

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    link = uploaded_image.link

    return link

def buildqr(id, username):

    gen_qr(f"https://shwt.xyz/{username}")

    link = uploadimage(f'{id}qrcode')

    return link

def getUserData(Users,username):
    credentials = Users.query.filter_by(username=username).first()

    return credentials

def sendcode(phone):
    code = gen_code()
    api = 'YbDHcts0r2MxX61fJNegnCopGj7kEuzPK3ASyF5T9mvqOwaLldxlqIitAPrp1nXKNQGeOh8MzSsE0uTB'
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = "message=Your%20linklerz%20security%20code%20is%20{code}&language=english&route=q&numbers={phone}"
    headers = {
        'authorization': api,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)



def sortLinkname(data):
    link_name = re.sub(r"\s+", "", data['name'], flags=re.UNICODE)
    return link_name.capitalize()



