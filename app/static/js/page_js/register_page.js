$(function () {
    let username_is_ok = false;
    let password_is_ok = false;
    let repassword_is_ok = false;
    let icode_is_ok = false;
    let error_info = $('#error_info');
    $('#login_btn').on('click', function (e) {
        window.location.href='/login/'
    });
    $('.registration-form').submit(function (e) {
        e.preventDefault();
        if (username_is_ok && username_is_ok && repassword_is_ok && icode_is_ok){
            error_info.html();
            $('.registration-form').ajaxSubmit(function (data) {
                if (data.code === 200){
                    alert('注册成功,1秒后跳转到登录界面');
                    setTimeout(function (e) {
                       window.location.href = '/login/';
                    },1000);
                }else {
                    error_info.html(data.msg)
                }
            });
        }else if (!username_is_ok) {
            error_info.html('用户名应为4-16位字母数字下划线和减号!');
        }else if (!password_is_ok) {
            error_info.html('密码最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符!!');
        }else if (!repassword_is_ok) {
            error_info.html('确认密码不一致!');
        }else if (!icode_is_ok){
            error_info.html('邀请码不符合要求');
        }
        let random = Math.random();
        $('#vcode_img').attr('src', '/VerifyCode/'+random+'/');
    });
    $('#form-user-name').blur(function (e) {
        let username = $('#form-user-name').val();
        let check_username = /^[a-zA-Z0-9_-]{4,16}$/;
        if (username === ''){
            error_info.html('用户名不能为空!');
            return;
        }
        if (check_username.test(username)){
            username_is_ok = true;
            error_info.html('');
        } else{
            error_info.html('用户名应为4-16位字母数字下划线和减号!');
        }
    });
    $('#form-password').blur(function (e) {
        let password = $('#form-password').val();
        let check_password = /^(\w){6,20}$/;
        if (password === ''){
            error_info.html('密码不能为空!');
            return;
        }
        if (check_password.test(password)) {
            password_is_ok = true;
            error_info.html('');
        } else {
            error_info.html('只能输入6-20个字母、数字、下划线');
        }
    });
    $('#form-re-password').blur(function (e) {
        let repassword = $('#form-re-password').val();
        let password = $('#form-password').val();
        if (repassword === '') {
            error_info.html('确认密码不能为空!');
            return;
        }
        if (repassword === password){
            repassword_is_ok = true;
            error_info.html('');
        } else {
            error_info.html('两次密码不一致!');
        }
    });
    $('#form-invitation-code').blur(function (e) {
        let icode = $('#form-invitation-code').val();
        let check_icode = /^[a-zA-Z]+$/;
        if (check_icode === ''){
            error_info.html('邀请码不能为空!');
            return;
        }
        if (check_icode.test(icode)){
            icode_is_ok = true;
            error_info.html('');
        } else {
            error_info.html('邀请码为全英文字母!');
        }
    });
    $('#form-verify-code').blur(function (e) {
        let vcode = $('#form-verify-code').val();
        if (vcode === '') {
            error_info.html('验证码不能为空!');
        } else if (vcode.length !== 4) {
            error_info.html('验证码长度为4位');
        }else {
            error_info.html('');
        }
    });
    $('#vcode_img').on('click', function (e) {
        let random = Math.random();
        $('#vcode_img').attr('src', '/VerifyCode/'+random+'/');
    });
});