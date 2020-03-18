import server
from database import *
import welcome_page
import threading
import time
from monitoring_db import *


# def create_query_connect(tcp_server_socket):
#
#     sym_key, client_socket = server.connect_new_client(tcp_server_socket)
#     return sym_key, client_socket


def start_query(sym_key, client_socket):
    while True:
        select = server.recv_date(sym_key, client_socket)

        query_statement = building_query_statements(select)

        date_list = query(query_statement)

        server.send_date(sym_key, client_socket, str(date_list))

        print("sended")


def query_value(tcp_server_socket):
    sym_key, client_socket = server.connect_new_client(tcp_server_socket)
    # sym_key, client_socket, tcp_server_socket = query_value_bind()

    print("*" * 100)
    print("""
                                    1  --->  allow query
                                    2  --->  close now client connect
                                    3  --->  close server
    """)
    select_model = input("input you select:")
    if select_model == "1":
        start_query(sym_key, client_socket)
    elif select_model == "2":
        server.refuse_noe_connect(client_socket)
        sym_key, client_socket = server.connect_new_client(tcp_server_socket)
        print("wait connection")
        start_query(sym_key, client_socket)
    elif select_model == "3":
        server.refuse_all_connect(tcp_server_socket)
    else:
        print("input true select")


# def create_monitoring_connect(tcp_server_socket):
#     monitoring_sym_key, monitoring_client_socket = server.connect_new_client(tcp_server_socket)
#     return monitoring_sym_key, monitoring_client_socket


def start_monitoring_query(monitoring_sym_key, monitoring_client_socket):
    while True:
        select = server.recv_monit_date(monitoring_sym_key, monitoring_client_socket)

        query_statement = create_query(select)

        date_list = query_monit(query_statement)

        print(date_list)

        server.send_monit_date(monitoring_sym_key, monitoring_client_socket, str(date_list))

        print("sended")


def monitoring(tcp_server_socket):
    monitoring_sym_key, monitoring_client_socket = server.connect_new_client(tcp_server_socket)
    start_query(monitoring_sym_key, monitoring_client_socket)


welcome_page.welcome()
tcp_server_socket = server.create_secret_socket_listen()
t1 = threading.Thread(target=monitoring, args=(tcp_server_socket,))
t2 = threading.Thread(target=query_value, args=(tcp_server_socket,))
t1.start()
time.sleep(1)
t2.start()
