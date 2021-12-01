from app import settings
from app import app

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

# app variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# cloud db uri
URI = params['database_uri_1']

e = create_engine(
    URI, pool_recycle=1800)


app.secret_key = params['app_key']
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
oauth = OAuth(app)

db = SQLAlchemy(app)
# app.config['SERVER_NAME'] = 'localhost:5000'
