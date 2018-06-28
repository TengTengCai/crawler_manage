$(function () {
    $.get('/getWebSite/', function (data) {
        if (data.code === 200) {
            let list = data.webs;
            for (let i = 0 ; i< list.length; i++){
                // console.log(list[i].id);
                let opt = $("<option></option>");
                opt.html(list[i].webSite);
                opt.attr('w_id', list[i].id);
                $('#website_input').append(opt);
            }
        } else if (data.code === 1000) {
            window.location.href = '/login/'
        } else {
            alert('服务器出错!稍后再试!')
        }
    });
    $('#cookies_table').bootstrapTable({
        url: '/selectCookies/',
        method: 'GET',
        // contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        height: 700,
        pageNumber: 1,
        pageList: [10, 15],
        pageSize: 10,
        pagination: true,
        sortable: false,
        striped: true,
        sidePagination: 'server',
        queryParams: getParams,
        columns: [{
            field: 'id',
            title: 'id',
            width: '5%',
        }, {
            field: 'website',
            title: '站点地址',
            class: 'website',
            width: '10%',
            formatter: function (value, row, index) {
                return '<p id="website_c_id_'+row.id+'">'+value+'</p>'
            }
        }, {
            field: 'cookies_string',
            title: 'Cookies字符串',
            width: '80%',
            formatter: function (value, row, index) {
                return '<p id="cookies_s_id_'+row.id+'" class="tWidth">'+value+'</p>'
            }
        }, {
            field: 'operation',
            title: '操作',
            alert: 'center',
            width: '140px',
            formatter:function (value, row, index) {
                // console.log(row.id);
                return [
                    '<button type="button" c_id="'+row.id+'" class="RoleOfdelete btn btn-danger  btn-sm" style="margin-right:15px;">删除</button>',
                    '<button type="button" c_id="'+row.id+'" class="RoleOfedit btn btn-primary  btn-sm" style="margin-right:15px;" data-toggle="modal" data-target="#myModal">修改</button>'
                    ].join('');
            }
        }],
        onLoadSuccess:function (data) {
            setEventListener();
        },
        onLoadError:function () {
            alert('数据加载失败!');
        }
    });
    $('#add_cookie_form').submit(function (e) {
        e.preventDefault();
        let website = $('#input_website').val();
        let cookies = $('#input_cookies').val();
        let add_info = $('#modal_info_p');
        $('#add_cookie_info').modal('show');
        add_info.html('正在添加等待服务器响应...');
        if (website.length&&cookies.length){
            $('#add_cookie_form').ajaxSubmit({
                success: function (data) {
                    // alert(data);
                    if (data.code === 200){
                        refresh_table();
                        $('#input_cookies').val('');
                        add_info.html('添加成功!');
                        setTimeout(function () {
                            $('#add_cookie_info').modal('hide');
                        }, 1000);
                    } else if (data.code === 1000){
                        window.location.href = '/login/'
                    }
                },
                error: function () {
                    alert('添加数据失败!')
                }
            });
        }
    });
    function refresh_table() {
        $("#cookies_table").bootstrapTable('refresh', {
            url: '/selectCookies/',
            silent: true,
            query: getParams
        });
    }
    function getParams(params) {
        let website = $('#website_input').val();
        if (website === ''){
            website = 'null'
        }
        return {
            rows: params.limit,                         //页面大小
            page: (params.offset / params.limit) + 1,   //页码
            website: website
        };
    }
    $('#select_cookie_form').submit(function (e) {
        e.preventDefault();
        refresh_table()
    });
    function setEventListener() {
        $('.RoleOfdelete').on('click', function (e) {
            // alert('qwe');
            if (confirm('确认删除!')){
                let c_id = $(this).attr('c_id');
                $.ajax('/deleteCookies/'+c_id+'/',{
                    type: 'delete',
                    success: function (data) {
                        // alert(data.code);
                        if (data.code === 200){
                            refresh_table();
                        }else if (data.code === 1000){
                            window.location.href = '/login/'
                        }else {
                            alert(data.msg)
                        }
                    }
                });
            }
        });
        $('.RoleOfedit').on('click', function () {
            let c_id = $(this).attr('c_id');
            let website_host = $('#website_c_id_'+c_id).html();
            let cookies_str = $('#cookies_s_id_'+c_id).html();
            let cookies_input = $('#cookies_input');
            $('#website_p').html(website_host);
            cookies_input.val(cookies_str);
            $('#c_id_input').val(c_id);
        });
        $('#cookies_input').focus(function () {
           $(this).select();
        });
        $('#change_save_btn').on('click', function () {
            let c_id = $('#c_id_input').val();
            let cookies_str = $('#cookies_input').val();
            if (cookies_str.length === 0){
                $('#form_info_p').html('修改的数据不能为空!');
                return;
            }
            console.log(c_id);
            $('#modal_form').ajaxSubmit({
                type: 'post',
                success: function (data) {
                    if (data.code === 200) {
                        $('#form_info_p').html('数据修改成功!');
                        $('#cookies_s_id_'+c_id).html(cookies_str);
                        setTimeout(function () {
                            $('#myModal').modal('hide');
                        }, 1000);
                    } else if (data.code === 1000){
                        window.location.href = '/login/'
                    } else {
                        alert('修改数据失败!')
                    }
                }
            });
        });
    }
});