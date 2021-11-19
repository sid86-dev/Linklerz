# flask modules
from os import abort
import re
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine

# python tool modules
from functools import lru_cache
import hashlib
import string
import random
import threading
import json
import requests

# external modules
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

# local modules
from mail.delete_mailer import delete_email
from mail.mailer import send_email
from api.api import api_conv
from google_auth import*


with open('config.json', 'r') as f:
    params = json.load(f)["params"]

# app variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# cloud db uri
URI = params['database_uri_1']

e = create_engine(
    URI, pool_recycle=1800)
app = Flask(__name__)

app.secret_key = params['app_key']
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

s = URLSafeTimedSerializer('Linklerz.li')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    plan = db.Column(db.String(12), nullable=False)
    confirmation = db.Column(db.String(20), nullable=False)
    linktype = db.Column(db.String(500), nullable=False)
    linkurl = db.Column(db.String(500), nullable=False)
    userid = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(50), nullable=False)


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

# index route


@app.route('/')
def index():
    return render_template('index.html')

# error handler route


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# setting route


@app.route('/settings/<string:username>')
def settings(username):
    if ('user' in session and session['user'] == username):
        return render_template('settings.html', username=username)
    else:
        return render_template('404.html')


# home route
@app.route('/home/<string:username>')
def home(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        # credentials = get_credentials(username)
        linktype = credentials.linktype
        list_linktype = get_linktype(linktype)
        return render_template('home.html', list_linktype=list_linktype, credentials=credentials)
    return redirect('/login')


# edit route
@app.route('/edit/<string:username>')
def edit(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)

        linkdic = {}
        for key in list_linktype:
            for value in list_linkurl:
                linkdic[key] = value
                list_linkurl.remove(value)
                break

        plan = credentials.plan
        if plan == "free":
            num = 5 - len(list_linktype)
        else:
            num = 10 - len(list_linktype)
        return render_template('edit.html', linkdic=linkdic, num=num, credentials=credentials)
    return redirect('/login')


# profile route
@app.route("/profile/<string:username>", methods=['GET', 'POST'])
def profile(username):
    error = ''
    if request.method == "POST":
        get_username = request.form.get('username')
        try:
            if get_username == username:
                return redirect(f'/home/{get_username}')
            credentials = Users.query.filter_by(username=get_username).first()
            # to verify
            email = credentials.email

            # return to the same route with error
            credentials = Users.query.filter_by(username=username).first()
            error = 'Username already exist'
            return render_template('profile.html', credentials=credentials, error=error)
        except:
            credentials = Users.query.filter_by(username=username).first()
            credentials.username = get_username
            db.session.commit()
            # handle log info
            session.pop('user')
            session['user'] = get_username
            return redirect(f'/home/{get_username}')

    try:
        if ('user' in session and session['user'] == username):
            credentials = Users.query.filter_by(username=username).first()
            return render_template('profile.html', credentials=credentials, error=error)
    except:
        return redirect('/login')

# saving data


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == "POST":
        username = session['user']
        if ('user' in session and session['user'] == username):
            credentials = Users.query.filter_by(username=username).first()
            linktype = credentials.linktype
            list_linktype = get_linktype(linktype)
            # print(list_linktype)
            # get old edited inklist
            oldlist_linktype = []
            oldlist_linkurl = []
            for item in list_linktype:
                old_linktype = request.form.get(f'{item}type', '')
                old_linkurl = request.form.get(item, '')
                if old_linktype != '' and old_linkurl != '':
                    oldlist_linktype.append(old_linktype)
                    oldlist_linkurl.append(old_linkurl)

            # get new edited inklist
            new_linktype = request.form.get(f'new_linktype', '')
            new_linkurl = request.form.get(f'new_linkurl', '')

            if new_linktype != "" and new_linkurl != "":
                oldlist_linktype.append(new_linktype)
                oldlist_linkurl.append(new_linkurl)

            x = ">".join(oldlist_linktype)
            y = ">".join(oldlist_linkurl)

            credentials.linktype = x
            credentials.linkurl = y

            db.session.commit()
            return redirect(f'/home/{username}')

# delete route


@app.route('/delete/<link_name>')
def delete(link_name):
    username = session['user']
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)
        # get index and delete with the index
        index = list_linktype.index(link_name)
        list_linktype.remove(link_name)
        list_linkurl.remove(list_linkurl[index])

        x = ">".join(list_linktype)
        y = ">".join(list_linkurl)

        credentials.linktype = x
        credentials.linkurl = y

        db.session.commit()
        return redirect(f'/edit/{username}')
    return redirect(f'/edit/{username}')

