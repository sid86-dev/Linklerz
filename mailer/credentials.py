import json

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

EMAIL_ADDRESS = params['email']
EMAIL_PASSWORD = params['password']