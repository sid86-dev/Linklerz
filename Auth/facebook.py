from app.modules import *
from app.db import *
from app.builder import *


def login_with_facebook(email):
    credentials = Users.query.filter_by(email=email).first()
    username = credentials.username
    session['user'] = username
    return username

