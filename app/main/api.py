from functools import wraps
from random import randint

from flask import Blueprint, jsonify, request

from app.models import RedisConnection, User, db, WebSite, Cookies

api = Blueprint('api', __name__)
redis_conn = RedisConnection()


def is_exist_app_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            app_key = request.args['app_key']
        except KeyError as e:
            return jsonify({'code': 1101, 'msg': '缺少app_key参数!'})
        else:
            user = User.query.filter_by(app_key=app_key).first()
            if not user:
                return jsonify({'code': 1102, 'msg': 'app_key的值不存在!'})
            else:
                return fn(user, *args, **kwargs)

    return wrapper


@api.route('/getOneIPProxy/', methods=['GET'])
@is_exist_app_key
def get_one_ip_proxy(user):
    data = {}
    proxy = redis_conn.get_one_ip_proxy()
    user.ip_proxy_vt += 1
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        data['code'] = 1201
        data['msg'] = '服务器忙,请稍后再试!' + str(e)
        return jsonify(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        data['data'] = [proxy]
        return jsonify(data)


@api.route('/getMoreIPProxy/<int:num>/', methods=['GET'])
@is_exist_app_key
def get_more_ip_proxy(user, num):
    data = {}
    proxy_list = []
    for i in range(num):
        proxy = redis_conn.get_one_ip_proxy()
        proxy_list.append(proxy)
    user.ip_proxy_vt += 1
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        data['code'] = 1201
        data['msg'] = '服务器忙,请稍后再试!' + str(e)
        return jsonify(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        data['data'] = proxy_list
        return jsonify(data)


@api.route('/getCookies/<string:host>/', methods=['GET'])
@is_exist_app_key
def get_one_cookies(user, host):
    data = {}
    website = WebSite.query.filter_by(web_site_host=host).first()
    if not website:
        data['code'] = 1301
        data['msg'] = '当前host='+host+'在数据库中并不存在,请确认是否输入正确,或在后台中添加相应站点的Cookies的数值'
        return jsonify(data)
    w_id = website.w_id
    cookies_list = Cookies.query.filter_by(w_id=w_id, u_id=user.u_id)
    count = cookies_list.count()
    cookies = cookies_list.offset(randint(0, count)).limit(1).first()
    cookies_str = cookies.cookies_String if cookies else ''
    data['code'] = 200
    data['msg'] = '请求成功'
    data['data'] = cookies_str
    return jsonify(data)
