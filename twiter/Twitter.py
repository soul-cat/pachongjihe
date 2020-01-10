import requests
import twitter
from Tools.tools import time_13
import re

s = requests.session()
"""
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA

https://abs.twimg.com/responsive-web/web/main.ef42eb84.js
https://abs.twimg.com/responsive-web/web/main.ef42eb84.js
链接也是一样的，看什么时候值变了，链接会不会变
"""


# 点赞
def zan(art_id, cookie):
    url = 'https://api.twitter.com/1.1/favorites/create.json'
    headers = get_headers(cookie)
    params = {
        'tweet_mode': 'extended',
        'id': art_id
    }
    res = s.post(url, headers=headers, data=params, verify=False).json()
    try:
        return {
            'code': 1,
            'msg': '点赞成功',
            'id': res['id']
        }
    except:
        return error(res)


# 一级评论
def reply_one(art_id, reply_text, cookie):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    headers = get_headers(cookie)
    params = {
        'include_profile_interstitial_type': 1,
        'include_blocking': 1,
        'include_blocked_by': 1,
        'include_followed_by': 1,
        'include_want_retweets': 1,
        'include_mute_edge': 1,
        'include_can_dm': 1,
        'include_can_media_tag': 1,
        'skip_status': 1,
        'cards_platform': 'web-12',
        'include_cards': 1,
        'include_composer_source': 'true',
        'include_ext_alt_text': 'true',
        'include_reply_count': 1,
        'tweet_mode': 'extended',
        'simple_quoted_tweet': 'true',
        'trim_user': 'false',
        'include_ext_media_color': 'true',
        'include_ext_media_availability': 'true',
        # 是否直接在新闻下，还是别人的评论
        'auto_populate_reply_metadata': 'false',
        'batch_mode': 'off',
        'semantic_annotation_ids': '13.125.{0}'.format(art_id),
        'status': reply_text
    }
    res = s.post(url, headers=headers, data=params, verify=False).json()
    print(res)
    try:
        return {
            'code': 1,
            'msg': '评论成功',
            'id': res['id']
        }
    except:
        print(res)
        return error(res)


# 二级评论
def reply_two(art_id, reply_text, cookie):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    headers = get_headers(cookie)
    params = {
        'include_profile_interstitial_type': 1,
        'include_blocking': 1,
        'include_blocked_by': 1,
        'include_followed_by': 1,
        'include_want_retweets': 1,
        'include_mute_edge': 1,
        'include_can_dm': 1,
        'include_can_media_tag': 1,
        'skip_status': 1,
        'cards_platform': 'web-12',
        'include_cards': 1,
        'include_composer_source': 'true',
        'include_ext_alt_text': 'true',
        'include_reply_count': 1,
        'tweet_mode': 'extended',
        'simple_quoted_tweet': 'true',
        'trim_user': 'false',
        'include_ext_media_color': 'true',
        'include_ext_media_availability': 'true',
        # 是否直接在新闻下，还是别人的评论
        'auto_populate_reply_metadata': 'true',
        'batch_mode': 'off',
        'in_reply_to_status_id': art_id,
        'status': reply_text
    }
    res = s.post(url, headers=headers, data=params, verify=False).json()
    print(res)
    try:
        return {
            'code': 1,
            'msg': '评论成功',
            'id': res['id']
        }
    except:
        print(res)
        return error(res)


# 转推
def zhuan(art_id, cookie):
    url = 'https://api.twitter.com/1.1/statuses/retweet.json'
    headers = get_headers(cookie)
    params = {
        'tweet_mode': 'extended',
        'id': art_id
    }
    res = s.post(url, headers=headers, data=params).json()
    try:
        return {
            'code': 1,
            'msg': '转发成功',
            'id': res['id']
        }
    except:
        print(res)
        return error(res)


# 带评论转推
def zhuan_com(attachment_url, reply_text, cookie):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    headers = get_headers(cookie)
    params = {
        'include_profile_interstitial_type': 1,
        'include_blocking': 1,
        'include_blocked_by': 1,
        'include_followed_by': 1,
        'include_want_retweets': 1,
        'include_mute_edge': 1,
        'include_can_dm': 1,
        'include_can_media_tag': 1,
        'skip_status': 1,
        'cards_platform': 'web-12',
        'include_cards': 1,
        'include_composer_source': 'true',
        'include_ext_alt_text': 'true',
        'include_reply_count': 1,
        'tweet_mode': 'extended',
        'simple_quoted_tweet': 'true',
        'trim_user': 'false',
        'include_ext_media_color': 'true',
        'include_ext_media_availability': 'true',
        'attachment_url': attachment_url,
        'auto_populate_reply_metadata': 'false',
        'batch_mode': 'off',
        'status': reply_text
    }
    res = s.post(url, data=params, headers=headers).json()
    print(res)
    try:
        return {
            'code': 1,
            'msg': '评论成功',
            'id': res['id']
        }
    except:
        return error(res)


