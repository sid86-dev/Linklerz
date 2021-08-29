from typing_extensions import final
from flask import Flask, render_template, session, request
# from flask_sqlalchemy import SQLAlchemy
import json

from werkzeug.utils import redirect
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

from itsdangerous import URLSafeTimedSerializer

import sqlite3

import hashlib

from mailer import send_email

app = Flask(__name__)
app.secret_key = 'my-secret-key'

s = URLSafeTimedSerializer('Linklerz.li')


def gen_token(email):
    token = s.dumps(email, salt='email-confirm')
    return token


def delete_data(delete_name):
    username = session['user']

    conn = sqlite3.connect('linklerz_.db')

    c = conn.cursor()

    c.execute(f"SELECT * FROM details WHERE username='{username}'")

    data = c.fetchone()

    # print(data)
    length = len(data)

    names = []
    links = []

    lst = []

    for i in range(1, length):
        lst.append(data[i])

    my_dic = {}

    # print(lst)

    for i in range(len(lst)):
        if ">" in lst[i]:
            item = lst[i]
            seperate = item.split('>')
            # print(seperate)
            my_dic[seperate[0]] = seperate[1]
        else:
            my_dic[""] = ""

    my_dic.pop(delete_name)

    # print(my_dic)

    final_lst = []
    for item in my_dic:
        if item != "":
            final_lst.append(f"{item}>{my_dic[item]}")

    return final_lst


