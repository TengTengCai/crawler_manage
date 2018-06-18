import time
from io import BytesIO
from random import choice
from datetime import datetime
from hashlib import md5
from flask import Blueprint, render_template, request, session, Response, jsonify

# from app import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

from config import STATICFILES_DIR, TEMPLATES_DIR
from units import verify_code
from app.models import User, db

views = Blueprint('views', __name__,
                  static_folder=STATICFILES_DIR,
                  template_folder=TEMPLATES_DIR)

hash_md5 = md5()


@views.route('/')
def index():
    return 'Hello, World'


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
