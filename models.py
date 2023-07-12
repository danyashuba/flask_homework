from enum import Enum, auto

from app import db


class StatusEnum(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    REJECTED = auto()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=False, nullable=False)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String, unique=True, nullable=False)


class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String, db.ForeignKey('Users.user'), unique=False, nullable=False)
    purchased_book = db.Column(db.String, db.ForeignKey('Books.book'), unique=False, nullable=False)
