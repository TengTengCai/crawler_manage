$(function () {
    $('.login-form').submit(function (e) {
        e.preventDefault();

        // let username = $('#form-user-name').val();
        // let password = $('#form-password').val();
        // let verify_code = $('#form-verify-code').val();
        let error_info = $('#error_info');
        $('form').ajaxSubmit(function (data) {
            if (data.code === 200) {
                alert(data.msg);
                setTimeout(function (e) {
                    window.location.href = '/console/'
                }, 1000);
            } else {
                error_info.html(data.msg)
            }
        });
        let random = Math.random();
        $('#vcode_img').attr('src', '/VerifyCode/' + random + '/');
    });
    $('#register_btn').on('click', function (e) {
        window.location.href = '/register/'
    });
    $('#vcode_img').on('click', function (e) {
        let random = Math.random();
        $('#vcode_img').attr('src', '/VerifyCode/' + random + '/');
    });
});