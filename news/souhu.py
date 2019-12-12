import re
import datetime
from time import sleep

import requests
from Tools.tools import time_13, time_10, md_5, string_todatetime, MysqlHelper
from lxml import etree

helper = MysqlHelper('221.225.81.216', 23355, 'acq_data', 'rps_data', 'sLNJ&Auqe9pXSs2(')
upda = {}


def query_souhu(query, page):
    """
    搜索入口，获取列表页数据并清洗
    :param query: 搜索关键词
    :param page: 用于做页码
    """
    url = 'http://search.sohu.com/search/meta'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78'
                      '.0.3904.108 Safari/537.36'
    }
    params = {
        'keyword': query,
        'terminalType': 'pc',
        'ip': 'undefined',
        'city': 'undefined',
        'spm-pre': f'smpc.csrpage.0.0.{time_13}Eai3EbT',
        'SUV': '04507266887805d5',
        'from': str(page * 10),
        'size': '10',
        'searchType': 'news',
        'queryType': 'edit',
        'queryId': f'{time_10}undefined5aqS00{str(page)}',
        'pvId': f'{time_13}JqdrDjF',
        'refer': 'http://search.sohu.com',
        '_': time_13
    }
    try:
        res = requests.get(url, headers=headers, params=params, timeout=None).json()['data']['news']
    except Exception as e:
        print(e)
        print('没有数据了')
        exit()
    for c in res:
        upda['url'] = c['url']
        query_t(upda['url'])


def query_t(url):
    """
    访问二级页面，获取标题、内容、来源、发布时间
    :param url: 二级页面链接
    :return: None
    """
    # url = 'http://www.sohu.com/a/353537706_120179204'
    res = requests.get(url).text
    root = etree.HTML(res)
    upda['hash_key'] = md_5(url)
    upda['title'] = root.xpath('//h1/text()')[0].replace(' ', '').replace('\r', '').replace('\n', '').replace(' ', '')
    try:
        upda['source'] = root.xpath('//div[@id="user-info"]/h4/a/text()')[0]
    except Exception as e:
        print(e)
        print(url)
        upda['source'] = ''
    try:
        upda['putime'] = root.xpath('//span[@id="news-time"]/text()')[0]
        puttime = re.findall(r'\d{1,4}', upda['putime'])
        if len(puttime) == 5:
            upda['putime'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:{puttime[4]}:00')
        elif len(puttime) == 6:
            upda['putime'] = string_todatetime(f'{puttime[0]}-{puttime[1]}-{puttime[2]} {puttime[3]}:'
                                               f'{puttime[4]}:{puttime[5]}')
    except Exception as e:
        print(e)
        print(url)
        upda['putime'] = datetime.datetime.now()
    upda['content'] = ''.join(root.xpath('//article[@id="mp-editor"]//p/text()'))
    print(upda)
    save_mysql(upda)
    upda.clear()


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
    for p in range(1, 11):
        query_souhu('爬虫', p)
        sleep(3)


if __name__ == '__main__':
    main()