def get_links(user):
    conn = sqlite3.connect('linklerz_.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM details WHERE username='{user}'")

    # data processing
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data


def data_processing(username, lst1, lst2, lst3, lst4):
    newlst1 = []
    newlst2 = []

    for a in lst1:
        if a != "":
            newlst1.append(a)
    for b in lst2:
        if b != "":
            newlst2.append(b)

    for c in lst3:
        if c != "":
            newlst1.append(c)
        else:
            newlst1.append(c)
    for d in lst4:
        if d != "":
            newlst2.append(d)
        else:
            newlst2.append("")
    length = len(newlst2)

    # print(newlst1)
    # print(newlst2)

    finaldic = {}
    for y in range(5):
        if newlst1[y] != "":
            if newlst1[y] != "":
                finaldic[f"link{y+1}"] = f"{newlst1[y]}>{newlst2[y]}"
        else:
            finaldic[f"link{y+1}"] = f""

    # print(finaldic)

    # print(f"value={finaldic['link3']}")
    # print(newlst2)
    str = f"INSERT INTO details VALUES('{username}','{finaldic['link1']}', '{finaldic['link2']}', '{finaldic['link3']}', '{finaldic  ['link4']}', '{finaldic['link5']}')"
    # dic = {"apple":"world"}
    # print(dic[lst1[1]])
    return str


def encrypt(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash


@app.route('/')
def index():
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            return redirect('/home')
    except:
        return render_template('index.html', params=params)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_exist = "NO"
    match = "YES"
    length = "MORE"
    if request.method == 'POST':
        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password').lower()
        password_confirm = request.form.get('password_confirm').lower()
        print(email, username, password, password_confirm)

        # validation
        conn = sqlite3.connect('user.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM users WHERE username='{username}'")
        data = c.fetchone()
        # print(type(data))
        conn.close()
        if data == None:
            user_exist == "NO"
            if len(password) < 6:
                return render_template('signup.html', user_exist=user_exist, match="YES", length="LESS")
            if password != password_confirm:
                return render_template('signup.html', user_exist=user_exist, match="NO", length=length)
            else:
                hash_password = encrypt(password)
                # to users
                conn = sqlite3.connect('user.db')
                c = conn.cursor()
                c.execute(
                    f"INSERT INTO users VALUES('{username}','{hash_password}', '{email}', 'free', 'no')")
                conn.commit()
                conn.close()
                # to details
                conn = sqlite3.connect('linklerz_.db')
                c = conn.cursor()
                c.execute(
                    f"INSERT INTO details VALUES('{username}','', '', '', '','')")
                conn.commit()
                conn.close()

                token = gen_token(email)
                final_token = f"https://linklerz.cleverapps.io/confirm/{token}"
                # print(final_token)
                send_email(email, username, final_token)
                # print("Database done")
                return render_template('confirm.html', email_address=email)
        elif len(data) > 0:
            # print(user_exist)
            # print(data)
            return render_template("signup.html", user_exist="YES", match=match, length=length)
        # print(user_exist)
        # conn.commit()
    return render_template('signup.html', user_exist=user_exist, match=match, length=length)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    try:
        username = session['user']
        data = user_detail(username)
        return render_template('profile.html', data=data)
    except:
        return redirect('/error')


@app.route('/emailconfirm')
def emailconfirm():
    try:
        username = session['user']
        data = user_detail(username)
        email = data[2]
        token = gen_token(email)
        final_token = f"https://linklerz.cleverapps.io/confirm/{token}"
        # print(final_token)
        send_email(email, username, final_token)
        return render_template('confirm.html', email_address=email)
    except:
        return redirect('/error')


@app.route('/confirm/<token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm', max_age=60480)
    # data process
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE email='{email}'")
    data = c.fetchone()
    c.execute(f"DELETE FROM users WHERE email='{email}'")

    password = data[1]
    username = data[0]
    # email = data[2]
    c.execute(
        f"INSERT INTO users VALUES('{username}','{password}', '{email}', 'free', 'yes')")

    # print(data)
    conn.commit()
    conn.close()

    return render_template("confirm_email.html", email=email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect('/home')


@app.route('/logout')
def logout():
    try:
        session.pop('user')
        return redirect('/')
    except:
        return redirect('/error')


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        # delete row
        username = request.form.get('username', "")
        conn = sqlite3.connect('linklerz_.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM details WHERE username='{username}'")
        conn.commit()
        conn.close()
        # add row
        link_address1 = request.form.get('link_address0', '')
        link_address2 = request.form.get('link_address1', '')
        link_address3 = request.form.get('link_address2', '')
        link_address4 = request.form.get('link_address3', '')
        link_address5 = request.form.get('link_address4', '')
        link_name1 = request.form.get('link_name0', '')
        link_name2 = request.form.get('link_name1', '')
        link_name3 = request.form.get('link_name2', '')
        link_name4 = request.form.get('link_name3', '')
        link_name5 = request.form.get('link_name4', '')
        newlink_name1 = request.form.get('newlink_name0', "")
        newlink_name2 = request.form.get('newlink_name1', "")
        newlink_name3 = request.form.get('newlink_name2', "")
        newlink_name4 = request.form.get('newlink_name3', "")
        newlink_name5 = request.form.get('newlink_name4', "")
        newlink_address1 = request.form.get('newlink_address0', "")
        newlink_address2 = request.form.get('newlink_address1', "")
        newlink_address3 = request.form.get('newlink_address2', "")
        newlink_address4 = request.form.get('newlink_address3', "")
        newlink_address5 = request.form.get('newlink_address4', "")
        lst_name = [link_name1, link_name2, link_name3, link_name4, link_name5]
        lst_link_address = [link_address1, link_address2,
                            link_address3, link_address4, link_address5]
        newlst_name = [newlink_name1, newlink_name2,
                       newlink_name3, newlink_name4, newlink_name5]
        newlst_link_address = [newlink_address1, newlink_address2,
                               newlink_address3, newlink_address4, newlink_address5]

        print(len(lst_name))
        print(len(lst_link_address))
        print(len(newlst_name))
        print(len(newlst_link_address))
        process = data_processing(
            username, lst_name, lst_link_address, newlst_name, newlst_link_address)
        print(process)
        conn = sqlite3.connect('linklerz_.db')
        c = conn.cursor()
        c.execute(process)
        # database processing
        conn.commit()
        conn.close()
    return redirect('/home')


@app.route('/delete/<link_name>', methods=['GET', 'POST'])
def delete(link_name):
    username = session['user']
    get_name = link_name
    print(get_name)
    lst = delete_data(get_name)

    if len(lst) < 5:
        for i in range(5-len(lst)):
            lst.append("")

    str = f"INSERT INTO details VALUES('{username}','{lst[0]}', '{lst[1]}', '{lst[2]}', '{lst[3]}', '{lst[4]}')"
    conn = sqlite3.connect('linklerz_.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM details WHERE username='{username}'")
    c.execute(str)
    conn.commit()
    conn.close()
    return redirect('/edit')


def user_detail(username):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}'")
    data = c.fetchone()
    conn.commit()
    conn.close()

    return data


@app.route('/home', methods=['GET', 'POST'])
def home():
    login_fail = ""
    links = 0
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            # posts = Posts.query.all()
            data = get_links(username)
            link_name = []
            link_address = []
            for i in data:
                if i == "":
                    links -= 1
                links += 1
            # print(links)
            for i in range(1, links):
                link = data[i]
                seperate = link.split(">")
                link_name.append(seperate[0])
                link_address.append(seperate[1])
            username = session['user']
            data = user_detail(username)
            plan = data[3]
            confirm = data[4]
            # print(link_address, link_name)
            return render_template('home.html', username=username, link_name=link_name, link_address=link_address, links=links-1, plan=plan, confirm=confirm)
    except Exception as e:
        e = "by post"
    if request.method == 'POST':
        username = request.form.get('username').lower()
        userpass = request.form.get('password').lower()
        userpass = encrypt(userpass)
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM users WHERE username='{username}'")
            # data processing
            data = c.fetchone()
            conn.commit()
            conn.close()
            # print(data)

            data_username = data[0]
            data_password = data[1]
            if (username == data_username and userpass == data_password):
                data = get_links(username)
                link_name = []
                link_address = []
                for i in data:
                    if i == "":
                        links -= 1
                    links += 1
                # print(links)
                for i in range(1, links):
                    link = data[i]
                    seperate = link.split(">")
                    link_name.append(seperate[0])
                    link_address.append(seperate[1])
                # set the session variable
                session['user'] = username
                # posts = Posts.query.all()
                # print(link_address, link_name)
                data = user_detail(username)
                plan = data[3]
                confirm = data[4]
                return render_template('home.html', username=username, link_name=link_name, link_address=link_address, links=links-1, plan=plan, confirm=confirm)
        except:
            login_fail = "Username and Password do not match"
    return render_template('login.html', login_fail=login_fail)


@app.route('/edit')
def edit():
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            data = get_links(username)
            link_name = []
            link_address = []
            links = 0
            for i in data:
                if i == "":
                    links -= 1
                links += 1
            for i in range(1, links):
                link = data[i]
                seperate = link.split(">")
                link_name.append(seperate[0])
                link_address.append(seperate[1])
            num = 5 - len(link_name)
            # print(link_address, link_name)
            return render_template('edit.html', username=username, link_name=link_name, link_address=link_address, num=num, links=links-1)
    except:
        username = "error"
        return redirect('/error')


@app.route(
    '/li.<user>')
def link(user):
    # connects to database
    conn = sqlite3.connect('linklerz_.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM details WHERE username='{user}'")

    # data processing
    data = c.fetchone()
    conn.commit()
    conn.close()
    link_name = []
    link_address = []
    links = 0
    for i in data:
        if i == "":
            links -= 1
        links += 1
        print(links)
    for i in range(1, links):
        link = data[i]
        seperate = link.split(">")
        link_name.append(seperate[0])
        link_address.append(seperate[1])

    return render_template('default.html', username=user, link_name=link_name, link_address=link_address, links=links)


@app.route('/settings')
def settings():
    try:
        username = session['user']
        data = user_detail(username)
        plan = data[3]
        return render_template('settings.html', username=username, plan=plan)
    except:
        return redirect("/error")


@app.route("/error")
def error():
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
