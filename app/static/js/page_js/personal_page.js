$(function () {

    $.get('/getUserInfo/', function (data) {
        if (data.code === 200) {
            $('#show_username').html(data.username);
            $('#show_nickname').html(data.nickname);
            $('#show_app_key').html(data.app_key);
            $('#show_icode').html(data.invitation_code);
        } else if (data.code === 1000){
            window.location.href = '/login/'
        } else {
            alert('获取信息失败！')
        }
    });
    $('#ch_nickname').on('click', function () {
        var input_nickname = $('#input_nickname');
        input_nickname.attr('type', 'text');
        $('#show_nickname').hide();
        $('#ch_nickname').hide();
        var old_name = $('#show_nickname').html();
        input_nickname.val(old_name);
        input_nickname.focus();
    });
    $('#input_nickname').blur(function (e) {
        $('#show_nickname').show();
        $('#ch_nickname').show();
        var old_name = $('#show_nickname').html();
        var new_name = $('#input_nickname').val();
        $('#input_nickname').attr('type', 'hidden');
        if (old_name === new_name) {
            return;
        }
        if (confirm('确定修改昵称吗？')) {
            $.post('/setNickName/', {'new_name': new_name}, function (data) {
                if (data.code) {
                    $('#show_nickname').html(new_name);
                } else {
                    alert('请求有误' + data.msg);
                }
            });
        }
    });
});