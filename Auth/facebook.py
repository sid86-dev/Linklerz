from app.modules import *
from app.db import *
from app.builder import *


def login_with_facebook(email):
    credentials = Users.query.filter_by(email=email).first()
    username = credentials.username
    session['user'] = username
    return username


def signup_with_facebook(email, name):
    num = random.randint(11, 500)
    username = f"{name[:4]}{name[-3:-1]}{num}"

    token = gen_token(email)
    final_token = f"https://lerz.herokuapp.com/confirm/{token}"

    # entry to database
    threading.Thread(target=entry, args=(
        username, "facebook_auth", email), name='thread_function').start()

    # send confirmation email
    threading.Thread(target=send_email, args=(
        email, username, final_token), name='thread_function').start()

    session['user'] = username
