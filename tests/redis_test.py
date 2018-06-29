import json
import logging
import time
from functools import wraps


from redis import RedisError, Redis

from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, IP_PROXY_LIST_NAME


def deal_redis_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return fn(*args, **kwargs)
            except RedisError as e:
                logging.error(str(e) + '...2秒后重试')
                time.sleep(2)
        logging.error('连接错误,请检查网络连接或服务器!')
        return None

    return wrapper


class RedisConnection(object):
    @deal_redis_error
    def __init__(self):
        self._conn = Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           password=REDIS_PASSWORD)

    @deal_redis_error
    def get_ip_proxy(self, start, end):
        proxy_list = self._conn.lrange('proxy_info_pool', start, end)
        proxy_list_str = []
        for item in proxy_list:
            item_str = item.decode('utf-8')
            proxy_list_str.append(json.loads(item_str, encoding='utf-8'))
        return json.dumps(proxy_list_str)

    @deal_redis_error
    def get_ip_proxy_total(self):
        return self._conn.llen(IP_PROXY_LIST_NAME)

    @deal_redis_error
    def get_one_ip_proxy(self):
        proxy_bytes = self._conn.rpoplpush(IP_PROXY_LIST_NAME, IP_PROXY_LIST_NAME)
        proxy = proxy_bytes.decode('utf-8')
        return proxy


def main():
    rconn = RedisConnection()
    proxy_list = rconn.get_ip_proxy(0, 9)
    # print(proxy_list)
    # print(rconn.get_ip_proxy_total())
    print(rconn.get_one_ip_proxy())
    # print(len(proxy_list))
    # print(type(proxy_list))


if __name__ == '__main__':
    main()
