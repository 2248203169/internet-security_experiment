#发送钓鱼邮件
import smtplib
import pandas as pd
from email.mime.image import MIMEImage
from email.header import Header
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
from threading import Timer
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import time, os, random, zipfile, smtplib

df = pd.read_excel('D:/163.xls')#保存网易邮箱的账号，smtp授权码
username = df['username']#账号，对应列名"username"
password = df['password']#smtp授权码，对应列名"password"
dp = pd.read_excel('D:/information.xlsx')
screen_name = dp['screen_name']
location = dp['location']
gender = dp['gender']
liker = dp['liker']
email = dp['email']
topic = dp['label']
uid = dp['uid']
day = dp['birthday']

def ModifyFileTime(filePath, lastTime):
    #构造时间
    fh = CreateFile(filePath, GENERIC_READ|GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
    offsetSec=random.randint(1200, 1500)
    cTime, aTime, wTime = GetFileTime(fh)
    aTime = Time(time.mktime(lastTime) - offsetSec)
    wTime = Time(time.mktime(lastTime) - offsetSec)
     #修改时间属性
    SetFileTime(fh, cTime, aTime, wTime)
    CloseHandle(fh)

def sendmail_excute(user,pwd,to,like1,subject,text,fileP):
    from_addr = user
    password = pwd
    to_addr = to
    smtp_server = 'smtp.163.com'

    pdfFile = fileP
    pdfApart = MIMEApplication(open(pdfFile, 'rb').read())
    pdfApart.add_header('Content-Disposition', 'attachment', filename=pdfFile)

    msg_file = MIMEMultipart()
    msg_file['From'] = Header(str(like1)+"的官方邮箱", 'utf-8')
    msg_file['To'] = Header(to_addr)
    msg = MIMEText(text, 'plain', 'utf-8')
    msg_file.attach(msg)
    msg_file.attach(pdfApart)
    msg_file['Subject'] = Header(subject,'utf-8')

    server = smtplib.SMTP(smtp_server, 25)
    server.starttls()
    server.ehlo()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg_file.as_string())
    server.quit()

def PreparingFilesAndSend(user,pwd,to,like1,subject,text,fileP,runTime):
    ModifyFileTime(fileP, runTime)
    #发送邮件
    sendmail_excute(user,pwd,to,like1,subject,text,fileP)

def TimedTask(user,pwd,to,like1,subject,text,filePath, runTime):
    interval = time.mktime(runTime) - time.mktime(time.localtime())
    Timer(interval, PreparingFilesAndSend, args=(user,pwd,to,like1,subject,text,filePath, runTime)).start()
    print("sending success")

def sendmail(user,pwd,to,like1,subject,text):
    msg = MIMEMultipart('related')

    message_html = MIMEText(text)
    # 将邮件内容装入的邮件信息中
    msg.attach(message_html)
    msg['From'] = Header(str(like1)+"的官方邮箱", 'utf-8')
    msg['To'] = to
    msg['Subject'] = Header(subject,'utf-8')
    try:
        smtpserver = smtplib.SMTP('smtp.163.com',25)
        print("connecting to  mail server>>>")
        smtpserver.ehlo()
        print("starting encrypted session>>>")
        smtpserver.starttls()
        smtpserver.ehlo()
        print("logging into mail server>>>")
        smtpserver.login(user,pwd)
        print("sending mail>>>")
        smtpserver.sendmail(user,to,msg.as_string())
        smtpserver.close()
        print("mail send successfully!!!")
    except Exception as e:
        print(e)

def sendmail_picture(user,pwd,to,like1,subject,text,draw):
    msg = MIMEMultipart('related')

    message_html = MIMEText(text+'<img src="cid:small">', 'html',
                            'utf-8 ')
    # 将邮件内容装入的邮件信息中
    msg.attach(message_html)

    # -----------------------发送图片--------------
    # rb 读取二进制文件
    image_data = open(draw, 'rb')
    # 设置读取获取的二进制文件
    message_img = MIMEImage(image_data.read())
    # 关闭刚刚打开的文件
    image_data.close()
    message_img.add_header('Content-ID', 'small')
    # 添加图片文件到邮件信息中
    msg.attach(message_img)

    msg['From'] = Header(str(like1)+"的官方邮箱", 'utf-8')
    msg['To'] = to
    msg['Subject'] = subject
    try:
        smtpserver = smtplib.SMTP('smtp.163.com',25)
        print("connecting to  mail server>>>")
        smtpserver.ehlo()
        print("starting encrypted session>>>")
        smtpserver.starttls()
        smtpserver.ehlo()
        print("logging into mail server>>>")
        smtpserver.login(user,pwd)
        print("sending mail>>>")
        smtpserver.sendmail(user,to,msg.as_string())
        smtpserver.close()
        print("mail send successfully!!!")
    except Exception as e:
        print(e)


def main():
    a = 0
    for i in range(len(screen_name)):
        c = random.randint(0,8)
        user = username[c]
        pwd = password[c]
        handle = screen_name[i]
        tgt = email[i]
        if handle == None or tgt == None or user == None or pwd==None:
            print("please input again")
            exit(0)
        print("fetching weibo from:"+str(handle))
        location1 = location[i];gender1 = gender[i]
        liker1 = liker[i];topic1 = topic[i]
        uid1 = uid[i]
        if gender1 == 'm':
            call = '女士'
        elif gender1 == 'f':
            call = '先生'
        else:
            call = ''
        spammsg = "亲爱的微博用户"+handle+call+"：您好!\n我是"+liker1+"，您所在的"+location1+\
                    "即将开展有关"+str(topic1)+"的线下活动，查看具体详情请前往http://mlb.mlb.com"
        spam = "亲爱的微博用户"+handle+call+"：您好!\n我是"+liker1+"\n请获取附件，查收我送给您的生日贺卡"
        print("sending message:"+spammsg)
        picture = 'D:/guanzhutouxiang/'+str(uid1)+'.jpg'#保存关注头像
        fp = r"D:/生日贺卡.exe"
        rt = "2021-6-17 6:00:00"#设置成用户的生日
        # 转化为结构化时间
        timeFormat = "%Y-%m-%d %H:%M:%S"
        s_time = time.strptime(rt, timeFormat)
        choose = input("你想实现的邮箱发送方式是发送普通邮件/发送头像/发送生日贺卡:m/p/t:")
        try:
            if choose == 'p':
                sendmail_picture(user,pwd,tgt,liker1,'活动通知',spammsg,picture)
            elif choose == 'm':
                sendmail(user,pwd,tgt,liker1,'活动通知',spammsg)
            elif choose == 't':
                TimedTask(user,pwd,tgt,liker1,'生日通知',spam,fp,s_time)
                a += 1
                if a >= 1:
                    break
        except Exception as e:
            print(e)
        time.sleep(10)

if __name__ == '__main__':
    main()