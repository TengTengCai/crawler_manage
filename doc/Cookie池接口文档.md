# Cookie池接口文档

## 获取一条Cookie数据

### 方法

*GET*

#### URL地址

`http://127.0.0.1:5000/api/getCookies/<string:host>/?app_key=`

`<string:host>`为需要获取哪个站点的Cookie值

`app_key`为用户的钥匙,在控制台中可查看其值为多少.

### 响应

会随机返回一个符合要求的Cookie(前提是需要在后台添加你要获取的Cookie)

#### 请求成功

```
{
  "code": 200,
  "data": "SUV=1802141907505183; debug_test=sohu_third_cookie; t=1530172506629; gidinf=x099980109ee0dbed7ba5a8580009075217e9c2185d3; sohutag=8HsmeSc5NCwmcyc5NSwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5NTIsJ2kmOiAsJ3cmOiAsJ2gmOiAsJ2NmOiAsJ2UmOiAsJ20mOiAsJ3QmOiB9; gn12=w:1; _muid_=1527731489680410; IPLOC=CN5100; reqtype=pc",
  "msg": "请求成功"
}
```

#### 输入的站点不存在

```
{
  "code": 1301,
  "msg": "当前host=www.baidu.com在数据库中并不存在,请确认是否输入正确,或在后台中添加相应站点的Cookies的数值"
}
```

#### 缺少app_key参数

```json
{
  "code": 1101,
  "msg": "缺少app_key参数!"
}
```

#### app_key不存在

```json
{
  "code": 1102,
  "msg": "app_key的值不存在!"
}
```

#### 数据库错误

```json
{
  "code": 1102,
  "msg": "服务器忙,请稍后再试! <string: 错误原因>"
}
```