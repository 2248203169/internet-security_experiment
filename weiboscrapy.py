# 导入爬取网页内容的模块
import  requests
import  json
import pandas as pd
from multiprocessing.pool import Pool
import time
import random
from selenium import webdriver
import xlwt

# 返回随机的User-Agent
def get_random_ua():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.5211 SLBChan/30"
    ]
    return {
        "User-Agent": random.choice(user_agent_list)
    }

def get_weibo_user_info(id):#获取用户信息列表
    url = "https://m.weibo.cn/api/container/getIndex?is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%s" %(id)
    content = requests.get(url,headers = get_random_ua()).text

    if not content:
        print("Error: 页面爬取错误")
        return  None
    python_content_dict = json.loads(content)
    print(content)

    userinfo = python_content_dict.get('data').get('userInfo')
    return userinfo

def getname(id):#获取用户名
    userinfo = get_weibo_user_info(id)
    print(id, userinfo)
    if userinfo:
        try:
            name = userinfo['screen_name']
        except Exception as e:
            name = ''
            print(e)
    else:
        print('Error: 该用户%s不存在' %(id))
    print(name)
    return name

def getdesc(id):#获取用户描述
    userinfo = get_weibo_user_info(id)
    if userinfo:
        try:
            desc = userinfo['description']
        except Exception as e:
            desc = ''
            print(e)
    else:
        print('Error: 该用户%s不存在' %(id))
    return desc

def getgender(id):#获取用户性别
    userinfo = get_weibo_user_info(id)
    if userinfo:
        try:
            if userinfo['gender'] == 'f':
                gender = 'f'
            else:
                gender = 'm'
        except Exception as e:
            gender = ''
            print(e)
    else:
        print("该用户%s不存在"%(id))
    print(gender)
    return gender

def getfollower(id):#获取粉丝数
    userinfo = get_weibo_user_info(id)
    if userinfo:
        try:
            followers = userinfo['followers_count']
        except Exception as e:
            print(e)
    else:
        print('Error: 该用户%s不存在' %(id))
    print(followers)
    return followers

def getfollow(id):#获取关注人数
    userinfo = get_weibo_user_info(id)
    if userinfo:
        try:
            follow = userinfo['follow_count']
        except Exception as e:
            print(e)
    else:
        print('Error: 该用户%s不存在' %(id))
    print(follow)
    return follow

def getverrify(id):#获取认证信息
    userinfo = get_weibo_user_info(id)
    if userinfo:
        try:
            if userinfo['verified'] == True:
                veri = userinfo['verified_reason']
            else:
                veri = ''
        except Exception as e:
            print(e)

    else:
        print('Error: 该用户%s不存在' %(id))

    return veri

def get_all_info(driver,id):
    driver.get('https://weibo.com/p/100505'+str(id)+'/info?mod=pedit_more')
    html = driver.page_source
    ss = html.split('<script>FM.view')

    ide = []
    ind = []
    index = []
    drop = []
    label = []
    all = []

    try:
        for i in range(len(ss)):
            if '<li class=\\"li_1 clearfix\\"><span class=\\"pt_title S_txt2\\">' in ss[i]:
                ide.append(i)
        sss = ss[ide[0]].split('<li class=\\"li_1 clearfix\\"><span class=\\"pt_title S_txt2\\">')
        for i in range(len(sss)):
            if '所在地' in sss[i]:
                ind.append(i)
            if '生日' in sss[i]:
                index.append(i)
            if '邮箱' in sss[i]:
                drop.append(i)
            if 'tag' in sss[i]:
                label.append(i)
    except Exception as e:
        for i in range(4):
            all.append('')
        print(e)
    try:
        ssss1 = sss[ind[0]].split('<\/span><span class=\\"pt_detail\\">')
        sssd = ssss1[1].split('<\/span><\/li>\\r\\n')
        all.append(sssd[0])
    except Exception as e:
        all.append('')
        print(e)
    try:
        ssss2 = sss[index[0]].split('<\/span><span class=\\"pt_detail\\">')
        sssb = ssss2[1].split('<\/span><\/li>\\r\\n')
        all.append(sssb[0])
    except Exception as e:
        all.append('')
        print(e)
    try:
        ssss3 = sss[drop[0]].split('<\/span><span class=\\"pt_detail\\">')
        ssse = ssss3[1].split('<\/span><\/li>\\r\\n')
        all.append(ssse[0])
    except Exception as e:
        all.append('')
        print(e)
    try:
        ssss4 = sss[label[0]].split('<\/span>\\r\\n')
        sssss = ssss4[2].split('<\/a>\\r\\n')
        sssl = sssss[0].strip()
        all.append(sssl)
    except Exception as e:
        all.append('')
        print(e)
    finally:
        time.sleep(10)
        print(all)
        return all

