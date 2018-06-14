from app import db
from datetime import datetime


class BaseModel(db.Model):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)


class User(BaseModel):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)  # ID
    username = db.Column(db.String(20), unique=True)  # 用户名
    password = db.Column(db.String(225), nullable=False)  # 密码
    nike_name = db.Column(db.String(20), unique=True)  # 昵称

    __tablename__ = 'cm_users'

    def __repr__(self):
        return f'<User u_id:{self.u_id}, username:{self.username}>'
