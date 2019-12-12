import csv

from Tools.ip_tools import *
from Tools.tools import *
from lxml import etree


# 获取主页表格中所有信息
def get_school_data():
    # 用于写入csv文件
    hh = ['院校名称', '专业类别', '专业名称']
    print("*" * 50)
    print(f'任务启动，抓取阳光高考所有高校信息！')
    print("*" * 50)
    collection = db.阳光高考
    num = 0
    while True:
        url = 'https://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-' + str(num) + '.dhtml'
        html = get_res(url, headers=headers).content.decode().replace('\n', '').replace('\r', '')
        num += 20
        root = etree.HTML(html)
        tr_list = root.xpath('//table//tr[position()>1]')
        # 判定是否有数据
        isnull = tr_list[0].xpath('.//td[@colspan]')
        if isnull:
            print("*" * 50)
            print(f'现在是{(num + 20) / 20}页，目标网站没有数据，程序结束！')
            print("*" * 50)
            return 'Over！'
        print("*" * 50)
        print(f'第{(num+20)/20}页开始爬取！')
        print("*" * 50)
        rows = []
        # with open('gaokao.csv', 'w', newline='')as fw:
        #     f_csv = csv.DictWriter(fw, hh)
        #     f_csv.writeheader()
        #     f_csv.writerows(rows)
        for td, index in zip(tr_list, range(1, len(tr_list)+1)):
            # 院校名称
            if td.xpath('./td[1]/a/text()'):
                school = td.xpath('./td[1]/a/text()')[0].replace(' ', '')
                # 院校链接
                school_link = 'https://gaokao.chsi.com.cn' + td.xpath('./td[1]/a/@href')[0].replace(' ', '')
            elif td.xpath('./td[1]/text()'):
                # 院校链接，有可能不存在
                school_link = ''
                school = td.xpath('./td[1]/text()')[0].replace(' ', '')
            else:
                # 院校链接，有可能不存在
                school_link = ''
                print(f'...........第{index}条院校信息获取失败！')
                continue
            temp_dic = {}
            temp_dic['院校名称'] = school
            print(school_link)
            if school_link:
                res_l = get_res(school_link, headers=headers).content.decode()
                root_l = etree.HTML(res_l)
                type_link = 'https://gaokao.chsi.com.cn' + root_l.xpath('//div[@class="nav-c'
                                                                        'ontainer clearfix"]/a[4]/@href')[0]
                res_ll = get_res(type_link, headers=headers).content.decode()
                root_ll = etree.HTML(res_ll)
                # 获取到所有专业块
                div_list_ll = root_ll.xpath('//div[@class="container"]/div[@clas'
                                            's="tab-container zyk-zyfb-tab yxk-zyjs-tab"]')
                for div_ll in div_list_ll:
                    # 分类名称
                    type_ll = div_ll.xpath('./*/*/a/text()')[0]
                    temp_dic['专业类别'] = type_ll
                    if div_ll.xpath('.//li/a/text()'):
                        # 专业名称列表
                        zy_names_ll = div_ll.xpath('.//li/a/text()')
                    else:
                        zy_names_ll = div_ll.xpath('.//li/text()')
                    for zy_name in zy_names_ll:
                        temp_dic['专业名称'] = zy_name.replace('\r\n', '').replace(' ', '')
                        # 在这里插入
                        print(temp_dic)
                        rows.append(temp_dic.copy())
                        temp_dic.pop('专业名称')
                    temp_dic.pop('专业类别')

            else:
                print('目标没有链接')
            with open('gaokao.csv', 'w', newline='')as fw:
                f_csv = csv.DictWriter(fw, hh)
                f_csv.writeheader()
                f_csv.writerows(rows)
                print('*' * 50)
                print('*' * 50)
                print('*' * 50)
            if BaseMongo.find_one(collection, {'院校名称': school}, {'院校名称'}):
                print(f'*****{school}*****这条信息已经存在！')
                continue
            # 院校地址
            address = td.xpath('./td[2]/text()')[0].replace(' ', '')
            # 所属
            belong = td.xpath('./td[3]/text()')[0].replace(' ', '')
            # 院校类型
            types = td.xpath('./td[4]/text()')[0].replace(' ', '')
            # 学历
            gradation = td.xpath('./td[5]/text()')[0].replace(' ', '')
            # 研究生院，1为真，0为假
            graduate_student = len(td.xpath('./td[6]/i'))
            # 满意度
            try:
                score = td.xpath('./td[7]/a/text()')[0].replace(' ', '')
            except Exception as e:
                print(e)
                score = '目标网站暂无数据！'

            upda = {
                '院校名称': school,
                '院校地址': address,
                '所属': belong,
                '院校类型': types,
                '学历': gradation,
                '研究生院': graduate_student,
                '评分': score
            }
            BaseMongo.insert_one(collection, upda)
            print(f'...........第{index}条院校信息**{school}**写入数据库成功！')


# 获取学校详情页部分详细信息
def get_details():
    url = 'https://gaokao.chsi.com.cn/sch/schoolInfoMain--schId-14.dhtml###'
    html = get_res(url, headers=headers).content.decode()
    print(html)
    root = etree.HTML(html)

    # 第一块，学校地址，电话，邮箱
    link_phone_address = root.xpath('//div[@class="mid"]/div/span')
    # 学校官网
    link = link_phone_address[0].xpath('.//a/@href')[0]
    # 电话
    phone = link_phone_address[1].xpath('./text()')[0]
    # 学校地址
    address = link_phone_address[2].xpath('./text()')[0].replace('\r\n', '')
    print(link, '\n', phone, '\n', address, '\n')

    # 第二块，专业top10
    # 获取三个div块，每个都是不同的top10，并爬取目标网站有的跳转链接（及里面信息）
    div_list = root.xpath('//div[contains(@class, "col-list")]')
    for div in div_list:
        # 标题，比如专业推荐指数Top10，专业满意度Top10
        title = div.xpath('.//h3/text()[2]')
        # 获取若干tr块，每个代表一条专业信息
        tr_list = div.xpath('.//tr')
        for tr in tr_list:
            # 排名
            ranking = tr.xpath('./td[1]/span/text()')
            # 专业名称
            profess_name = tr.xpath('./td[2]/@title')
            # 专业链接，有的没有 加上   https://gaokao.chsi.com.cn
            profess_link = tr.xpath('./td[2]/*/a/@href')
            if profess_link:
                profess_link = 'https://gaokao.chsi.com.cn' + profess_link[0]
            # 评分和评比人数，交替
            score__person = tr.xpath('./td[3]//span[1]/text()')
            # 评分
            score = score__person[0]
            # 人数
            person = score__person[1]
            print(title)
            print(ranking)
            print(profess_name)
            print(profess_link)
            print(score)
            print(person)

    # 第三块


if __name__ == '__main__':
    get_school_data()
    # get_details()