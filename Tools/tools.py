import datetime
import hashlib
import time
import pymongo
from fake_useragent import UserAgent
import requests
import json
import MySQLdb

# UA池
user_agent = str(UserAgent().random)

headers = {
    'User-Agent': user_agent
}

# 13位时间戳
time_13 = str(int(time.time() * 1000))
time_10 = str(int(time.time() * 10))


def md_5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


def get_json(url, headers, params):
    res = requests.post(url, headers=headers, data=json.dumps(params)).json()
    return res


def datetime_tostring(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string_todatetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


def jsonp_to_json(st):
    json_res = st.split('(', 1)[1].rsplit(')', 1)[0]
    return json.loads(json_res)


def get_cookie(url):
    headers = {
        'User-Agent': user_agent
    }
    res = requests.get(url, headers=headers)
    cookies = dict(res.cookies)
    cookie = ''
    for k in cookies.keys():
        cookie = cookie + k + '=' + cookies[k] + ';'
    return cookie


client = pymongo.MongoClient(host='localhost', port=27017)
db = client.pachong


class BaseMongo(object):
    """
    mongo工具类
    """
    @staticmethod
    def insert_one(collection, data):
        """直接使用insert() 可以插入一条和插入多条 不推荐 明确区分比较好"""
        res = collection.insert_one(data)
        return res.inserted_id

    @staticmethod
    def insert_many(collection, data_list):
        res = collection.insert_many(data_list)
        return res.inserted_ids

    @staticmethod
    def find_one(collection, data, data_field={}):
        if len(data_field):
            res = collection.find_one(data, data_field)
        else:
            res = collection.find_one(data)
        return res

    @staticmethod
    def find_many(collection, data, data_field={}):
        """ data_field 是指输出 操作者需要的字段"""
        if len(data_field):
            res = collection.find(data, data_field)
        else:
            res = collection.find(data)
        return res

    @staticmethod
    def update_one(collection, data_condition, data_set):
        """修改一条数据"""
        res = collection.update_one(data_condition, data_set)
        return res

    @staticmethod
    def update_many(collection, data_condition, data_set):
        """ 修改多条数据 """
        res = collection.update_many(data_condition, data_set)
        return res

    @staticmethod
    def delete_many(collection, data):
        res = collection.delete_many(data)
        return res

    @staticmethod
    def delete_one(collection, data):
        res = collection.delete_one(data)
        return res


class MysqlHelper():
    """
    mysql工具类
    """
    def __init__(self, host, port, db, user, passwd, charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params=()):
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count
