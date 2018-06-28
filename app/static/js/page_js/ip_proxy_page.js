$(function () {
    $('#table').bootstrapTable({
        url: '/getIPProxy/',
        method: 'GET',
        pagination: true,
        height: 790,
        pageNumber: 1,
        pageList: [10, 15, 20],
        pageSize: 10,
        sortable: false,
        striped: true,
        sidePagination: 'server',
        queryParams: function(params){
            let temp = {
                rows: params.limit,                         //页面大小
                page: (params.offset / params.limit) + 1,   //页码
            };
            return temp;
        },
        columns: [{
            field: 'ip',
            title: 'IP地址'
        }, {
            field: 'port',
            title: '端口'
        }, {
            field: 'anonymity',
            title: '是否匿名'
        }, {
            field: 'p_type',
            title: '类型'
        }, {
            field: 'p_address',
            title: '服务器地址'
        }],
        onLoadSuccess:function () {

        },
        onLoadError:function () {
            alert('数据加载失败!');
        }
    });
});

