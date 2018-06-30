import os
from datetime import timedelta

import redis

basedir = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR = os.path.join(basedir, 'app/static')
TEMPLATES_DIR = os.path.join(basedir, 'app/templates')
REDIS_HOST = '120.79.52.3'
REDIS_PORT = 8464
REDIS_PASSWORD = 'yxgw'
IP_PROXY_LIST_NAME = 'proxy_info_pool'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TTCISAGOODBOY'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 15
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host=REDIS_HOST,
                                port=REDIS_PORT,
                                password=REDIS_PASSWORD)
    SESSION_COOKIE_NAME = 'CrawlM'
    SESSION_KEY_PREFIX = 'CrawlM:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=48)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/crawl_manage?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/crawl_manage'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/crawl_manage'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}