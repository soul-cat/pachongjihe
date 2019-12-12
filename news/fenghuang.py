import requests
import json
import re
from Tools.tools import time_13, jsonp_to_json, headers, md_5, string_todatetime, MysqlHelper
from time import sleep

helper = MysqlHelper('221.225.81.216', 23355, 'acq_data', 'rps_data', 'sLNJ&Auqe9pXSs2(')
upda = {}


def parse(query, page):
    """
    搜索入口，只负责获取二级页面url
    :param query: 关键词
    :param page: 页码
    :return:
    """
    url = f'http://shankapi.ifeng.com/autumn/getSoFengData/all/{query}/{str(page)}/getSoFengDataCallback'
    params = {
        'callback': 'getSoFengDataCallback',
        '_': time_13
    }
    res = requests.get(url, headers=headers, params=params).content.decode('utf-8')
    json_re = jsonp_to_json(res)
    if not json_re['data']['items']:
        print('没有数据了')
        exit()
    for new in json_re['data']['items']:
        url_t = 'http:' + new['url']
        get_t(url_t)


def get_t(url):
    """
    获取信息，包括标题，内容，时间，来源
    :param url:
    :return:
    """
    res = requests.get(url).text
    try:
        json_res = json.loads(re.findall(r'var allData = (.*?);\n', res, re.S)[0])
    except Exception as e:
        print(e)
        return None
    title = json_res['docData']['title']
    try:
        putime = json_res['docData']['newsTime']
    except Exception as e:
        print(e)
        putime = ''
    try:
        content_html = json_res['docData']['contentData']['contentList'][0]['data']
        content = re.sub('<.*?>', '', content_html).replace('\n', '').replace('\r', '')
    except Exception as e:
        print(e)
        print(json_res)
        content = ''
    try:
        referer = json_res['docData']['vestAccountDetail']['sourceFrom']
    except Exception as e:
        print(e)
        try:
            referer = json_res['docData']['source']
        except:
            referer = ''
    upda['hash_key'] = md_5(url)
    upda['title'] = title
    upda['content'] = content
    upda['source'] = referer
    upda['putime'] = putime
    puttime = re.findall(r'\d{1,4}', upda['putime'])
    if len(puttime) == 5:
        upda['putime'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:{puttime[4]}:00')
    elif len(puttime) == 6:
        upda['putime'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:'
                                           f'{puttime[4]}:{puttime[5]}')
    print(upda)
    save_mysql(upda)
    upda.clear()
    print('*' * 50)


def save_mysql(data: dict):
    try:
        sql_q = 'select hash_key from fanlei where hash_key=%s'
        one = helper.get_one(sql_q, params=[data['hash_key']])
        if one:
            print(one)
            print('该条数据已存在')
        else:
            sql = 'insert into fanlei(hash_key,title,content,put_time,source) values(%s,%s,%s,%s,%s)'
            params = (data['hash_key'], data['title'], data['content'], data['putime'], data['source'])
            if helper.insert(sql, params):
                print('插入成功')
            else:
                print('插入失败')
    except Exception as e:
        print(e)
        print('插入失败')


def main():
    for p in range(1, 20):
        parse('爬虫', p)
        sleep(3)


if __name__ == '__main__':
    main()
