from app import db
from datetime import datetime


class TimestampMixin(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)


class User(TimestampMixin, db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)  # ID
    username = db.Column(db.String(20), unique=True)  # 用户名
    password = db.Column(db.String(225), nullable=False)  # 密码
    nike_name = db.Column(db.String(20), unique=True)  # 昵称

    __tablename__ = 'cm_users'

    def __repr__(self):
        return f'<User u_id:{self.u_id}, username:{self.username}>'


class Cookies(TimestampMixin, db.Model):
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    cookies_String = db.Column(db.Text, nullable=True)
    w_id = db.Column(db.Integer, db.ForeignKey('cm_website.w_id'), nullable=False)

    __tablename__ = 'cm_cookie'

    def __repr__(self):
        return f'<Cookies cookie_id:{self.cookie_id}>'


class WebSite(db.Model):
    w_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    web_site_name = db.Column(db.String(64), )
    cookies = db.relationship('Cookies', backref='website', lazy=True)

    __tablename__ = 'cm_website'

    def __repr__(self):
        return f'<WebSite w_id:{self.w_id}, webSiteName:{self.web_site_name}>'
