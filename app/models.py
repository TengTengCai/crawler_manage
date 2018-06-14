from app import db


class User(db.Model):
    username = db.Column(db.Integer, unique=True)

