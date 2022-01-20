from app.settings import *


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    plan = db.Column(db.String(12), nullable=False)
    confirmation = db.Column(db.String(20), nullable=False)
    linktype = db.Column(db.String(500), nullable=False)
    linkurl = db.Column(db.String(500), nullable=False)
    userid = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    auth = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    qrlink = db.Column(db.String(30), nullable=False)
