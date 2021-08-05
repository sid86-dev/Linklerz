from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
import json
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

import sqlite3

app = Flask(__name__) 


@app.route('/')
def home():
    return render_template('index.html', params=params)
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route(
    '/link/<user>')
def sid(user):
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
    for i in range(1,4):
        link  = data[i]
        seperate = link.split(">")
        # print(seperate)
        link_name.append(seperate[0])
        link_address.append(seperate[1])
    # print(link_name)
    # print(link_address)
    # lst = ["Instagram", "Facebook", "Whatsupp", "Snapchat"]

    return render_template('home.html', username=user,link_name=link_name,link_address=link_address)

if __name__ == "__main__":
    app.run(debug=True)