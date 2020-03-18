import socket
import pickle
import hashlib
from cryptography.fernet import Fernet
import rsa


def create_secret_socket_listen():
    # create socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind local information
    bind_local_port = 12345
    tcp_server_socket.bind(("", bind_local_port))
    local_addr = socket.gethostbyname("xuan.example.com")
    print("already bind %s : %d" % (local_addr, bind_local_port))
    # listen
    tcp_server_socket.listen(1024)
    print("wait connection")
    return tcp_server_socket


def connect_new_client(tcp_server_socket):
    # 接受客户端传递的公钥
    # 这里可以加一个哈希函数检验公钥的正确性！
    # 运用pickle进行反序列化
    client_socket, addr = tcp_server_socket.accept()
    print("和客户端{0}建立连接".format(addr))
    public_key, public_key_sha254 = pickle.loads(client_socket.recv(1024))
    if hashlib.sha256(public_key).hexdigest() != public_key_sha254:
        print("key is not safe")
        return
    else:
        use_public_key = pickle.loads(public_key)
        print("public is safe")

    # 下面是用公钥加密对称密钥并传递的过程
    # 产生用于对称加密的密钥
    sym_key = Fernet.generate_key()
    # 用pickle进行序列化用来进行网络传输
    # 对密钥进行hash保证其准确性
    en_sym_key = rsa.encrypt(pickle.dumps(sym_key), use_public_key)
    en_sym_key_md5 = hashlib.md5(en_sym_key).hexdigest()
    print("正在加密传送密钥")
    client_socket.send(pickle.dumps((en_sym_key, en_sym_key_md5)))
    print(sym_key)
    return sym_key, client_socket


def recv_date(sym_key, client_socket):
    # 初始化加密对象
    f = Fernet(sym_key)
    en_recv_date = client_socket.recv(1024)
    recv_date = f.decrypt(en_recv_date).decode()
    return recv_date


def recv_monit_date(sym_key, client_socket):
    # 初始化加密对象
    f = Fernet(sym_key)
    en_recv_date = client_socket.recv(1024)
    recv_date = f.decrypt(en_recv_date).decode()
    return recv_date


def send_date(sym_key, client_socket, send_date):
    # 初始化加密对象
    print(send_date)
    f = Fernet(sym_key)
    en_send_date = f.encrypt(send_date.encode())
    en_send_date = en_send_date + b'='
    client_socket.send(en_send_date)


def send_monit_date(sym_key, client_socket, send_date):
    # 初始化加密对象
    print(send_date)
    f = Fernet(sym_key)
    en_send_date = f.encrypt(send_date.encode())
    en_send_date = en_send_date + b'='
    client_socket.send(en_send_date)


def refuse_noe_connect(client_socket):
    client_socket.close()


def refuse_all_connect(tcp_server_socket):
    tcp_server_socket.close()




