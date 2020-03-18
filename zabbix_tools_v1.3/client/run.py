from welcome_page import welcome
from data_query import *
from reset_zabbix_web_passwd import *
import client
from background_monitoring import *
import threading


def select_t1(sym_key, tcp_client_socket):
    while True:
        print("*" * 100)
        print("""
                                                                1  --->  后台监控  <--- 此项不可重复选择
                                                                2  --->  数据查询
                                                                3  --->  reset password
                                                                4  --->  exit
                            """)
        print("*" * 100)
        select_t2 = input("请输入你的选择：")
        if select_t2 == "1":
            print("此项不可重复选择")
        elif select_t2 == "2":
            data_query(sym_key, tcp_client_socket)
        elif select_t2 == "3":
            reset_zabbix_passwd(sym_key, tcp_client_socket)
        elif select_t2 == "4":
            client.close_socket(tcp_client_socket)
            break
        else:
            print("请输入正确的序号")


if __name__ == "__main__":
    welcome()
    monitoring_sym_key, monitoring_tcp_client_socket = client.connect_secert_server_socket()
    time.sleep(2)
    sym_key, tcp_client_socket = client.connect_secert_server_socket()

    # while True:
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
        t1 = threading.Thread(target=select_t1, args=(sym_key, tcp_client_socket))
        # background_monitoring(monitoring_sym_key, monitoring_tcp_client_socket)
        t2 = threading.Thread(target=background_monitoring, args=(monitoring_sym_key, monitoring_tcp_client_socket))
        t1.start()
        t2.start()

    elif select == "2":
        while True:
            data_query(sym_key, tcp_client_socket)
    elif select == "3":
        reset_zabbix_passwd(sym_key, tcp_client_socket)
    elif select == "4":
        client.close_socket(tcp_client_socket)
        # break
    else:
        print("请输入正确的序号")

