from flask import Flask, render_template
import json
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

app = Flask(__name__) 



@app.route('/')
def output():
    return render_template('home.html', params=params)
@app.route('/sid')
def sid():
    return render_template('sidhome.html', params=params)
@app.route('/amit')
def amit():
    return render_template('amithome.html', params=params)
@app.route('/bishal')
def bishal():
    return render_template('bishalhome.html', params=params)

if __name__ == "__main__":
    app.run(debug=True)