import requests

x = requests.get('https://lerz.herokuapp.com/api/sid86_')

print(type(x.text))