# from Tools.ip_pools import *
import csv

from Tools.tools import *
from lxml import etree
from Tools.ip_tools import *

headers['Cookie'] = 'acw_tc=24638ed115690360716985328e4942483e85ded6044f1c69b5cb8100be; QCCS' \
                    'ESSID=keor9o12l07svq9itmd1fj9hv4; UM_distinctid=16d51d8598e363-03cf8da98f' \
                    '1b4-67e1b3f-100200-16d51d8598f293; CNZZDATA1254842228=1102579259-15690357' \
                    '00-%7C1569035700; zg_did=%7B%22did%22%3A%20%2216d51d85b21fb-04f31d57cf45' \
                    '62-67e1b3f-100200-16d51d85b22621%22%7D; hasShow=1; _uab_collina=156903619' \
                    '677764314942447; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1569036198; zg' \
                    '_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569036196645%2C%22up' \
                    'dated%22%3A%201569037884041%2C%22info%22%3A%201569036196651%2C%22superPr' \
                    'operty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%' \
                    '22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%' \
                    '20%229d7d7266023df459461e77a8a9bedc5f%22%7D; Hm_lpvt_3456bee468c83cc63fb' \
                    '5147f119f1075=1569037884'


# 获取最大页码
def get_end_page(name):
    url = 'https://www.qichacha.com/search?key=' + str(name)
    html = get_res(url, headers=headers).content.decode().replace('\r', '').replace('\n', '')
    root = etree.HTML(html)
    page_end = root.xpath('//ul[@class="pagination pagination-md"]/li'
                          '[last()-1]/a/text()')[0].split('.')[-1]
    return page_end


def get_data(name):
    collection = db.企查查
    end_page = get_end_page(name)
    # csv容器
    rows = []
    hh = ['_id', '公司名字', '法人代表', '注册资本', '成立日期', '地址']
    # 遍历页码，爬取每一页数据
    # end_page+1
    for page in range(1, 3):
        print('*' * 50)
        print(f'{"." * 6}当前位置第{page}页！')
        url = 'https://www.qichacha.com/search?key=' + str(name) + '#p:' + str(page)
        html = get_res(url, headers=headers).content.decode().replace('\r', '').replace('\n', '')
        root = etree.HTML(html)
        td_list = root.xpath('//table[@class="m_srchList"]//tr/td[3]')

        # 爬取每一条数据，并写入数据库
        for td in td_list:
            # 公司名字
            company_name = ''.join(td.xpath('./a//text()'))
            # 判定该条信息是否已存在
            if BaseMongo.find_one(collection, {'公司名字': company_name}, {'公司名字'}):
                print(f'{"." * 6}**{company_name}**已存在！')
                continue
            # 法人代表
            legal = td.xpath('./p[1]/a/text()')[0]
            # 注册资本
            capital = td.xpath('./p[1]/span[1]/text()')[0].split('：')[1]
            # 成立日期
            data_c = td.xpath('./p[1]/span[2]/text()')[0].split('：')[1]
            # 地址
            address = td.xpath('./p[3]/text()')[0].replace(' ', '').split('：')[1]
            upda = {
                '公司名字': company_name,
                '法人代表': legal,
                '注册资本': capital,
                '成立日期': data_c,
                '地址': address
            }
            # 装入csv容器
            rows.append(upda)
            # 插入mongo
            BaseMongo.insert_one(collection, upda)
            print(f'{"." * 6}{company_name}插入成功！')
    with open('../data/企查查.csv', 'w', newline='')as f:
        f_csv = csv.DictWriter(f, hh)
        f_csv.writeheader()
        f_csv.writerows(rows)
    print('写入csv文件完毕！')


if __name__ == '__main__':
    get_data('小米')
    # print(get_end_page('小米'))
