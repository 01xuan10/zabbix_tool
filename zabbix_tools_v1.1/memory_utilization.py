from send_mail import send_mail


receiver = input("请输入接收邮件的邮箱：")
send_mail(receiver, "test", "test")