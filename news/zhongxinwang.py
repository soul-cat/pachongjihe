from time import sleep
import requests
import re
import execjs
from lxml import etree
from Tools.tools import md_5, MysqlHelper, string_todatetime

helper = MysqlHelper('221.225.81.216', 23355, 'acq_data', 'rps_data', 'sLNJ&Auqe9pXSs2(')
upda = {}


def search(query, page):
    """
    获取搜索页列表
    :param query:
    :return:
    """
    try:
        url = 'http://sou.chinanews.com/search.do'
        headers = {
            'Host': 'sou.chinanews.com',
            'Referer': 'http://sou.chinanews.com/search.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0'
                          '.2924.87 Safari/537.36',
        }
        data = {
            "q": query,
            'ps': 10,
            'start': str(int(page) * 10),
            'sort': 'pubtime',
            'time_scope': '0',
            'channel': 'all',
            'adv': '1'
        }
        r = requests.post(url, data=data, headers=headers, timeout=15)
        __jsluid = r.headers["Set-Cookie"].split(';')[0]
        txt_521 = ''.join(re.findall('<script>(.*?)</script>', r.text))
        if txt_521 != "":
            txt_5211 = txt_521.split('return c}')[0] + "return c}"
            js_str = """%s
            window={}
            function getJSL() {
            var z = f(y.match(/\w/g).sort(function (x, y) {
                return f(x) - f(y)
            }).pop());
            var data = "";
            var initZ = z;
            while (data.indexOf("document.cookie='__jsl") == -1 && z++ - initZ < 20) {
                data = y.replace(/\\b\w+\\b/g, function (y) {
                    return x[f(y, z) - 1] || ("_" + y)
                });
            }
            ;
            return eval(data.slice(data.indexOf("'__jsl_clearance"), data.indexOf("+';Expires")).replace(/document(.*?)toLowerCase\(\)/g, function (y) {
                return '"www.sou.chinanews.com/"'
            }));
        }""" % txt_5211
            ctx = execjs.compile(js_str)
            __jsl_clearance = ctx.call('getJSL').split(';')[0]
        headers1 = {
            "Cookie": "{}; {}".format(__jsluid, __jsl_clearance),
            'Host': 'sou.chinanews.com',
            'Referer': 'http://sou.chinanews.com/search.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0'
                          '.2924.87 Safari/537.36',
        }
        res = requests.post(url, data=data, headers=headers1, timeout=15).content.decode('utf-8')
        root = etree.HTML(res)
        url_list = root.xpath('//li[@class="news_title"]/a/@href')
        return url_list
    except Exception as e:
        print(e)


def get_t(url):
    """
    获取二级页面
    注意后面数据有编码问题，如果需要比较老的数据，写编码判断。大概是2018年12月5号以前的数据
    编码判断可以通过try分割那句代码去判断
    :param url:
    :return:
    """
    res = requests.get(url).content.decode('utf-8', "ignore")
    root = etree.HTML(res)
    upda['title'] = root.xpath('//h1/text()')[0].replace(' ', '').replace('\n', '').replace('\r', '')
    try:
        put_time_referer = root.xpath('//div[@class="left-t"]/text()')[0].replace('\xa0', '')\
            .replace(' ', '').split('来源：')
        upda['put_time'] = put_time_referer[0]
        puttime = re.findall(r'\d{1,4}', upda['put_time'])
        if len(puttime) == 5:
            upda['put_time'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:'
                                                 f'{puttime[4]}:00')
        elif len(puttime) == 6:
            upda['put_time'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:'
                                                 f'{puttime[4]}:{puttime[5]}')
        upda['referer'] = put_time_referer[1]
    except Exception as e:
        print(e)
        print(url)
    upda['content'] = ''.join(root.xpath('//div[@class="left_zw"]/p//text()')).replace('\n', '').replace('\r', '')
    save_mysql(upda)
    upda.clear()


def save_mysql(data: dict):
    print(data)
    try:
        sql_q = 'select hash_key from fanlei where hash_key=%s'
        one = helper.get_one(sql_q, params=[data['hash_key']])
        if one:
            print(one)
            print('该条数据已存在')
        else:
            sql = 'insert into fanlei(hash_key,title,content,put_time,source) values(%s,%s,%s,%s,%s)'
            params = (upda['hash_key'], upda['title'], upda['content'], upda['put_time'], upda['referer'])
            if helper.insert(sql, params):
                print('插入成功')
            else:
                print('插入失败')
    except Exception as e:
        print(e)
        print('插入失败')


def main():
    for page in range(10):
        url_list = search('爬虫', page)
        for url in url_list:
            upda['hash_key'] = md_5(url)
            get_t(url)
            print('*' * 50)
            sleep(3)


if __name__ == '__main__':
    main()
