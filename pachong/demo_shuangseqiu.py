from bs4 import BeautifulSoup
from Tools.ip_tools import *
from Tools.tools import *
import csv


def get_shuang():
    f = open('../data/双色球.csv', 'a', newline='')
    header = [
        '期号', '开奖日期', '红球', '蓝球', '总投注额',
        '一等奖注数', '一等奖奖金', '二等奖注数', '二等奖奖金', '奖金滚存'
    ]
    f_csv = csv.DictWriter(f, header)
    with open('../data/双色球.csv') as ff:
        ff.read()
    f_csv.writeheader()
    url = 'http://zst.aicai.com/ssq/openInfo/'
    html = get_res(url, headers=headers).content.decode().replace(
        '\n', '').replace('\r', '')
    soup = BeautifulSoup(html, 'lxml')
    tr_list = soup.select('tr')
    tr_list.pop(0)
    tr_list.pop(0)
    for tr in tr_list:
        td_list = tr.select('td')
        # 期号
        qihao = td_list[0].get_text()
        # 开奖日期
        k_data = td_list[1].get_text()
        # 红球
        red_num_list = td_list[2:8]
        red_num = ''
        for red in red_num_list:
            red = red.get_text()
            red_num = red_num + red + ' '
        # 蓝球
        blue_num = td_list[8].get_text()
        # 总投注额
        z_money = td_list[9].string.replace(',', '')
        # 一等奖注数
        first_num = td_list[10].string
        # 一等奖奖金
        first_money = td_list[11].string.replace(',', '')
        # 二等奖注数
        second_num = td_list[12].string
        # 二等奖奖金
        second_money = td_list[13].string.replace(',', '')
        # 奖金滚存
        moneys = td_list[14].string.replace(',', '')
        # print(red_num)
        # print(blue_num)
        # print(z_money)
        # print(first_num)
        # print(first_money)
        # print(second_num)
        # print(second_money)
        # print(moneys)
        upda = {
            '期号': qihao,
            '开奖日期': k_data,
            '红球': red_num,
            '蓝球': blue_num,
            '总投注额': z_money,
            '一等奖注数': first_num,
            '一等奖奖金': first_money,
            '二等奖注数': second_num,
            '二等奖奖金': second_money,
            '奖金滚存': moneys
        }
        f_csv.writerow(upda)
        print(upda)
        print('*' * 50)
    else:
        f.close()


if __name__ == '__main__':
    get_shuang()
