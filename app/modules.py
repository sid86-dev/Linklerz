# flask modules
from flask import Flask, render_template, session, request, redirect, jsonify, url_for, make_response
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
from google_auth_oauthlib.flow import Flow
import redis
import pyimgur


# local modules
from mailer.delete_mailer import delete_email
from mailer.mailer import send_email
from api.api import api_conv
# from facebook_auth import*
import os
import pathlib
import json
import asyncio
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
import re



with open('config.json', 'r') as f:
    params = json.load(f)["params"]
