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
