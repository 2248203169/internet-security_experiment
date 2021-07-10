from selenium import webdriver
import time
import xlwt
import pandas as pd

# 访问列表网站
driver = webdriver.Firefox()
driver.implicitly_wait(5)

driver.get('https://weibo.com/u/6004286722/home?wvr=5&sudaref=passport.weibo.com')

time.sleep(10)
driver.find_element_by_id('loginname').send_keys('user_id')#输入自己的微博账号

driver.find_element_by_name('password').send_keys('user_password')#输入自己的微博密码
#用自己的微博软件扫码

driver.find_element_by_class_name('W_btn_a ').click()

time.sleep(10)

try:
    if '"text=请输入验证码"' in driver.page_source:
        img_ele = driver.find_element_by_xpath('//img[@node-type="verifycode_image"]')

        image_url = img_ele.get_attribute('src')
        import requests

        response = requests.get(image_url)
        with open('verify_image.jpg', 'wb') as f:
            f.write(response.content)
        vares_img = input('请输入：\n')
        driver.find_element_by_name('verifycode').send_keys(vares_img)
        driver.find_element_by_class_name('W_btn_a ').click()
except Exception as e:
    print(e)

time.sleep(30)


def get_relation(id):
    ide = []
    sssu = []
    sssn = []
    sss = []
    try:
        driver.get('https://weibo.com/p/100505'+str(id)+'/follow?from=page_100505_profile&wvr=6&mod=modulerel')
        html = driver.page_source
        s = html.split('<script>FM.view')
        print("正在获取用户id:"+str(id))

        for i in range(len(s)):
            if "pl.content.followTab.index" in s[i]:
                ide.append(i)

        ss = s[ide[0]].split('action-data=\\"uid=')
        for i in range(len(ss)):
            if '&sex=' in ss[i]:
                sss.append(ss[i])

        for i in sss:
            a = i.split('&fnick=')
            b = a[1].split('&sex=')
            sssu.append(a[0])
            sssn.append(b[0])
    except Exception as e:
        sssu.append('')
        sssn.append('')
        print(e)
    time.sleep(3)
    return sssu,sssn


def data_to_excel(file,sid,tid,name):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    ji = 1
    sheet1.write(0,0,'suid');sheet1.write(0,1,'tuid');sheet1.write(0,2,'username')
    for i in range(len(sid)):
        for j in range(len(tid[i])):
            sheet1.write(ji, 0, str(sid[i]))
            sheet1.write(ji, 1, str(tid[i][j]))
            sheet1.write(ji, 2, name[i][j])
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
    uid = []
    name = []

    for i in id_list:
        u,n = get_relation(i)
        uid.append(u)
        name.append(n)

    data_to_excel('D:/relationship.xlsx',id_list,uid,name)#爬取到数据保存在该文件中

main()