# login route


@app.route('/login', methods=['GET', 'POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            return redirect(f'/home/{username}')
    except:
        login_fail = ""
        login_type = "Member"
        if request.method == 'POST':
            username_get = request.form.get('username').lower()
            # if '.com' in username_get:
                # username_get = username_get.lower()
            userpass_get = request.form.get('password')
            userpass_encrypt = encrypt(userpass_get)
            try:
                if '@' in username_get:
                    credentials = Users.query.filter_by(
                        email=username_get).first()
                    password = credentials.password
                    if password == 'google_auth':
                        login_fail = "Please sign in using Google"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type, authorization_url=authorization_url)

                    elif password == userpass_encrypt:
                        session['user'] = credentials.username
                        return redirect(f'/home/{credentials.username}')
                    else:
                        login_fail = "Username and Password do not match"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type, authorization_url=authorization_url)

                elif '@' not in username_get:
                    credentials = Users.query.filter_by(
                        username=username_get).first()
                    if credentials.password == userpass_encrypt:
                        # set the session variable
                        session['user'] = credentials.username
                        return redirect(f'/home/{credentials.username}')
                    else:
                        login_fail = "Username and Password do not match"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type, authorization_url=authorization_url)
            except:
                login_fail = "Username and Password do not match"
                return render_template('login.html', login_fail=login_fail, login_type=login_type, authorization_url=authorization_url)
        return render_template('login.html', login_fail=login_fail, login_type=login_type, authorization_url=authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    try:
        username = login_with_google(id_info)
        return redirect(f'/home/{username}')
    except:
        email = signup_with_google(id_info)
        return redirect(f'/datapolicy/{email}')


@app.route('/datapolicy/<string:email>', methods=['GET', 'POST'])
def datapolicy(email):
    if request.method == "POST":
        return render_template('confirm.html', email_address=email)
    arg = ''
    credentials = {'username': 'Data Policy', 'email': email}
    return render_template('google_policy.html', credentials=credentials, arg=arg)


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
    threading.Thread(target=entry, args=(
        username, "google_auth", email), name='thread_function').start()

    # send confirmation email
    threading.Thread(target=send_email, args=(
        email, username, final_token), name='thread_function').start()
    # add username session variable
    session['user'] = username

    return email

# signup route


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    user_exist = "NO"
    if request.method == 'POST':
        useremail_get = request.form.get('email').lower()
        userpass_get = request.form.get('password')
        confirmpass_get = request.form.get('password_confirm')
        full_name = request.form.get('username').lower()
        num = random.randint(11, 500)
        username_get = f"{full_name[:4]}{full_name[-3:]}{num}"
        try:
            credentials = Users.query.filter_by(username=username_get).first()
            username = credentials.username
            user_exist = "YES"
            return render_template('signup.html', user_exist=user_exist, authorization_url=authorization_url)
        except:
            user_exist = "NO"
            if userpass_get == confirmpass_get:
                try:
                    credentials = Users.query.filter_by(
                        email=useremail_get).first()
                    useremail = credentials.email
                    email_exist = "yes"
                    return render_template('signup.html', user_exist=user_exist, email_exist=email_exist, authorization_url=authorization_url)
                except:
                    userpass_encrypt = encrypt(userpass_get)
                    session['user'] = username_get

                    token = gen_token(useremail_get)
                    final_token = f"https://lerz.herokuapp.com/confirm/{token}"
                    # entry to database
                    threading.Thread(target=entry, args=(
                        username_get, userpass_encrypt, useremail_get), name='thread_function').start()

                    # send confirmation email
                    threading.Thread(target=send_email, args=(
                        useremail_get, username_get, final_token), name='thread_function').start()

                    return render_template('confirm.html', email_address=useremail_get)
            else:
                match = "NO"
                return render_template('signup.html', user_exist=user_exist, match=match, authorization_url=authorization_url)
    return render_template('signup.html', user_exist=user_exist, authorization_url=authorization_url)


# email send
@app.route('/sendconfirm/<string:email>')
def emailconfirm(email):
    try:
        username = session['user']
        token = gen_token(email)
        final_token = f"https://lerz.herokuapp.com/confirm/{token}"

        send_email(email, username, final_token)
        return render_template('confirm.html', email_address=email)
    except:
        return redirect('/error')


@app.route('/confirm/<string:token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm', max_age=172800)
    # data process
    credentials = Users.query.filter_by(email=email).first()
    credentials.confirmation = "yes"
    db.session.commit()
    return render_template('confirm_email.html', credentials=credentials)

# delete account


@app.route('/deletelog/<string:email>/<string:username>')
def delete_account(email, username):
    if ('user' in session and session['user'] == username):
        keyword = gen_word()
        word = f"{username}{keyword}"
        # credentials = Users.query.filter_by(username=username).first()
        return render_template('delete.html', username=username, word=word, email=email)


def delete_data(username):
    credentials = Users.query.filter_by(username=username).first()
    # delete data
    # email = credentials.email
    db.session.delete(credentials)
    db.session.commit()
    # return email


@app.route('/deletecheck/<string:username>/<string:word>/<string:email>', methods=['GET', 'POST'])
def delete_check(username, word, email):
    if request.method == "POST":
        inputtext = request.form.get('inputtext')
        if inputtext != word:
            return redirect(f'/deletelog/{username}')
        else:
            # query to database
            threading.Thread(target=delete_data, args=(
                username,), name='thread_function').start()

            # send delete email
            threading.Thread(target=delete_email, args=(
                email, username,), name='thread_function').start()

            return redirect('/logout')
    return redirect('/login')

# Logging out


@app.route('/logout')
def logout():
    try:
        session.pop('user')
        return redirect('/login')
    except:
        return render_template('404.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    login_fail = ""
    login_type = "Admin"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == params['admin_username'] and password == params['admin_password']:
            session['admin_user'] = params['admin_username']
            return redirect('/admin_dashboard')
        login_fail = "Username and Password do not match"
    try:
        return render_template('login.html', login_fail=login_fail, login_type=login_type)
    except:
        return render_template('404.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    try:
        if session['admin_user'] == params['admin_username']:
            credentials = Users.query.filter_by().all()
            return render_template('admin_dashboard.html', credentials=credentials)
    except:
        return redirect('/admin')

# render links


@app.route(
    '/li.<string:username>')
def link(username):
    credentials = Users.query.filter_by(username=username).first()
    linktype = credentials.linktype
    linkurl = credentials.linkurl
    list_linktype = get_linktype(linktype)
    list_linkurl = get_linktype(linkurl)
    theme = credentials.theme

    linkdic = {}
    for key in list_linktype:
        for value in list_linkurl:
            linkdic[key] = value
            list_linkurl.remove(value)
            break
    # return render_template('dark_theme.html', credentials=credentials, linkdic=linkdic)
    return render_template(f'{params[credentials.theme]}.html', credentials=credentials, linkdic=linkdic)


@app.route('/appearance/<string:username>', methods=['GET', 'POST'])
def appearance(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        if request.method == 'POST':
            theme = request.form.get('slider')
            # print((theme).upper())
            credentials.theme = theme
            db.session.commit()
            return redirect(f'/home/{{credentials.username}}')
        return render_template('appearance.html', credentials=credentials)
    else:
        return redirect('/login')


# @app.route('/bug')
# def bug():
#     credentials = Users.query.filter_by(username='sid86_').first()
#     password = encrypt(password='Siddharth8604')
#     credentials.password = password
#     db.session.commit()
#     return 'Done'



# api for linklerz.li
@app.route(
    '/api/<string:username>')
def api(username):
    try:
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)

        linkdic = {}
        for key in list_linktype:
            for value in list_linkurl:
                linkdic[key] = value
                list_linkurl.remove(value)
                break

        return jsonify(api_conv(linkdic))
    except:
        return jsonify(username='Does not exist')


@app.route('/community')
def community():
    return render_template('community_select.html')


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    fixed_credentials = {'username': 'Help Center'}
    arg = ''
    if request.method == 'POST':
        recoveryinput = request.form.get('recoveryinput')
        print(recoveryinput)
        try:
            if '@' in recoveryinput:
                credentials = Users.query.filter_by(
                    email=recoveryinput).first()
                email = credentials.email
                username = credentials.username
            else:
                credentials = get_credentials(recoveryinput)
                email = credentials.email
                username = credentials.username
            arg = 'success'
            delete_email(email, username)
            return render_template('recovery.html', credentials=fixed_credentials, arg=arg)
        except:
            arg = 'Username or Email does not exist'
            return render_template('recovery.html', credentials=fixed_credentials, arg=arg)
    return render_template('recovery.html', credentials=fixed_credentials, arg=arg)


# if __name__ == "__main__":
    # app.run(host="0.0.0.0")

if __name__ == "__main__":
    app.run(debug=True)
