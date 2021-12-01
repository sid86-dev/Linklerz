from app import settings

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
    userid = f"{w}{random.randint(1000,9999)}"
    entry = Users(username=username_get, password=userpass_encrypt,  email=useremail_get, plan='free',
                  confirmation='no', linktype="", linkurl="", userid=userid, theme='DEFAULT THEME')
    db.session.add(entry)
    db.session.commit()


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