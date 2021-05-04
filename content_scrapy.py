import json
# 导入爬取页面内容的模块
import requests


def get_weibo_userPublishContent(id):
    # 这个是我们要爬取内容的网址
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s' % (id)

    # 用text方法得到JSON字符串类型
    content = requests.get(url).text
    # 将其转换为python字典
    python_content_dic = json.loads(content)

    # 我们只能爬取到用户发布的最新10条内容
    for i in range(10):
        # 此为我们分析数据存储格式之后，定义的变量以及变量值的获取
        userContent = python_content_dic['data']['cards'][i]['mblog']
        publishClient = userContent['source']
        publishDate = userContent['created_at']
        publishContent = userContent['text']

        # 将爬取内容写入文件
        with open('doc/weiboContent.txt', 'a+') as f:
            f.writelines('发布日期:%s\n发布客户端:%s\n发布内容:%s\n\n' % (publishDate, publishClient, publishContent))

get_weibo_userPublishContent('1846360445')