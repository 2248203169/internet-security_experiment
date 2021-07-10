import json
# 导入爬取页面内容的模块
import requests
import pandas as pd
import xlwt


def get_weibo_userPublishContent(id,fid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+fid

    content = requests.get(url).text
    python_content_dic = json.loads(content)
    print(python_content_dic)
    return python_content_dic

    # 只能爬取到用户发布的最新10条内容
def get_fid(id,fid):
    python_content_dic = get_weibo_userPublishContent(id,fid)
    fid = []
    for i in range(10):
        try:
                fid.append(python_content_dic['data']['cardlistInfo']['containerid'])
        except Exception as e:
            fid.append('')
            print(e)
    return fid

def get_mid(id,fid):
        python_content_dic = get_weibo_userPublishContent(id, fid)
        mid = []
        for i in range(10):
            try:
                mid.append(python_content_dic['data']['cardlistInfo']['since_id'])
            except Exception as e:
                mid.append('')
                print(e)
        return mid

def get_usercontent(id,fid):
    python_content_dic = get_weibo_userPublishContent(id,fid)
    user = []
    publishClient = []
    publishDate = []
    publishContent = []
    for i in range(10):
        try:
                userContent = python_content_dic['data']['cards'][i]['mblog']
                user.append(userContent)
                publishClient.append(userContent['source'])
                publishDate.append(userContent['created_at'])
                publishContent.append(userContent['text'])
        except Exception as e:
            user.append('')
            publishContent.append('')
            publishDate.append('')
            publishClient.append('')
            print(e)
    print(publishDate)
    print(publishContent)
    return user,publishClient,publishDate,publishContent

def data_to_file(file,fid,publishDate,publishClient,publishContent):
    try:
        # 将爬取内容写入文件
        with open(file, 'a+', encoding='utf-8') as f:#file == 'D:/网安实训/weiboContent.txt'
            f.writelines('用户id:%s\n发布日期:%s\n发布客户端:%s\n发布内容:%s\n\n' % (fid, publishDate, publishClient, publishContent))
    except Exception as e:
        print(e)

def data_to_excel(file,mid,fid,publishDate,publishClient,publishContent):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    ji = 1
    sheet1.write(0,0,'mid');sheet1.write(0,1,'date')
    sheet1.write(0,2,'text');sheet1.write(0,3,'source')
    sheet1.write(0,4,'uid');sheet1.write(0,5,'topic')
    for i in range(len(fid)):
        for j in range(10):
            sheet1.write(ji, 0, str(mid[i][j]))
            sheet1.write(ji, 1, publishDate[i][j])
            sheet1.write(ji, 2, publishContent[i][j])
            sheet1.write(ji, 3, publishClient[i][j])
            sheet1.write(ji, 4, fid[i][j].replace('107603',''))
            ji += 1

    book.save(file)
    print("文件保存成功")

def excel_to_data(file):
    excel_name = file#file=="D:/id.xls"
    data = pd.read_excel(excel_name)  # 读取excel表格
    id_list = data['id']  # 获取列值
    return id_list

def main():
    id_list = excel_to_data("D:/id.xls")#在该文件中保存列值为"id"的用户id列

    fid = []
    mid = []
    publishDate = []
    publishClient = []
    publishContent = []

    for id in id_list:
        fid.append(get_fid(str(id),'107603'+str(id)))#get_weibo_userPublishContent(str(id),'107603'+str(id))
        mid.append(get_mid(str(id),'107603'+str(id)))
        user,date,client,content = get_usercontent(str(id),'107603'+str(id))
        publishDate.append(date)
        publishClient.append(client)
        publishContent.append(content)

    data_to_excel('D:/Content.xlsx',mid,fid,publishClient,\
                         publishDate,publishContent)#爬取到数据保存在该文件中

main()
