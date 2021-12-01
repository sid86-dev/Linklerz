from app import settings

app = Flask(__name__)

from app import views
from app import config
from app import db
from app import builder