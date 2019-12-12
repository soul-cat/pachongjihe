from fontTools.ttLib import TTFont

'''
&#xf4cc;    9
&#xeab4;    4

&#xe585;
&#xf09d;
'''
# 实例化font对象
# font = TTFont('../data/maoyan2.woff')
# font.saveXML('font2.xml')
# 提取cmap节点
# font_data_dict = font.getGlyphOrder()
# print(font_data_dict)
# 只要value
# for value in font_data_dict.value:
#     print(value)

import requests

import re

import os

from fontTools.ttLib import TTFont


class MaoYan():

    # 初始化需要的数据
    def __init__(self):

        self.url = 'http://maoyan.com/films/1209159'

        self.headers = {

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHT"
                          "ML,             like Gecko) Chrome/70.0.3538.110 Safari/537.36",

        }

    # 发送请求
    def get_html(self, url):

        response = requests.get(url, headers=self.headers)

        return response.content

    # 下载woff字体文件

    def create_font(self, font_file):

        # 列出已下载文件

        file_list = os.listdir('./fonts')

        # 判断是否已下载

        if font_file not in file_list:
            # 未下载则下载新woff字体文件

            url = 'http://vfile.meituan.net/colorstone/' + font_file

            new_file = self.get_html(url)

            with open('./fonts/' + font_file, 'wb')as f:
                f.write(new_file)

        # 打开字体文件

        self.font = TTFont('./fonts/' + font_file)

    # 把获取到的数据用字体对应起来，得到真实数据

    def modify_data(self, data):

        # 打开自己保存的woff文件，设置映射关系

        font2 = TTFont("./95ebcb3e871c993e8014b6cf244c939b2088.woff")

        keys = font2['glyf'].keys()

        values = list(' .0714682953')

        # 对应替换

        dict1 = dict((k, v) for k, v in zip(keys, values))

        font1 = self.font

        # 空字典，保存新的替换映射关系

        dict2 = {}

        for key in font1["glyf"].keys():

            for k, v in dict1.items():

                # 通过比较 字形定义 填充新的name和num映射关系

                if font2["glyf"][k] == font1["glyf"][key]:
                    dict2[key] = v.strip()

                    break

        # 将获取到的网页数据中的&#x替换成uni

        for i in dict2:

            gly = i.replace('uni', '&#x').lower() + ';'

            if gly in data:
                data = data.replace(gly, dict2[i])

        return data

    # 获取数据

    def start_crawl(self):

        html = self.get_html(self.url).decode('utf-8')

        # 正则匹配字体文件

        font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', html)[0]

        self.create_font(font_file)

        # 正则匹配评分

        star = \
            re.findall(r'<span class="index-left info-num ">\s+<span class="stonefont">(.*?)</span>\s+</span>', html)[0]

        star = self.modify_data(star)

        # 正则匹配想看的人数

        people = re.findall(r'<span class=".*?score-num.*?">(.*?)</span>', html, re.S)[0]

        people = self.modify_data(people)

        # 正则匹配累计票房

        ticket_number = re.findall(
            r'<div class="movie-index-content box">\s+<span class="stonefont">(.*?)'
            r'</span><span class="unit">(.*?)</span>\s+</div>',
            html)[0]

        ticket_number1 = self.modify_data(ticket_number[0])

        print('用户评分: %s' % star)

        print('评分人数: %s' % people)

        print('累计票房: %s' % ticket_number1, ticket_number[1])


if __name__ == '__main__':
    maoyan = MaoYan()

    maoyan.start_crawl()
