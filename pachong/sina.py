from functools import reduce

import requests
import re

# url = 'https://s.weibo.com/weibo'
headers = {
    'Cookie': 'SINAGLOBAL=9239753195656.152.1568647114764; UOR=news.ifeng.com,widget.weibo.'
              'com,www.baidu.com; un=15896963082; wvr=6; ALF=1606458629; SSOLoginState=157492'
              '2630; SCF=Ag5TKmS3fVkJPVCz0oDXE5uZzHpXsMwdROLwPyzGi0txsgYiLIqNZwD3Ki9SdYjNAFT'
              'Grl0anu16tqqmAAOjTYQ.; SUB=_2A25w2xnXDeRhGeNJ7FYQ-CnIwjSIHXVTkQwfrDV8PUNbmtBeL'
              'UXwkW9NS7Lw2jmuQNYqTKmFOt4ba6esxPl8K3WV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D'
              '9WF30zdmw2JIMljmJIN.rejD5JpX5KzhUgL.Fo-NS0Bp1hMX1Kn2dJLoIX5LxKBLB.BL1K-LxKBLB.'
              '2L12zLxKMLBKML12zLxK.LBKeL12-LxKqL1hzLBozLxKML1KBLB.zLxKqL1h.L1hUE; SUHB=0N21l'
              'lHWR0sk8v; _s_tentry=login.sina.com.cn; Apache=4615398128409.845.1574922635580'
              '; ULV=1574922635640:4:3:2:4615398128409.845.1574922635580:1574922458295; webim'
              '_unReadCount=%7B%22time%22%3A1574922646804%2C%22dm_pub_total%22%3A0%2C%22chat_g'
              'roup_client%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D; WBStorage=422'
              '12210b087ca50|undefined',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/78.0.3904.108 Safari/537.36',
    'Referer': 'https://s.weibo.com/weibo?q=2019%E8%92%B8%E8%92%B8%E6%97%A5%E4%B8%8A%E8%BF%8E%E6%96'
               '%B0%E8%B7%91&wvr=6&b=1&Refer=SWeibo_box'
}
# params = {
#     'q': '2019蒸蒸日上迎新跑',
#     'wvr': '6',
#     'b': '1',
#     'Refer': 'SWeibo_box',
#     'page': '2'
# }
# html = requests.get(url, headers=headers, params=params).content.decode('utf-8')
# print(html)

# url = 'https://weibo.com/u/3104482655?refer_flag=1001030103_&is_hot=1'
# res = requests.get(url, headers=headers).content.decode('utf-8')
# str1 = r'<strong class=\"W_f18\">323<\/strong><span class=\"S_txt2\">关注<\/span><\/a><\/td>\r\n\t\t\t\t\t\
# t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\"S_line1\">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\
# t\t\t\t\t\t\t\t<a bpfilter=\"page_frame\"  class=\"t_link S_txt1\" href=\"\/\/weibo.com\/p\/1005053104482655' \
#        r'\/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place\" ><strong class=\"W_f18\"' \
#        r'>476<\/strong><span class=\"S_txt2\">粉丝<\/span><\/a><\/td>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t' \
#        r'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\"S_line1\">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\
#        t<a bpfilter=\"page_frame\"  class=\"t_link S_txt1\" href=\"\/\/weibo.com\/p\/1005053104482655\/home?' \
#        r'from=page_100505_profile&wvr=6&mod=data#place\" ><strong class=\"W_f18\">6712<\/strong><span class=\
#        "S_txt2\">微博<\/span><\/a><\/td>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<\/' \
#        r'tr>\r\n\t\t\t\t\t\t\t\t\t<\/tbody>'
#
# res = re.findall(r'W_f18\\">(.*?)<', str1, re.S)
# print(res)


