import json
import time
from functools import wraps
import logging

from app import db
from datetime import datetime
from redis import Redis, RedisError
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, IP_PROXY_LIST_NAME


class TimestampMixin(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)


class User(TimestampMixin, db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)  # ID
    username = db.Column(db.String(20), unique=True)  # 用户名
    password = db.Column(db.String(225), nullable=False)  # 密码
    nike_name = db.Column(db.String(20), unique=True)  # 昵称
    invitation_code = db.Column(db.String(20), nullable=False)  # 邀请码
    app_key = db.Column(db.String(225), unique=True, nullable=False)  # 用户访问接口钥匙
    ip_proxy_vt = db.Column(db.Integer, default=0, unique=False, nullable=False)  # ip接口访问次数
    cookies_vt = db.Column(db.Integer, default=0, unique=False, nullable=False)  # cookies接口访问次数

    __tablename__ = 'cm_user'

    def __repr__(self):
        return f'<User u_id:{self.u_id}, username:{self.username}>'


class Cookies(TimestampMixin, db.Model):
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    cookies_String = db.Column(db.Text, nullable=True)
    w_id = db.Column(db.Integer, db.ForeignKey('cm_website.w_id'), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('cm_user.u_id'), nullable=False)
    __tablename__ = 'cm_cookie'

    def __repr__(self):
        return f'<Cookies cookie_id:{self.cookie_id}>'


class WebSite(db.Model):
    w_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    web_site_host = db.Column(db.String(64), unique=True)
    cookies = db.relationship('Cookies', backref='website', lazy=True)

    __tablename__ = 'cm_website'

    def __repr__(self):
        return f'<WebSite w_id:{self.w_id}, webSiteName:{self.web_site_host}>'


def deal_redis_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return fn(*args, **kwargs)
            except RedisError as e:
                logging.error(str(e) + '...2秒后重试')
                time.sleep(2)
        logging.error('连接错误,请检查网络连接或服务器!')
        return None

    return wrapper


class RedisConnection(object):
    @deal_redis_error
    def __init__(self):
        self._conn = Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           password=REDIS_PASSWORD)

    @deal_redis_error
    def get_ip_proxy(self, start, end):
        proxy_list_byte = self._conn.lrange(IP_PROXY_LIST_NAME, start, end)
        proxy_list_str = []
        for item in proxy_list_byte:
            item_str = item.decode('utf-8')
            proxy_list_str.append(json.loads(item_str, encoding='utf-8'))
        return proxy_list_str

    @deal_redis_error
    def get_ip_proxy_total(self):
        return self._conn.llen(IP_PROXY_LIST_NAME)

    @deal_redis_error
    def get_one_ip_proxy(self):
        proxy_bytes = self._conn.rpoplpush(IP_PROXY_LIST_NAME, IP_PROXY_LIST_NAME)
        proxy = proxy_bytes.decode('utf-8')
        return proxy
