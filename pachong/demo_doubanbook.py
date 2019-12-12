from Tools.tools import *
from Tools.ip_tools import get_res
from bs4 import BeautifulSoup
import csv


def spl(strs):
    one = strs.split('/', 1)
    two = one[1].rsplit('/', 1)
    return [one[0], two[0], two[1]]


def get_new_books():
    header = ['书名', '评分', '作者', '出版社', '发布日期', '简介信息']
    f = open('../data/newBook.csv', 'a', newline='', encoding='utf-8')
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    url = 'https://book.douban.com/latest'
    html = get_res(url, headers=headers).content.decode().replace('\r', '').replace('\n', '')
    soup = BeautifulSoup(html, 'lxml')
    div_list = soup.select('.detail-frame')
    for div in div_list:
        # 书名
        book_name = div.a.string
        # 评分
        score = div.select('span')[1].string.replace(' ', '')
        # 作者
        author_cbs_data = div.select('p[class="color-gray"]')[0].string.replace(' ', '')
        acd_list = spl(author_cbs_data)
        author = acd_list[0]
        # 出版社
        cbs = acd_list[1]
        # 发布日期
        put_data = acd_list[2]
        # 简介信息
        msg = div.select('p')[2].string.replace(' ', '')
        print('*****')
        upda = [book_name, score, author, cbs, put_data, msg]
        f_csv.writerow(upda)


if __name__ == '__main__':
    get_new_books()

