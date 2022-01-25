from flask import Flask

app = Flask(__name__)


@app.get('/')
def index():
	return "HEllo world"

@app.get('/check')
def check():
	data = {'name':'sid','age': 17 }

	return data


@app.get('/getdata')
	data = ''