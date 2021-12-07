from app.modules import *

app = Flask(__name__)

from app.settings import *
from app.db import *
from app.builder import *
from app.views import *
