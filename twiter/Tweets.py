import requests
import re
import csv
"""
有一点缺陷，就是随着url循环次数的增加，很有可能取到重复的url
"""


def quchong(data: list):
    return list(set(data))


def get_tweet_url(data: list):
    return ['https://twitter.com' + i for i in quchong(list(filter(lambda x: len(x) < 50, data)))]


def get_u_url(data: list):
    return ['https://twitter.com' + i for i in quchong([re.findall(r'com(/.*?)/status', i, re.S)[0] for i in data])]


def old_url(data=None):
    if data:
        with open('old_url.csv', 'a+', encoding='utf-8') as fw1:
            fc = csv.writer(fw1)
            fc.writerow([data])
    else:
        with open('old_url.csv', 'r', encoding='utf-8') as fr:
            old_ = csv.reader(fr)
            return [x[0] for x in old_ if x]


def new_url(data=None):
    if data:
        fw1 = open('new_url.csv', 'w', encoding='utf-8')
        for i in data:
            fc = csv.writer(fw1)
            fc.writerow([i])
        else:
            fw1.close()
    else:
        with open('new_url.csv', 'r', encoding='utf-8') as fr:
            new_ = csv.reader(fr)
            return [x[0] for x in new_ if x]


def get_Tweet(url):
    global start_urls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3'
                      '945.117 Safari/537.36'
    }
    res_1 = requests.get(url, headers=headers)
    tweet_url = re.findall(r'href="(/.*?/status/\d{16,19})"', res_1.text)
    # 推文链接，存起来
    tweet_urls = get_tweet_url(tweet_url)
    u_url = get_u_url(tweet_urls)
    for i in u_url:
        if i not in new_url() and i not in old_url():
            start_urls.append(i)
        else:
            continue
    temp_urls = [[x] for x in tweet_urls]
    f_csv.writerows(temp_urls)


def main():
    for i in range(10):
        if start_urls:
            start_url = start_urls.pop(0)
            old_url(start_url)
            print('本次取出：{0}'.format(start_url))
            print('*' * 50)
            get_Tweet(start_url)
        else:
            print('start_urls空了')
            break
    else:
        print('剩余：{0}'.format(start_urls))


if __name__ == '__main__':
    start_urls = new_url()
    if not start_urls:
        start_urls = ['https://twitter.com/NSWRFS']
    fw = open('tweet_url.csv', 'a+', encoding='utf-8')
    f_csv = csv.writer(fw)
    main()
    fw.close()
    new_url(start_urls)