str1 = """
<div class="num-wrap"><span>--</span></div><div class="nav-name">科技</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/technology/fun/"><span>趣味科普人文</span></a></li><li><a href="//www.bilibili.com/v/technology/wild/"><span>野生技术协会</span></a></li><li><a href="//www.bilibili.com/v/technology/speech_course/"><span>演讲·公开课</span></a></li><li><a href="//www.bilibili.com/v/technology/military/"><span>星海</span></a></li><li><a href="//www.bilibili.com/v/technology/mechanical/"><span>机械</span></a></li><li><a href="//www.bilibili.com/v/technology/automobile/"><span>汽车</span></a></li></ul></li><li><a href="//www.bilibili.com/v/digital/"><div class="num-wrap"><span>--</span></div><div class="nav-name">数码</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/digital/mobile/"><span>手机平板</span></a></li><li><a href="//www.bilibili.com/v/digital/pc/"><span>电脑装机</span></a></li><li><a href="//www.bilibili.com/v/digital/photography/"><span>摄影摄像</span></a></li><li><a href="//www.bilibili.com/v/digital/intelligence_av/"><span>影音智能</span></a></li></ul></li><li><a href="//www.bilibili.com/v/life/"><div class="num-wrap"><span>--</span></div><div class="nav-name">生活</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/life/funny/"><span>搞笑</span></a></li><li><a href="//www.bilibili.com/v/life/daily/"><span>日常</span></a></li><li><a href="//www.bilibili.com/v/life/food/"><span>美食圈</span></a></li><li><a href="//www.bilibili.com/v/life/animal/"><span>动物圈</span></a></li><li><a href="//www.bilibili.com/v/life/handmake/"><span>手工</span></a></li><li><a href="//www.bilibili.com/v/life/painting/"><span>绘画</span></a></li><li><a href="//www.bilibili.com/v/life/sports/"><span>运动</span></a></li><li><a href="//www.bilibili.com/v/life/other/"><span>其他</span></a></li></ul></li><li><a href="//www.bilibili.com/v/kichiku/"><div class="num-wrap"><span>--</span></div><div class="nav-name">鬼畜</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/kichiku/guide/"><span>鬼畜调教</span></a></li><li><a href="//www.bilibili.com/v/kichiku/mad/"><span>音MAD</span></a></li><li><a href="//www.bilibili.com/v/kichiku/manual_vocaloid/"><span>人力VOCALOID</span></a></li><li><a href="//www.bilibili.com/v/kichiku/course/"><span>教程演示</span></a></li></ul></li><li><a href="//www.bilibili.com/v/fashion/"><div class="num-wrap"><span>--</span></div><div class="nav-name">时尚</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/fashion/makeup/"><span>美妆</span></a></li><li><a href="//www.bilibili.com/v/fashion/clothing/"><span>服饰</span></a></li><li><a href="//www.bilibili.com/v/fashion/aerobics/"><span>健身</span></a></li><li><a href="//www.bilibili.com/v/fashion/catwalk/"><span>T台</span></a></li><li><a href="//www.bilibili.com/v/fashion/trends/"><span>风尚标</span></a></li></ul></li><li><a href="//www.bilibili.com/v/ad/ad/"><div class="num-wrap"><span>--</span></div><div class="nav-name">广告</div></a><ul class="sub-nav"><!----></ul></li><li><a href="//www.bilibili.com/v/ent/"><div class="num-wrap"><span>--</span></div><div class="nav-name">娱乐</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/ent/variety/"><span>综艺</span></a></li><li><a href="//www.bilibili.com/v/ent/star/"><span>明星</span></a></li><li><a href="//www.bilibili.com/v/ent/korea/"><span>Korea相关</span></a></li></ul></li><li><a href="//www.bilibili.com/v/cinephile/"><div class="num-wrap"><span>--</span></div><div class="nav-name">影视</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/v/cinephile/cinecism/"><span>影视杂谈</span></a></li><li><a href="//www.bilibili.com/v/cinephile/montage/"><span>影视剪辑</span></a></li><li><a href="//www.bilibili.com/v/cinephile/shortfilm/"><span>短片</span></a></li><li><a href="//www.bilibili.com/v/cinephile/trailer_info/"><span>预告·资讯</span></a></li></ul></li><li><a href="//www.bilibili.com/cinema/"><div class="num-wrap"><span>--</span></div><div class="nav-name">放映厅</div></a><ul class="sub-nav"><li><a href="//www.bilibili.com/documentary/"><span>纪录片</span></a></li><li><a href="//www.bilibili.com/movie/"><span>电影</span></a></li><li><a href="//www.bilibili.com/tv/"><span>电视剧</span></a></li></ul></li><li class="side-nav zl"><a href="//www.bilibili.com/read/home" class="side-link">
"""
res = re.findall(r'<.*?>(.*?)<.*?>', str1, re.S)
print(res)


class Foo(object):
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):

        if cls.__instance:
            return cls.__instance
        else:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
            return cls.__instance


li = [
    {'name': 'zs', 'age': 18},
    {'name': 'ls', 'age': 15},
    {'name': 'ww', 'age': 24},
    {'name': 'zl', 'age': 9},
]

li_1 = sorted(li, key=lambda a: a['age'], reverse=True)
print(li_1)
