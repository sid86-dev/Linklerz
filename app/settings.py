# flask modules
from flask import Flask, render_template, session, request, redirect, jsonify,url_for
import re
from os import abort
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine
from authlib.integrations.flask_client import OAuth


# python tool modules
from functools import lru_cache
import hashlib
import string
import random
import threading
import json
import requests

# external modules
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

# local modules
from mail.delete_mailer import delete_email
from mail.mailer import send_email
from api.api import api_conv
from google_auth import*
# from facebook_auth import*