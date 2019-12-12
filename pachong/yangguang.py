from Tools.ip_tools import *
from lxml import etree
from Tools.tools import *


def get_school_data():
    url = 'https://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-100.dhtml'
    html = get_res(url, headers=headers).content.decode().replace('\n', '').replace('\r', '')
    root = etree.HTML(html)
    tr_list = root.xpath('//table//tr[position()>1]')
    isnull = tr_list[0].xpath('.//td[@colspan]')
    if isnull:
        return 'Over！'
    for td in tr_list:
        # 院校名称
        school = td.xpath('./td[1]/a/text()')[0].replace(' ', '')
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
        print(school)
        print(score)
        print(gradation)
        print(graduate_student)
        print(address)
        print(belong)
        print(types)


print(get_school_data())

'''

//table//tr[position()>1]   # 获取所有tr

//table//tr[position()>1][position()=1]/td[1]/a/text()

'''
