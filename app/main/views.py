import time
from io import BytesIO
from random import choice
from datetime import datetime
from hashlib import md5
from functools import wraps
from flask import Blueprint, render_template, request, session, Response, jsonify, redirect

# from app import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

from config import STATICFILES_DIR, TEMPLATES_DIR
from units import verify_code
from app.models import User, db, RedisConnection, WebSite, Cookies

views = Blueprint('views', __name__,
                  static_folder=STATICFILES_DIR,
                  template_folder=TEMPLATES_DIR)

hash_md5 = md5()


@views.route('/')
def index():
    try:
        user_id = session['user_id']
    except KeyError as e:
        return redirect('/login/')
    if user_id != '':
        return redirect('/myConsole/')
    else:
        return redirect('/login/')


@views.route('/register/', methods=['GET', 'POST'])
def register():
    method = request.method
    if method == 'GET':
        return render_template('register.html')
    elif method == 'POST':
        form = request.form
        vcode = form['form-verify-code']
        username = form['form-user-name']
        password = form['form-password']
        repassword = form['form-re-password']
        icode = form['form-invitation-code']
        data = {}
        if not vcode == session['verify_code']:
            data['code'] = 401
            data['msg'] = '验证码错误!'
            return jsonify(data)
        user = User.query.filter_by(invitation_code=icode).first()
        if (not icode == 'TTCISAGOODBOY') or user:
            data['code'] = 402
            data['msg'] = '邀请码错误!'
            return jsonify(data)
        user = User.query.filter_by(username=username).first()
        if user:
            data['code'] = 403
            data['msg'] = '用户名已存在'
            return jsonify(data)
        if not password == repassword:
            data['code'] = 404
            data['msg'] = '两次密码不一致'
            return jsonify(data)
        you_icode = get_random_invitation_code()
        password = generate_password_hash(password)
        dtime = datetime.now()
        un_time = time.mktime(dtime.timetuple())
        nickname = '用户' + str(int(un_time))
        app_key = get_random_app_key(username, un_time)
        try:
            user = User(username=username,
                        password=password,
                        nike_name=nickname,
                        invitation_code=you_icode,
                        app_key=app_key)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            data['code'] = 405
            data['msg'] = '服务器错误' + str(e)
            return jsonify(data)
        else:
            data['code'] = 200
            data['msg'] = '请求成功'
            return jsonify(data)


def get_random_invitation_code():
    lib = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    code = ''
    for _ in range(20):
        code += choice(lib)
    return code


def get_random_app_key(username, un_time):
    h_md5 = hash_md5.copy()
    my_str = username + str(un_time)
    h_md5.update(my_str.encode('utf-8'))  # 需要将字符串进行编码，编码成二进制数据
    md5_str = h_md5.hexdigest()  # 获取16进制的摘要
    return str(md5_str)


@views.route('/login/', methods=['GET', 'POST'])
def login():
    method = request.method
    if method == 'GET':
        print('GET')
        return render_template('login.html')
    elif method == 'POST':
        # doLogin
        form = request.form
        vcode = form['form-verify-code']
        username = form['form-username']
        password = form['form-password']
        data = {}

        if not session['verify_code'] == vcode:
            data['code'] = 301
            data['msg'] = '验证码输入有误!'
            return jsonify(data)

        user = User.query.filter_by(username=username).first()
        if not user:
            data['code'] = 302
            data['msg'] = '登录的帐号不存在!'
            return jsonify(data)

        if not check_password_hash(user.password, password):
            data['code'] = 303
            data['msg'] = '登录的密码错误!'
            return jsonify(data)
        session['user_id'] = user.u_id
        data['code'] = 200
        data['msg'] = '登录成功,正在跳转...'
        return jsonify(data)


@views.route('/logout/', methods=['GET'])
def logout():
    session.pop('user_id')
    return redirect('/login/')


@views.route('/VerifyCode/<float:random_num>/')
def get_verify_code(random_num):
    print(random_num)
    vcode = verify_code.VerifyCode()
    image = vcode.verify_image
    session['verify_code'] = vcode.verify_code
    f = BytesIO()
    image.save(f, 'jpeg')
    resp = Response(f.getvalue(), mimetype="image/jpeg")
    return resp


