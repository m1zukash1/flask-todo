from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(96), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    todos = db.relationship('Todo', backref='author', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    priority = db.Column(db.Integer, default=1)