# 登录
def login(username, password):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                      '3945.88 Safari/537.36'
    }
    url_0 = 'https://twitter.com/'
    url_1 = 'https://twitter.com/i/js_inst?c_name=ui_metrics'
    url_2 = 'https://twitter.com/sessions'
    authenticity_token = ''
    for i in range(3):
        try:
            res_0 = s.get(url_0, headers=header)
            print(res_0)
            authenticity_token = re.findall(r'value="(.*?)".*?authenticity_token', res_0.text, re.S)[0]
            break
        except:
            pass
    if not authenticity_token:
        return {
            'code': 101,
            'msg': 'authenticity_token获取失败'
        }
    # input('阻塞，上一步是获取首页，并获取cookie')
    res_1 = s.get(url_1, headers=header)
    print(res_1)
    # input('阻塞，上一步是获取首页，并获取cookie')
    params = {
        'session[username_or_email]': username,
        'session[password]': password,
        'return_to_ssl': 'true',
        'scribe_log': '',
        'redirect_after_login': '/',
        'authenticity_token': authenticity_token,
    }
    res_2 = s.post(url_2, data=params, headers=header)
    print(res_2.text)
    cookie = ''
    code = 1
    msg = '登陆成功'
    if 'password you entered did not match our records. Please double-check and try again' in res_2.text:
        code = 3
        msg = '账户名或密码错误'
    elif 'asked to confirm you’re not a robot. Easy, right?' in res_2.text:
        code = 4
        msg = 'robot验证'
    elif 'You’ll use the code to verify this is really your number' in res_2.text:
        code = 5
        msg = 'phone number 验证'
    else:
        cookie = "auth_token={0};ct0={1};".format(s.cookies.get('auth_token'), s.cookies.get('ct0'))
    return {
        'code': code,
        'cookie': cookie,
        'msg': msg
    }


# 发推文
def put_tui(text, cookie):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    headers = get_headers(cookie)
    params = {
        'include_profile_interstitial_type': 1,
        'include_blocking': 1,
        'include_blocked_by': 1,
        'include_followed_by': 1,
        'include_want_retweets': 1,
        'include_mute_edge': 1,
        'include_can_dm': 1,
        'include_can_media_tag': 1,
        'skip_status': 1,
        'cards_platform': 'web-12',
        'include_cards': 1,
        'include_composer_source': 'true',
        'include_ext_alt_text': 'true',
        'include_reply_count': 1,
        'tweet_mode': 'extended',
        'simple_quoted_tweet': 'true',
        'trim_user': 'false',
        'include_ext_media_color': 'true',
        'include_ext_media_availability': 'true',
        # 是否直接在新闻下，还是别人的评论
        'auto_populate_reply_metadata': 'false',
        'batch_mode': 'off',
        'status': text
    }
    res = s.post(url, headers=headers, data=params, verify=False).json()
    try:
        return {
            'code': 1,
            'msg': '发布成功',
            'art_id': res['id']
        }
    except:
        return error(res)


# json类型code错误集
def error(res):
    if res.get('errors'):
        if res['errors'][0]['code'] == 89:
            code = 2
            msg = 'authenticity_token失效'
        elif res['errors'][0]['code'] == 353:
            code = 3
            msg = 'csrf_token不匹配'
        elif res['errors'][0]['code'] == 32:
            code = 4
            msg = '登陆状态失效'
        elif res['errors'][0]['code'] == 187:
            code = 6
            msg = '发布过重复内容，不可重发'
        elif res['errors'][0]['code'] == 326:
            code = 7
            msg = '账户被锁定'
        elif res['errors'][0]['code'] == 139:
            code = 8
            msg = '已经点赞过，无需重复点赞'
        elif res['errors'][0]['code'] == 327:
            code = 9
            msg = '已经转过'
        else:
            code = 5
            msg = '未知'
        return {
            'code': code,
            'msg': msg
        }
    else:
        return {
            'code': 100,
            'msg': '未知2'
        }


def get_headers(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                      '3945.88 Safari/537.36',
        'Cookie': cookie,
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cH'
                         'jhLTvJu4FA33AGWWjCpTnA',
        'x-csrf-token': re.findall(r'ct0=(.*?);', cookie, re.S)[0]
    }
    return headers


def get_proxy():
    try:
        proxy = requests.get('http://114.219.157.215:8000/proxy/checked/get_next/').json()
        return proxy
    except Exception as e:
        return None


if __name__ == '__main__':
    # print(login('m17139455368@163.com', 'ceshi123'))
    # print(zhuan_com('https://twitter.com/CBCToronto/status/1214260670142791685', 'chang ban wu shen', 'auth_token=bf1f968f0c8870141e35af6e2511d2754e8a0393;ct0=07b8feed59b785f70727fb92812d068a;'))
    proxy = None
    res = requests.get('http://2000019.ip138.com/', proxies=proxy)
    print(res.content.decode())
    print(proxy)
    """
    The phone number and password you entered did not match our records. Please double-check and try again
    The email and password you entered did not match our records. Please double-check and try again
    """
