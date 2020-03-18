from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from email.mime.text import MIMEText
import os


def send_value(filename, middle_receiver, middle_contents):
    # 邮件发送
    smtp = "smtp.qq.com"
    sender = '744319128@qq.com'
    receiver = middle_receiver
    # 授权密码 可自行百度设置方法 是一串英文字符
    pwd = 'tjrdjnhovcfhbdch'
    title = "zabbix_value"
    contents = middle_contents
    try:
        msg = MIMEMultipart()
        msg['Subject'] = title  # 主题
        msg['From'] = sender  # 发件人
        msg['To'] = receiver
        part_text = MIMEText(contents)
        msg.attach(part_text)
        current_path = os.path.split(os.path.realpath(__file__))[0]
        file = current_path + "\\" + filename  # 附件路径
        part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=filename)  # 为附件命名
        msg.attach(part_attach1)  # 添加附件
        smtp = smtplib.SMTP(smtp, 25)
        smtp.login(sender, pwd)
        smtp.sendmail(sender, receiver, msg.as_string())
        print("success")
    except Exception as e:
        pass