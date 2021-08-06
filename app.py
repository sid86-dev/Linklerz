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
        
        # lst_link = [link_address1,link_address2,link_address3,link_address4,link_address4,link_address5]
        lst_name = [link_name1,link_name2,link_name3,link_name4,link_name4,link_name5]
        for n in lst_name:
            if n != "":
                link1 = f"{link_name1}>{link_address1}"
                link2 = f"{link_name2}>{link_address2}"
                link3 = f"{link_name3}>{link_address3}"
                link4 = f"{link_name4}>{link_address4}"
                link5 = f"{link_name5}>{link_address5}"
            else:
                link1 = ""
                link2 = ""
                link3 = ""
                link4 = ""
                link5 = ""
                
        print(f"username={username}")
        print(f"Link={link1}")
        print(f"Link={link2}")
        print(f"Link={link3}")
        print(f"Link={link4}")
        print(f"Link={link5}")
        conn = sqlite3.connect('linklerz_.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO details VALUES('{username}','{link1}', '{link2}', '{link3}', '{link4}',  '{link5}')")
        # database processing
        conn.commit()
        conn.close()     
    return redirect('/home')

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
            # print(links)
            for i in range(1, links):
                link = data[i]
                seperate = link.split(">")
                link_name.append(seperate[0])
                link_address.append(seperate[1])
            username = session['user']
            # print(link_address, link_name)
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
            # print(link_address, link_name)
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
