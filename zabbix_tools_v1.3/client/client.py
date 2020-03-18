import socket
import rsa
import hashlib
import pickle
from cryptography.fernet import Fernet
import zabbix_config
# import time


def connect_secert_server_socket():
    #     create socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     connect socket
    # server_ip = input("input you want connect server")
    # server_port = int(input("input server port"))
    server_addr = (zabbix_config.zabbix_tools_server_ip, zabbix_config.zabbix_tools_server_port)
    tcp_client_socket.connect(server_addr)

    # create publickey and privatekey
    asy_key = rsa.newkeys(2048)
    public_key = asy_key[0]
    private_key = asy_key[1]
    # print(public_key)
    # print(private_key)

    # send public_key to server
    send_public_key = pickle.dumps(public_key)
    send_public_key_sha256 = hashlib.sha256(send_public_key).hexdigest()
    # print(send_public_key)
    # print(send_public_key_sha256)
    tcp_client_socket.send(pickle.dumps((send_public_key,send_public_key_sha256)))
    print("*" * 100)
    print("""                       Asymmetric crypto public key has been sent""")
    print("*" * 100)

    # Accept and decrypt the key passed by the server
    sym_key, sys_key_md5 = pickle.loads(tcp_client_socket.recv(1024))
    if hashlib.md5(sym_key).hexdigest() != sys_key_md5:
        print("key is not safe")
        return
    else:
        use_sym_key = pickle.loads(rsa.decrypt(sym_key, private_key))
        print("*" * 100)
        print("""                       Symmetric encryption key accepted""")
        print("*" * 100)
        print(use_sym_key)
    return use_sym_key, tcp_client_socket


def recv_date(sym_key, tcp_client_socket):

    f = Fernet(sym_key)
    end = '='
    en_recv_date = b''
    en_recv_date_str = ''
    # date = ''
    while end not in en_recv_date_str:
    # time.sleep(2)
    #     global en_recv_date
    #     date = tcp_client_socket.recv(1048576)
        date = tcp_client_socket.recv(1024)
        en_recv_date = en_recv_date + date
        en_recv_date_str = str(en_recv_date)
    # print(en_recv_date_str)
        # return total_en_recv_date
    #     if '=' in en_recv_date:
    #         total_en_recv_date.append(date[:date.find('=')])
    #         break
    #     total_en_recv_date.append(date)
    # return ''.join(total_en_recv_date)
    # print(total_en_recv_date)
    # return en_recv_date
    # print(en_recv_date)
    # print(en_recv_date)
    # en_recv_date = en_recv_date - b'='
    # print(en_recv_date)
    # print(type(en_recv_date))
    recv_dates = f.decrypt(en_recv_date).decode()
    return recv_dates


def recv_monit_date(sym_key, tcp_client_socket):
    f = Fernet(sym_key)
    end = '='
    en_recv_date = b''
    en_recv_date_str = ''
    while end not in en_recv_date_str:

        date = tcp_client_socket.recv(1024)
        en_recv_date = en_recv_date + date
        en_recv_date_str = str(en_recv_date)
    recv_dates = f.decrypt(en_recv_date).decode()
    return recv_dates


def send_date(sym_key, tcp_client_socket, send_date):
    f = Fernet(sym_key)
    en_send_date = f.encrypt(send_date.encode())
    tcp_client_socket.send(en_send_date)


def send_monit_date(sym_key, tcp_client_socket, send_date):
    f = Fernet(sym_key)
    en_send_date = f.encrypt(send_date.encode())
    tcp_client_socket.send(en_send_date)



def close_socket(tcp_client_socket):
    tcp_client_socket.close()
