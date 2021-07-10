# -*- coding: utf-8 -*-
import random
import urllib.request
import json
from anobrowser import *
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
import xlrd
from numpy import *
import re
import requests
import time

na = 'a'
# 设置代理IP

iplist = ['112.228.161.57:8118', '125.126.164.21:34592', '122.72.18.35:80', '163.125.151.124:9999', '114.250.25.19:80']

proxy_addr = "125.126.164.21:34592"


# 定义页面打开函数
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http': random.choice(iplist)})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data = use_proxy(url, random.choice(iplist))
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if (data.get('tab_type') == 'weibo'):
            containerid = data.get('containerid')
    return containerid


def mirrorImages(url, dirt):
    ab = anobrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html)
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        filename = os.path.join(dirt, filename.replace('/', '_'))
        print('[+]Saving' + str(filename))
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'wb+')
        save.write(data)
        save.close()


# 获取微博账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等,并保存头像
def get_userInfo(id, path):
    id = str(id)
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    data = use_proxy(url, random.choice(iplist))
    ok = json.loads(data).get('ok')
    if ok == 1:
        content = json.loads(data).get('data')
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        na = name
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        print(
            "微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(
                verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(
                fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")
        path = path
        newpath = 'D:/touxiang/' + path
        mkdir(newpath)

        file = newpath + '/' + id + '.jpg'
        print(file)
        urlretrieve(profile_image_url, file)
    elif ok == 0:
        pass


# 获取微博内容信息,内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def mkdir(path):
    path = path.strip()  # strip方法只要含有该字符就会去除
    # 去除首尾\符号
    path = path.rstrip('\\')
    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 根据需要是否显示当前程序运行文件夹
    # print("当前程序所在位置为："+os.getcwd())

    if not isExists:
        os.makedirs(path)
        print(path + '创建成功')
        return True
    else:
        print(path + '目录已存在')
        return False


def get_weibo(id, file):
    i = 1
    Directory = 'D:/weibopinglun/'
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(
            url) + '&page=' + str(i)
        try:
            data = use_proxy(weibo_url, random.choice(iplist))
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if (len(cards) > 0):
                for j in range(len(cards)):
                    print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")
                    card_type = cards[j].get('card_type')
                    if (card_type == 9):
                        mblog = cards[j].get('mblog')
                        # print(mblog)
                        # print(str(mblog).find("转发微博"))
                        if str(mblog).find('retweeted_status') == -1:
                            if str(mblog).find('original_pic') != -1:
                                img_url = re.findall(r"'url': '(.+?)'", str(mblog))  ##pics(.+?)
                                n = 1
                                timename = str(time.time())
                                timename = timename.replace('.', '')
                                timename = timename[7:]  # 利用时间作为独特的名称
                                for url in img_url:
                                    print('第' + str(n) + ' 张', end='')
                                    with open(Directory + timename + url[-5:], 'wb') as f:
                                        f.write(requests.get(url).content)
                                    print('...OK!')
                                    n = n + 1
                            # if( n%3==0 ):  ##延迟爬取，防止截流
                            #  time.sleep(3)

                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[j].get('scheme')
                        text = mblog.get('text')
                        with open(file, 'a', encoding='utf-8') as fh:
                            fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                            fh.write("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                                created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                                attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                                reposts_count) + "\n")
                i += 1
            else:
                break
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    uid = xlrd.open_workbook('D:/relation.xlsx')#之前爬取到的关注对象列表
    sheet = uid.sheet_by_index(0)
    nrows = sheet.nrows
    fensi_list = []
    for i in range(1, 100):
        path = sheet.cell(i, 1).value
        id = sheet.cell(i, 2).value
        print(id, path)
        get_userInfo(id, path)
        print('进行到', i)

    # 以下代码为存取用户发布的微博到txt文档，为我个人做的爬虫小测试，由于内容繁杂没有放入本次实验
    # t = sheet.cell(1, 1).value
    # filename = 'D:/touxiang/'+str(t) + '.txt'
    # print(filename)
    # get_weibo(t, filename)
