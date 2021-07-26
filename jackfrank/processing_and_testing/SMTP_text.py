from smtplib import SMTP
from poplib import POP3
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header

def send_msg1():
    text = 'hhhhhhhh'

    print('***************SMPT发送邮件和POP3收邮件************')

    SMTPSVR='smtp.sina.com' #smtp发送协议
    POP3SVR='pop3.sina.com' #pop3接收协议
    seder='w1013173649@sina.com' #发件箱
    password='w1414213562195' #发件箱密码
    recips=['1013173649@qq.com'] #收件人


    origmsg='''\    #发送信息：发件人，收件人发送内容
        From:%(who)s
        To:%(who)s
        Subject:first test
        
        Hello World!
        %(text)s
        '''% {'who':seder,'text':text}

    #使用SMTP完成邮件的发送
    sendSvr=SMTP(SMTPSVR) #创建一个smtp发送对象
    sendSvr.login(seder,password) #登录操作
    errs=sendSvr.sendmail(seder,recips,origmsg.encode('utf-8')) #参数：发件人，收件人，邮件整体（消息头和消息体的字符串表示）
    sendSvr.quit()
    assert len(errs)==0,errs #,assert返回为假就会触发异常
    print('smtp发送邮件完成')
    sleep(1)

    #使用pop3完成邮件的获取
    recvSvr=POP3(POP3SVR) #创建一个pop3接收对象
    recvSvr.user(seder) #设置用记名
    recvSvr.pass_(password)
    emailist=recvSvr.stat() #获取邮件列表
    rsp,msg,siz=recvSvr.retr(emailist[0]) #下载第一个邮件
    print(msg) #查看返回所有信息
    sep = msg.index(b'')  #查找列表中""空白元素，空白元素后面为邮件正文
    recvBody = msg[sep+1:]  #根据空白元素定位获取邮件正文
    print('pop3接收完成')

def send_msg2(text):
    user = 'w1013173649@sina.com'
    pwd = 'w1414213562195'
    to = ['1013173649@qq.com']
    msg = MIMEMultipart()
    msg['Subject'] = Header('我的主题...', 'utf-8')
    msg['From'] = Header(user)

    content1 = MIMEText(text, 'plain', 'utf-8')
    msg.attach(content1)

    s = smtplib.SMTP('smtp.sina.com')
    s.set_debuglevel(1)  # 调试使用
    s.starttls()  # 建议使用
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    s.close()


# send_msg1()


send_msg2('hahahahahahahahah')