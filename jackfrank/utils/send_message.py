import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header

#发送信息到QQ邮箱
def send_msg(text):
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