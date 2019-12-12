# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)
"""
动作：
    在小红书 *首页* 栏的 *发现* 或 *郑州* 界面，做   自动点击进入>抓取信息>退出>
        自动点击进入>抓取信息>退出>自动点击进入>抓取信息>退出>循环操作
注意：
    全局没有去重处理，正常情况下会有很多重复信息
    全局没有做数据存储

去重方法：   
        1，mongoDB去重
        2，暂时将上层循环数据存入列表，在本次循环与上次循环数据依次比较，去除重复的同时
                将上层循环数据存储，依次执行，最后一层手动判断迭代临界值，直接存储
                ***注意字典型数据不能使用set去重（unhashable type: 'dict'）***
        3，没想出来
"""


# 滑屏
def huadong():
    poco.swipe([0.5, 0.8], [0.5, 0.2])


# 点击返回
def return_click():
    """
    目前只针对视频型信息页和普通型信息页，不知道有没有其他类型
    :return: None
    """
    try:
        poco("com.xingin.xhs:id/d9").click()
    except Exception as e:
        print(e)
        poco("com.xingin.xhs:id/backButton").click()


# 获取视频信息
def get_videos_data():
    """
    获取小红书视频型部分信息（不包括视频本体）
    :return: 单条信息，字典类型(dict)
    """
    # 用户昵称
    user = poco("com.xingin.xhs:id/matrixNickNameView").get_text()
    # 内容
    content = poco("com.xingin.xhs:id/noteContentText").get_text()
    # 点赞
    loved_num = poco("com.xingin.xhs:id/likeTextView").get_text()
    if loved_num == '点赞':
        loved_num = 0
    # 收藏
    vill_num = poco("com.xingin.xhs:id/id").get_text()
    if vill_num == '收藏':
        vill_num = 0
    # 评论
    reply_num = poco("com.xingin.xhs:id/commentTextView").get_text()
    if reply_num == '评论':
        reply_num = 0
    # 标签
    try:
        label_list = poco("com.xingin.xhs:id/b6g")
        label = ' '.join([l.get_text() for l in label_list])
    except Exception as e:
        print(e)
        label = '暂无标签'
    upda = {
        '用户昵称': user,
        '内容': content,
        '点赞数': loved_num,
        '收藏': vill_num,
        '评论': reply_num,
        '标签': label
    }
    return upda


# 获取主页控件
def get_menu():
    """
    获取当前屏幕所有信息块
    :return: 信息块迭代对象，列表类型(list)
    """
    menu_list = poco("com.xingin.xhs:id/b36").offspring("com.xingin.xhs:id/a8v").child("com.xingin.xhs:id/go")
    return menu_list


# 获取普通子页信息
def get_data():
    """
    获取小红书非视频型部分信息
    :return: 单条信息，字典类型(dict)
    """
    is_time = False
    is_content = False
    # 发布人
    user = poco("com.xingin.xhs:id/nickNameTV").get_text()
    # 地点
    try:
        address = poco("com.xingin.xhs:id/locationTV").get_text()
    except Exception as e:
        print(e)
        address = '暂无位置信息'
    # 喜欢
    loved_num = poco("com.xingin.xhs:id/amm").get_text()
    if loved_num == '点赞':
        loved_num = 0
    # 收藏
    vill_num = poco("com.xingin.xhs:id/alz").get_text()
    if vill_num == '收藏':
        vill_num = 0
    # 评论
    reply_num = poco("com.xingin.xhs:id/am4").get_text()
    if reply_num == '评论':
        reply_num = 0
    # 标题
    for j in range(2):
        try:
            if not is_content:
                content = poco("com.xingin.xhs:id/am7").get_text()
                is_content = True
        except Exception as e:
            print(e)
            pass
        try:
            if not is_time:
                # 发布时间
                put_time = poco("com.xingin.xhs:id/amp").get_text()
                is_time = True
        except Exception as e:
            print(e)
            pass
        try:
            title = poco("com.xingin.xhs:id/amv").get_text()
            break
        except Exception as e:
            print(e)
            huadong()
            title = '暂无标题信息'
    if not is_time:
        # 发布时间
        for k in range(5):
            try:
                put_time = poco("com.xingin.xhs:id/amp").get_text()
                break
            except Exception as e:
                print(e)
                huadong()
    # 内容
    if not is_content:
        try:
            content = poco("com.xingin.xhs:id/am7").get_text()
        except Exception as e:
            print(e)
            content = '暂无内容'
    # 标签
    try:
        label_list = poco("com.xingin.xhs:id/amx")
        label = ' '.join([l.get_text() for l in label_list])
    except Exception as e:
        print(e)
        label = '暂无标签'
    upda = {
        '用户昵称': user,
        '标题': title,
        '内容': content,
        '地点': address,
        '发布时间': put_time,
        '点赞数': loved_num,
        '收藏': vill_num,
        '评论': reply_num,
        '标签': label
    }
    return upda


# 识别并获取子页信息
def reco_get_data():
    """
    根据分享按钮的控件名称识别数据类型，并自动选择解析方法
    :return:
    """
    try:
        # 普通
        poco("com.xingin.xhs:id/moreOperateIV").get_name()
        print(get_data())
        print('*' * 50)
    except Exception as e:
        print(e)
        # 视频
        poco("com.xingin.xhs:id/shareButton").get_name()
        print(get_videos_data())
        print('*' * 50)


if __name__ == '__main__':
    for i in range(5):
        for menu in get_menu():
            menu.click()
            reco_get_data()
            return_click()
        else:
            huadong()