def data_to_file(file,name,desc,gender,followers,follow,veri,location,\
                 birth,email,label):
            with open(file, 'a+') as f:#file == 'D:/userinfo.txt'
                f.write("""
    微博用户:%s
    用户描述: %s        
    用户性别: %s
    粉丝数量： %s
    数量: %s
    官方认证信息: %s
    所在地:%s
    生日:%s
    邮箱:%s
    标签:%s
            """ %(name, desc, gender, followers, follow,veri,location,birth,\
                  email,label))
                f.close()

def data_to_excel(file,id,name,location,gender,follower,follow,birthday,\
                  email,label):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    ji = 1
    sheet1.write(0,0,'uid');sheet1.write(0,1,'screen_name')
    sheet1.write(0,2,'location');sheet1.write(0,3,'gender')
    sheet1.write(0,4,'followersum');sheet1.write(0,5,'followsum')
    sheet1.write(0,6,'birthday');sheet1.write(0,7,'email');sheet1.write(0,8,'label')
    for i in range(len(name)):
        sheet1.write(ji,0,str(id[i]));sheet1.write(ji,1,name[i])
        sheet1.write(ji,2,location[i]);sheet1.write(ji,3,gender[i])
        sheet1.write(ji,4,follower[i]);sheet1.write(ji,5,follow[i])
        sheet1.write(ji,6,birthday[i]);sheet1.write(ji,7,email[i]);sheet1.write(ji,8,label[i])
        ji += 1
    book.save(file)
    print("文件保存成功")

def excel_to_data(file):
    excel_name = file#file == "D:/information.xlsx"
    data = pd.read_excel(excel_name)  # 读取excel表格
    id_list = data['id']  # 获取列值
    return id_list

# 爬取用户的基本资料（性别和所在地）
def get_user_info(uid):
    uid_str = "230283" + str(uid)
    url2 = "https://m.weibo.cn/api/container/getIndex?containerid={}_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid={}&featurecode=10000326".format(
        uid_str, uid_str)
    data2 = {
        "containerid": "{}_-_INFO".format(uid_str),
        "title": "基本资料",
        "luicode": 10000011,
        "lfid": int(uid_str),
        "featurecode": 10000326
    }
    res2 = requests.get(url2, headers=get_random_ua(), data=data2)
    data = res2.json()['data']['cards'][1]
    print(data)
    if data['card_group'][0]['desc'] == '个人信息':
        add = data['card_group'][2]['item_content']
    else:
        add = data['card_group'][1]['item_content']
    # 对于所在地有省市的情况，把省份取出来
    if ' ' in add:
        add = add.split(' ')[0]
    print(add)
    return add

def main():
    id_list = excel_to_data('D:/id.xls')#此文件中保存要爬取的用户id,存在列名为"id"的列下

    suname = []
    sudesc = []
    sugender = []
    sufollowers = []
    sufollow = []
    suverrify = []
    addition = []
    birthday = []
    email = []
    label = []

    # 访问列表网站
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)

    driver.get('https://weibo.com/u/6004286722/home?wvr=5&sudaref=passport.weibo.com')

    time.sleep(10)
    driver.find_element_by_id('loginname').send_keys('user_id')#此处输入自己的微博账号完成预登录

    driver.find_element_by_name('password').send_keys('user_password')#此处输入自己的微博密码完成预登录

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

    #time.sleep(20)

    for id in id_list:
        try:
            suname.append(getname(id))
            sudesc.append(getdesc(id))
            sugender.append(getgender(id))
            sufollowers.append(getfollower(id))
            sufollow.append(getfollow(id))
            suverrify.append(getverrify(id))
            print("-----------3秒后爬取用户所在地、生日、邮箱、标签")
            time.sleep(3)
            all = get_all_info(driver,id)
            addition.append(all[0])
            birthday.append(all[1])
            email.append(all[2])
            label.append(all[3])
        except:
            suname.append('');sudesc.append('');sugender.append('');sufollowers.append('')
            sufollow.append('');suverrify.append('');addition.append('')
            birthday.append('');email.append('');label.append('')

    data_to_excel('D:/user_index.xlsx',id_list,suname,addition,\
                     sugender,sufollowers,sufollow,\
                     birthday,email,label)#爬取到数据保存在该文件中

main()