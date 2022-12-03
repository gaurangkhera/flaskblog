from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(32))
    blogs = db.relationship('Blog', backref='user')

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    author = db.Column(db.String(128), db.ForeignKey('user.username'), nullable=False)