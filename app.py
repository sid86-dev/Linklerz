# flask modules
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine

# python tool modules
import hashlib
import string
import random
import threading
import json

# local modules
from mail.delete_mailer import delete_email
from mail.mailer import send_email
from api.api import api_conv

with open('config.json', 'r') as f:
    params = json.load(f)["params"]


URI = params['database_uri']

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


# global functions

def encrypt(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash


def entry(username_get, userpass_encrypt, useremail_get):
    entry = Users(username=username_get, password=userpass_encrypt,  email=useremail_get, plan='free', confirmation='no', linktype="", linkurl=""
                  )
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
        linktype = credentials.linktype
        list_linktype = get_linktype(linktype)
        return render_template('home.html', list_linktype=list_linktype, credentials=credentials)
    return redirect('/login')

# edit route
@app.route('/edit')
def edit():
    username = session['user']
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
    try:
        if ('user' in session and session['user'] == username):
            credentials = Users.query.filter_by(username=username).first()
            return render_template('profile.html', credentials=credentials)
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
        return redirect('/edit')
    return redirect('/edit')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            return redirect(f'/home/{username}')
    except:
        login_fail = ""
        if request.method == 'POST':
            username_get = request.form.get('username').lower()
            userpass_get = request.form.get('password').lower()
            userpass_encrypt = encrypt(userpass_get)
            try:
                credentials = Users.query.filter_by(
                    password=userpass_encrypt).first()
                if credentials.username == username_get and credentials.password == userpass_encrypt:
                    # set the session variable
                    session['user'] = credentials.username
                    return redirect(f'/home/{credentials.username}')
                else:
                    login_fail = "Username and Password do not match"
                    return render_template('login.html', login_fail=login_fail)
            except:
                login_fail = "Username and Password do not match"
                return render_template('login.html', login_fail=login_fail)
        return render_template('login.html', login_fail=login_fail)

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_exist = "NO"
    if request.method == 'POST':
        useremail_get = request.form.get('email').lower()
        username_get = request.form.get('username').lower()
        userpass_get = request.form.get('password').lower()
        confirmpass_get = request.form.get('password_confirm').lower()
        try:
            credentials = Users.query.filter_by(username=username_get).first()
            username = credentials.username
            user_exist = "YES"
            return render_template('signup.html', user_exist=user_exist)
        except:
            user_exist = "NO"
            if userpass_get == confirmpass_get:
                try:
                    credentials = Users.query.filter_by(
                        email=useremail_get).first()
                    useremail = credentials.email
                    email_exist = "yes"
                    return render_template('signup.html', user_exist=user_exist, email_exist=email_exist)
                except:
                    userpass_encrypt = encrypt(userpass_get)
                    session['user'] = username_get

                    token = gen_token(useremail_get)
                    final_token = f"https://lerz.herokuapp.com/confirm/{token}"
                    # entry to database
                    threading.Thread(target=entry, args=(username_get, userpass_encrypt, useremail_get), name='thread_function').start()

                    # send confirmation email
                    threading.Thread(target=send_email, args=(useremail_get, username_get, final_token), name='thread_function').start()

                    return render_template('confirm.html', email_address=useremail_get)
            else:
                match = "NO"
                return render_template('signup.html', user_exist=user_exist, match=match)
    return render_template('signup.html', user_exist=user_exist)


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
@app.route('/deletelog/<string:username>')
def delete_account(username):
    if ('user' in session and session['user'] == username):
        keyword = gen_word()
        word = f"{username}{keyword}"
        return render_template('delete.html', username=username, word=word)

def delete_data(username):
    credentials = Users.query.filter_by(username=username).first()
    # delete data
    email = credentials.email
    db.session.delete(credentials)
    db.session.commit()
    return email

@app.route('/deletecheck/<string:username>/<string:word>', methods=['GET', 'POST'])
def delete_check(username, word):
    if request.method == "POST":
        inputtext = request.form.get('inputtext')
        if inputtext != word:
            return redirect(f'/deletelog/{username}')
        else:
            email = delete_data(username)
            # send email
            delete_email(email, username)

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
        


# render links
@app.route(
    '/li.<string:username>')
def link(username):
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
    return render_template('dark_theme.html', credentials=credentials, linkdic=linkdic)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
