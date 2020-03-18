import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.qq.com'
mail_user = '744319128'
mail_pass = 'tjrdjnhovcfhbdch'
mail_postfix = 'qq.com'


def send_mail(to_list, subject, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    # 增加 _charset="utf-8" ，使MIMEText使用utf-8编码，避免中文乱码
    msg = MIMEText(content, _charset="utf-8")
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        # print("send success")
        s.close()
        return True
    except Exception as e:
        print(str(e))
        # print ("send fail")
        return False


# if __name__ == "__main__":
#     # send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
#     send_mail()
