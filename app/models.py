from app import db


class User(db.Model):
    u_id = db.Column(db.In)
    username = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(225), nullable=False)
