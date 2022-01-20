from app.modules import *
from app.db import *
from app.builder import *
from app.settings import *

GOOGLE_CLIENT_ID = '983066542456-1gsapcu2uta11718lp1l6j9c7f5pnf5k.apps.googleusercontent.com'
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, 'client_secret.json')
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email', 'openid'
    ],
    redirect_uri=uri)


def login_with_google(info):
    email = info['email']
    credentials = Users.query.filter_by(email=email).first()
    username = credentials.username
    session['user'] = username
    return username


def signup_with_google(info):
    email = info['email'].lower()
    f_name = info['given_name'].lower()
    l_name = info['family_name'].lower()

    num = random.randint(11, 500)
    username = f"{f_name[:4]}{l_name}{num}"

    token = gen_token(email)
    final_token = f"https://lerz.herokuapp.com/confirm/{token}"
    # entry to database
    threading.Thread(target=entry,
                     args=(username, "google_auth", email),
                     name='thread_function').start()

    # send confirmation email
    threading.Thread(target=send_email,
                     args=(email, username, final_token),
                     name='thread_function').start()
    # add username session variable
    session['user'] = username

    return email
