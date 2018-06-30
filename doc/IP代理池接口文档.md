# IP代理池接口文档

该接口能从Redis高速缓存服务器中获取一条代理信息或多条IP代理信息.

## 获取一条代理信息

### 请求

#### 方法

*GET*

#### URL地址

 `http://120.79.52.3/api/getOneIPProxy/?app_key=`

在这里需要传递`app_key`用户的钥匙,在控制台中可查看其值为多少.

### 响应

#### 请求成功

```json
{
  "code": 200,
  "data": [
    "{\"ip\": \"119.10.67.144\", \"port\": \"808\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"https\", \"p_address\": \"\\u5317\\u4eac\"}"
  ],
  "msg": "请求成功"
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

## 获取多条代理IP

### 方法

*GET*

#### URL地址

 `http://120.79.52.3/api/getMoreIPProxy/<int:num>/?app_key=`

`<int:num>`为需要获取的IP代理跳数(最多10条,超过10条则只会返回10条数据)

`app_key`为用户的钥匙,在控制台中可查看其值为多少.

### 响应

#### 请求成功

```json
{
  "code": 200,
  "data": [
    "{\"ip\": \"115.204.27.169\", \"port\": \"6666\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"https\", \"p_address\": \"\\u6d59\\u6c5f\\u676d\\u5dde\"}",
    "{\"ip\": \"218.64.154.53\", \"port\": \"61234\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"http\", \"p_address\": \"\\u6c5f\\u897f\\u840d\\u4e61\\u5e02\\u4e0a\\u6817\\u53bf\"}",
    "{\"ip\": \"61.135.217.7\", \"port\": \"80\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"http\", \"p_address\": \"\\u5317\\u4eac\"}",
    "{\"ip\": \"182.113.172.33\", \"port\": \"36293\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"https\", \"p_address\": \"\\u6cb3\\u5357\\u6f2f\\u6cb3\"}",
    "{\"ip\": \"113.240.226.164\", \"port\": \"8080\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"https\", \"p_address\": \"\\u6e56\\u5357\\u957f\\u6c99\"}",
    "{\"ip\": \"115.221.121.103\", \"port\": \"27389\", \"anonymity\": \"\\u9ad8\\u533f\", \"p_type\": \"https\", \"p_address\": \"\\u6d59\\u6c5f\\u6e29\\u5dde\"}",
    "{\"ip\": \"120.78.78.141\", \"port\": \"8888\", \"anonymity\": \"\\u900f\\u660e\", \"p_type\": \"https\", \"p_address\": null}",
    "{\"ip\": \"222.185.22.45\", \"port\": \"6666\", \"anonymity\": \"\\u900f\\u660e\", \"p_type\": \"https\", \"p_address\": \"\\u6c5f\\u82cf\\u5e38\\u5dde\"}",
    "{\"ip\": \"120.26.110.59\", \"port\": \"8080\", \"anonymity\": \"\\u900f\\u660e\", \"p_type\": \"http\", \"p_address\": \"\\u5317\\u4eac\"}",
    "{\"ip\": \"183.128.35.176\", \"port\": \"18118\", \"anonymity\": \"\\u900f\\u660e\", \"p_type\": \"https\", \"p_address\": \"\\u6d59\\u6c5f\\u676d\\u5dde\"}"
  ],
  "msg": "请求成功"
}
```

#### 其他响应

其他的响应与获取一条代理信息的响应相同.