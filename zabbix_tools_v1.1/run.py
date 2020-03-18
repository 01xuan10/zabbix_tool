from welcome_page import welcome
from background_monitoring import *
from data_query import *
import threading
from reset_zabbix_web_passwd import *


# def select_t1():
#     while True:
#         print("*" * 100)
#         print("""
#                                                                 1  --->  后台监控  <--- 此项不可重复选择
#                                                                 2  --->  数据查询
#                                                                 3  --->  reset password
#                                                                 4  --->  exit
#                             """)
#         print("*" * 100)
#         select_t2 = input("请输入你的选择：")
#         if select_t2 == "1":
#             print("此项不可重复选择")
#         elif select_t2 == "2":
#             data_query()
#         elif select_t2 == "3":
#             reset_zabbix_passwd()
#         elif select_t2 == 4:
#             break
#         else:
#             print("请输入正确的序号")


if __name__ == "__main__":
    welcome()
    while True:
        print("*" * 100)
        print("""
                                            1  --->  后台监控
                                            2  --->  数据查询
                                            3  --->  reset zabbix web password
                                            4  --->  exit
        """)
        print("*" * 100)
        select = input("请输入你的选择：")
        if select == "1":
            background_monitoring()
            # t1 = threading.Thread(target=select_t1())
            # t2 = threading.Thread(target=background_monitoring())
            #
            # t1.start()
            # t2.start()

        elif select == "2":
            data_query()
        elif select == "3":
            reset_zabbix_passwd()
        elif select == "4":
            break
        else:
            print("请输入正确的序号")