def is_login(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = {}
        try:
            user_id = session['user_id']
        except KeyError as e:
            data['code'] = 1000
            data['msg'] = '未登录' + str(e)
            return jsonify(data)
        else:
            if user_id is '':
                data['code'] = 1000
                data['msg'] = '未登录'
                return jsonify(data)
            else:
                return fn(*args, **kwargs)

    return wrapper


@views.route('/myConsole/', methods=['GET'])
def my_console():
    try:
        session['user_id']
    except KeyError:
        return redirect('/login/')
    return render_template('console.html')


@views.route('/personal/', methods=['GET'])
def personal():
    try:
        session['user_id']
    except KeyError:
        return redirect('/login/')
    return render_template('personal.html')


@views.route('/getUserInfo/', methods=['GET'])
@is_login
def get_user_info():
    user_id = session['user_id']
    data = {}
    try:
        user = User.query.get(user_id)
    except Exception as e:
        data['code'] = 501
        data['msg'] = '用户不存在！' + str(e)
        return jsonify(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功！'
        data['username'] = user.username
        data['nickname'] = user.nike_name
        data['app_key'] = user.app_key
        data['invitation_code'] = user.invitation_code
        data['ip_proxy_vt'] = user.ip_proxy_vt
        data['cookies_vt'] = user.cookies_vt
        return jsonify(data)


@views.route('/setNickName/', methods=['POST'])
@is_login
def change_nick_name():
    user_id = session['user_id']
    data = {}
    form = request.form
    new_nicke_name = form['new_name']
    user = User.query.get(user_id)
    if not user:
        data['code'] = 601
        data['msg'] = '用户不存在！'
    else:
        user.nike_name = new_nicke_name
        db.session.commit()
        data['code'] = 200
        data['msg'] = '请求成功！'
    return jsonify(data)


@views.route('/IPProxy/', methods=['GET'])
def get_ip_proxy():
    return render_template('proxy_manage.html')


@views.route('/getIPProxy/', methods=['GET'])
@is_login
def query_ip_proxy():
    params = request.args
    rows = int(params['rows'])
    page = int(params['page'])
    rconn = RedisConnection()
    proxy_list = rconn.get_ip_proxy((page - 1) * rows, page * rows)
    data = {'total': rconn.get_ip_proxy_total(),
            'rows': proxy_list}
    return jsonify(data)


@views.route('/Cookies/', methods=['GET'])
def get_cookies():
    return render_template('cookies.html')


@views.route('/getWebSite/', methods=['GET'])
def get_website():
    website_list = WebSite.query.all()
    data = {}
    temp = []
    for website in website_list:
        w_id = website.w_id
        web_host = website.web_site_host
        item = {'id': w_id, 'webSite': web_host}
        temp.append(item)
    data['code'] = 200
    data['msg'] = '请求成功!'
    data['webs'] = temp
    return jsonify(data)


@views.route('/selectCookies/', methods=['GET'])
@is_login
def select_cookies():
    user_id = session['user_id']
    data = {}
    my_args = request.args
    try:
        rows = int(my_args['rows'])
        page = int(my_args['page'])
        website_host = my_args['website']
    except KeyError as e:
        print(e)
        data['code'] = 200
        data['msg'] = '参数错误!'
        return jsonify(data)
    else:
        # print(my_args)
        if website_host == 'null':
            all_cookies = Cookies.query.filter_by(u_id=user_id).offset(rows * (page - 1)).limit(rows)
            count = Cookies.query.count()
        else:
            website = WebSite.query.filter_by(web_site_host=website_host).first()
            all_cookies = Cookies.query.filter_by(w_id=website.w_id, u_id=user_id).offset(rows * (page - 1)).limit(rows)
            count = len(website.cookies)
        temp = []
        for cookie_obj in all_cookies:
            item = {'id': cookie_obj.c_id,
                    'website': cookie_obj.website.web_site_host,
                    'cookies_string': cookie_obj.cookies_String,
                    'operation': ''}
            temp.append(item)
        data['total'] = count
        data['rows'] = temp
        return jsonify(data)


@views.route('/addCookies/', methods=['POST'])
@is_login
def add_cookies():
    user_id = session['user_id']
    data = {}
    my_form = request.form
    try:
        website_host = my_form['website']
        cookies_string = my_form['cookies']
    except KeyError as e:
        print(str(e))
        data['code'] = 701
        data['msg'] = '参数不正确'
        return jsonify(data)
    website = WebSite.query.filter_by(web_site_host=website_host).first()
    if not website:
        website = WebSite(web_site_host=website_host)
        try:
            db.session.add(website)
            db.session.commit()
        except Exception as e:
            print(str(e))
            data['code'] = 702
            data['msg'] = '添加站点数据失败'
            db.session.rollback()
            return jsonify(data)
    cookies = Cookies(cookies_String=cookies_string, w_id=website.w_id, u_id=user_id)
    try:
        db.session.add(cookies)
        db.session.commit()
    except Exception as e:
        print(str(e))
        data['code'] = 703
        data['msg'] = '添加Cookies数据失败,数据库未响应!'
        db.session.rollback()
        return jsonify(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功!'
        return jsonify(data)


@views.route('/deleteCookies/<int:c_id>/', methods=['DElETE'])
@is_login
def delete_cookies(c_id):
    data = {}
    cookies = Cookies.query.get(c_id)
    w_id = cookies.w_id
    count = Cookies.query.filter_by(w_id=w_id).count()
    if count == 1:
        website = WebSite.query.get(w_id)
        db.session.delete(website)
    try:
        db.session.delete(cookies)
        db.session.commit()
    except Exception as e:
        print('删除数据出错' + str(e))
        data['code'] = 801
        data['msg'] = '删除数据出错'
        db.session.rollback()
        return jsonify(data)
    else:
        data['code'] = 200
        data['msg'] = '数据删除请求成功!'
        return jsonify(data)


@views.route('/changeCookies/', methods=['POST'])
@is_login
def change_cookies():
    data = {}
    my_form = request.form
    try:
        c_id = my_form['c_id']
        cookies_str = my_form['cookies']
    except KeyError as e:
        print('参数错误!' + str(e))
        data['code'] = 901
        data['msg'] = '参数错误'
        return jsonify(data)
    else:
        cookies = Cookies.query.get(c_id)
        cookies.cookies_String = cookies_str
        try:
            db.session.add(cookies)
            db.session.commit()
        except Exception as e:
            print('修改数据发生错误!' + str(e))
            db.session.rollback()
            data['code'] = 902
            data['msg'] = '修改数据发生错误!'
            return jsonify(data)
        else:
            data['code'] = 200
            data['msg'] = '请求成功,成功修改!'
            return jsonify(data)


@views.route('/IPProxyDoc/', methods=['GET'])
def ip_proxy_doc():
    return render_template('ip_api_doc.html')


@views.route('/CookieDoc/', methods=['GET'])
def cookies_doc():
    return render_template('cookies_doc.html')