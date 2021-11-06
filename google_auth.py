from google_auth_oauthlib.flow import Flow
import os
import pathlib
import json
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

development = False

if development == True:
    uri = 'http://127.0.0.1:5000/callback'
else:
    uri = 'https://lerz.herokuapp.com/callback'

GOOGLE_CLIENT_ID = '983066542456-1gsapcu2uta11718lp1l6j9c7f5pnf5k.apps.googleusercontent.com'
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email','openid'],
    redirect_uri=uri)
    