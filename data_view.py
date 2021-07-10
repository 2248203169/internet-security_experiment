import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import heapq

# 实现数据可视化
# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
colors = ['r','b','g','y']

def result(file,row):
    data = pd.read_excel(file)
    data = data.dropna(axis=0)
    province = data[row]
    res = dict(Counter(province))
    province = list(set(province))

    y=[]
    for i in province:
        y.append(res[i])
    return province,y

def topn_dict(d, n):
    return heapq.nlargest(n, d, key=lambda k: d[k])

province,y = result('D:/user.xlsx','province')
gender,g = result('D:/user.xlsx','gender')

def top_result(file,row):
    data = pd.read_excel(file)
    data = data.dropna(axis=0)

    location = data[row]
    res = dict(Counter(location))
    location = topn_dict(res,5)
    l = []
    for i in location:
        l.append(res[i])
    return location,l


def num(file,id):
    data = pd.read_excel(file)
    data = data.dropna(axis=0)
    location = data[id]
    res = dict(Counter(location))
    location = topn_dict(res,4)
    l = []
    for i in location:
        l.append(res[i])
    lo = []
    for j in location:
        lo.append(str(j))
    return lo,l

relation,re = num("D:/userrelation.xlsx",'username')
topic,t = num('D:/weibo.xlsx','topic')

label,la = top_result('D:/网安实训/user.xlsx','label')
location,lo = top_result('D:/网安实训/user.xlsx','location')

plt.subplot(2,2,1)
plt.bar(province,y,color=colors,width=0.3)
for a,b in zip(province,y):
  plt.text(a, b+0.05, '%d' % a, ha='center', va= 'bottom',fontsize=11)
plt.subplot(2,2,2)
plt.bar(gender,g,color=colors,width=0.3)
plt.subplot(2,2,3)
plt.bar(label,la,color=colors,width=0.3)
plt.subplot(2,2,4)
plt.bar(location,lo,color = colors,width=0.3)
plt.show()

plt.subplot(2,2,1)
plt.bar(relation,re,color=colors)
plt.subplot(2,2,3)
plt.bar(topic,t,color=colors)
plt.show()

