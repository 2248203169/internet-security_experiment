#筛选出有邮箱信息、个人标签的用户
import pandas as pd
import xlwt
import numpy as np

iris = pd.read_excel("D:/user.xlsx")
df = pd.read_excel("D:/user_relationship.xlsx")
suid = df['suid']
username = df['username']
email = iris['email']
label = iris['label']
uid = iris['uid']
name = iris['screen_name']
location = iris['location']
gender = iris['gender']

index = [];ind = [];u = []
n = [];l = [];g = []
li = [];e = [];la = [];us = []
suid = list(suid)

for i in range(len(email)):
    if pd.isnull(email[i]) or pd.isnull(label[i]):
        pass
    else:
        index.append(i)

print(index)

for x in index:
    u.append(uid[x])
    n.append(name[x])
    l.append(location[x])
    g.append(gender[x])
    e.append(email[x])
    la.append(label[x])

for j in u:
    try:
        num = suid.index(j)
        ind.append(num)
    except:
        ind.append('')

for y in ind:
    try:
        us.append(username[y])
    except:
        us.append('')

book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')
ji = 1
sheet1.write(0,0,'uid');sheet1.write(0,1,'screen_name');sheet1.write(0,2,'location')
sheet1.write(0,3,'gender');sheet1.write(0,4,'liker')
sheet1.write(0,5,'email');sheet1.write(0,6,'label')
for i in range(len(u)):
            sheet1.write(ji, 0, str(u[i]))
            sheet1.write(ji, 1, n[i])
            sheet1.write(ji, 2, l[i])
            sheet1.write(ji, 3, g[i])
            sheet1.write(ji, 4, us[i])
            sheet1.write(ji, 5, e[i])
            sheet1.write(ji, 6, la[i])
            ji += 1
book.save('D:/information.xlsx')#数据保存在该文件中
print("文件保存成功")