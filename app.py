from typing_extensions import final
from flask import Flask, render_template, session, request
# from flask_sqlalchemy import SQLAlchemy
import json

from werkzeug.utils import redirect
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

import sqlite3


app = Flask(__name__)
app.secret_key = 'my-secret-key'


def get_links(user):
    conn = sqlite3.connect('linklerz_.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM details WHERE username='{user}'")

    # data processing
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data


@app.route('/')
def index():
    return render_template('index.html', params=params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


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
                    links -=1
                links +=1
            print(links)
            for i in range(1, links):
                link = data[i]
                seperate = link.split(">")
                link_name.append(seperate[0])
                link_address.append(seperate[1])
            username = session['user']
            print(link_address, link_name)
            return render_template('home.html', username=username, link_name=link_name, link_address=link_address, links=links-1)
    except Exception as e:
        print(e)
        username = ""
    if request.method == 'POST':
        username = request.form.get('username')
        userpass = request.form.get('password')
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
                        links -=1
                    links +=1
                print(links)
                for i in range(1, links):
                    link = data[i]
                    seperate = link.split(">")
                    link_name.append(seperate[0])
                    link_address.append(seperate[1])
                # set the session variable
                session['user'] = username
                # posts = Posts.query.all()
                print(link_address, link_name)
                return render_template('home.html', username=username, link_name=link_name, link_address=link_address, links=links-1)
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
                    links -=1
                links +=1
            for i in range(1, links):
                link = data[i]
                seperate = link.split(">")
                link_name.append(seperate[0])
                link_address.append(seperate[1])
            num = 5 - len(link_name)
            print(link_address, link_name)
            return render_template('edit.html', username=username, link_name=link_name, link_address=link_address, num=num, links=links-1)
    except:
        username = "error"
        return render_template('404.html')


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
            links -=1
        links +=1
        print(links)
    for i in range(1, links):
        link = data[i]
        seperate = link.split(">")
        link_name.append(seperate[0])
        link_address.append(seperate[1])

    return render_template('link.html', username=user, link_name=link_name, link_address=link_address,links=links)


if __name__ == "__main__":
    app.run(debug=True)
