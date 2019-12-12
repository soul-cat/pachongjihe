import requests
from Tools.tools import headers, md_5, MysqlHelper
import re
from time import sleep

helper = MysqlHelper('xxx.xxx.xxx.xxx', port, 'db', 'user', 'password')


def get_siteid():
    """
    获取siteId
    :return:
    """
    url_1 = 'https://app.gzdaily.cn:4443/app_if/getConfig?appID=4'
    try:
        res = requests.get(url_1, headers=headers, verify=False, timeout=10).json()
    except Exception as e:
        print(e)
        return '4'
    return res['siteID']


site_id = get_siteid()


def get_list():
    """
    获取数据列表url
    :return:
    """
    meta_list = []
    url = 'https://app.gzdaily.cn:4443/app_if/getColumns?siteId=4&parentColumnId=54&version=0&columnType=-1'
    # params = {
    #     'siteId': str(site_id),
    #     'parentColumnId': '54',
    #     'version': '0',
    #     'columnType': '-1'
    # }
    try:
        columns = requests.get(url, headers=headers, verify=False, timeout=15).json()['columns']
    except Exception as e:
        print(e)
        exit()
    for column in columns:
        meta_list.append({'columnId': column['columnId'], 'columnStyle': column['columnStyle'], 'columnName': column['columnName']})
    else:
        return meta_list


def parse():
    """
    除参数lastFileId外都可从上面获取，lastFileId填写1100000
    :return:
    """
    meta_list = get_list()
    upda = {}
    url = 'https://app.gzdaily.cn:4443/app_if/getArticles'
    # 根据参数拼接板块url
    for meta in meta_list:
        # 最大页码不定
        for page in range(300):
            params = {
                'columnId': meta['columnId'],
                'version': '0',
                'lastFileId': '1100000',
                'page': page,
                'adv': '1',
                'columnStyle': meta['columnStyle']
            }
            try:
                res = requests.get(url, params=params, headers=headers, timeout=10).json()
            except Exception as e:
                print(e)
                continue
            try:
                carousel_list = res['carousel'] + res['list']
            except Exception as e:
                print(e)
                try:
                    carousel_list = res['carousel']
                except Exception as ee:
                    print(ee)
                    carousel_list = res['list']
            # 为空则是到这页就没有数据了
            if carousel_list:
                # 板块链接及板块名称
                c_url = f"{url}?columnId={meta['columnId']}&version=0&lastFileId=1100000&page={page}" \
                    f"&adv=1&columnStyle={meta['columnStyle']}"
                c_name = meta['columnName']
                print(c_url, c_name)
                break

                # 解析详情页数据，链接：carousel['contentUrl']
                # for carousel in carousel_list:
                #     sleep(1)
                #     upda['hash_key'] = md_5(carousel['contentUrl'])
                #     if filter_(upda['hash_key']):
                #         continue
                #     upda['title'] = carousel['title']
                #     upda['source'] = carousel['reporter']
                #     upda['putime'] = carousel['publishtime']
                #     upda['content'] = get_t(carousel['contentUrl'])
                #     if upda['content']:
                #         save_mysql(upda)
                #         upda.clear()
            else:
                break


def filter_(hash_key):
    sql_q = 'select hash_key from fanlei where hash_key=%s'
    one = helper.get_one(sql_q, params=[hash_key])
    return one


def save_mysql(data: dict):
    """
    插入mysql
    :param data:
    :return:
    """
    print(data)
    try:
        sql = 'insert into fanlei(hash_key,title,content,put_time,source) values(%s,%s,%s,%s,%s)'
        params = (data['hash_key'], data['title'], data['content'], data['putime'], data['source'])
        if helper.insert(sql, params):
            print('插入成功')
        else:
            print('插入失败')
    except Exception as e:
        print(e)
        print('插入失败')


def get_t(url):
    # try:
    #     res = requests.get(url, headers=headers, verify=False, timeout=10).json()
    #     content = re.sub('<.*?>', '', res['content']).replace('&nbsp;', '').replace('\n', '')\
    #         .replace('\r', '').replace(' ', '')
    # except Exception as e:
    #     print(e)
    #     try:
    #         print(url)
    #         res = requests.get(url, headers=headers, timeout=10).json()
    #         content = re.sub('<.*?>', '', res['content']).replace('\n', '').replace('\r', '')\
    #             .replace('&nbsp;', '').replace(' ', '')
    #     except Exception as ee:
    #         print(ee)
    #         content = '获取失败'
    if 'http' in url and 'html' in url:
        content = ''
    else:
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=10).json()
            content = re.sub('<.*?>', '', res['content']).replace('&nbsp;', '').replace('\n', '') \
                .replace('\r', '').replace(' ', '')
        except Exception as e:
            print(e)
            return ''
    return content


def main():
    parse()


def test():
    """
    https://app.gzdaily.cn:4443/app_if/getColumns?siteId=4&parentColumnId=54&version=0&columnType=-1
    变换参数找规律
    :return:
    """
    for column_id in range(1000):
        url = f'https://app.gzdaily.cn:4443/app_if/getColumns?siteId=4&parentColumnId=' \
            f'{column_id}&version=0&columnType=-1'
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=10)
        except Exception as e:
            print(e)
            continue
        sleep(1)
        try:
            if res.json()['columns']:
                print(url)
                print(column_id)
                print(res.text)
                print('*' * 50)
        except Exception as e:
            print(e)
            print(res)
            print('*' * 50)


if __name__ == '__main__':
    main()


