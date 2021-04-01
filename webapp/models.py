from . import db
from flask_login import UserMixin


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cause_issue = db.Column(db.String(200))
    solution_issue = db.Column(db.String(200))
    category_issue = db.Column(db.String(200))
    description = db.Column(db.String(10000))
    start_date = db.Column(db.DateTime(timezone=True))
    final_date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    FirstName = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
