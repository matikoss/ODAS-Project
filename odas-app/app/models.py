from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.String(500))
    owner_mail = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=False)
