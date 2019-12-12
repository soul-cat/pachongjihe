import requests
from time import sleep
from Tools.tools import md_5, string_todatetime, MysqlHelper
from lxml import etree
from apscheduler.schedulers.blocking import BlockingScheduler

upda = {}
helper = MysqlHelper('221.225.81.216', 23355, 'acq_data', 'rps_data', 'sLNJ&Auqe9pXSs2(')
sched = BlockingScheduler()


def parse(keyword, curpage=1):
    """
    搜索入口，获取标题信息、发布时间、信息来源
    :param keyword: 关键词
    :param curpage: 页码
    :return:
    """
    url = 'http://so.news.cn/getNews'
    params = {
        'keyword': keyword,
        'curPage': str(curpage),
        'sortField': '0',
        'searchFields': '1',
        'lang': 'cn'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0'
                      '.3904.108 Safari/537.36'
    }
    res_json = requests.get(url, params=params, headers=headers).json()
    if res_json['content']['results']:
        for new in res_json['content']['results']:
            title = new['title'].replace('<font color=red>', '').replace('</font>', '')
            pubtime = new['pubtime']
            referer = new['sitename']
            url_t = new['url']
            get_t(url_t)
            upda['hash_key'] = md_5(url_t)
            upda['title'] = title
            upda['putime'] = string_todatetime(pubtime)
            upda['source'] = referer
    else:
        print('没有更多数据了')
        exit()


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


# @sched.scheduled_job('interval', seconds=1)
def main():
    for page in range(1, 11):
        parse('爬虫', page)
        sleep(3)


def get_t(url):
    """
    访问二级页面，获取内容信息
    :param url: 二级页面url
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0'
                      '.3904.108 Safari/537.36'
    }
    res = requests.get(url, headers=headers).content.decode('utf-8')
    root = etree.HTML(res)
    content = ''.join(root.xpath('//p//text()')).replace('\u3000', '').replace('\r', '').replace('\n', '')
    upda['content'] = content.replace('\xa0', '')
    print(upda)
    save_mysql(upda)
    upda.clear()


if __name__ == '__main__':
    # sched.start()
    main()
