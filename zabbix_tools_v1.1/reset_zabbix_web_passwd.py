import getpass
import hashlib
from update_value_databases import *


def get_new_passwd():
    passwd1 = getpass.getpass("input new password:")
    passwd2 = getpass.getpass("input new password again:")
    if passwd1 == passwd2:
        global passwd
        passwd = passwd1
        # return
    elif passwd1 != passwd2:
        print("passwd1 != passwd2 please check it")
        get_new_passwd()
    return passwd




def reset_zabbix_passwd():
    print("reset zabbix web password")
    username = input("input you want reset username:")
    passwd = get_new_passwd()
    # print(type(passwd))
    # md5_passwd = hashlib.md5(b'passwd')
    md5_passwd = hashlib.md5(passwd.encode('utf8')).hexdigest()
    date = update_value(create_query("users", username=username, passwd=md5_passwd))
    if date == 1:
        print("password changed successfully")
    elif date == 0:
        print("please check username")