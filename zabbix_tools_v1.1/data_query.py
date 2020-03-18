from database import *
from create_value_xls import data_write
import datetime
from send_value import send_value
import os
import zabbix_config
import count_time


def data_query():
    # 输出所有的主机id和主机的对应关系
    host = query(building_query_statements("hosts", "hostid,host"))
    for i in range(len(host)):
        print("%s : %s" % (host[i][0], host[i][1]))

    # 根据输入的主机id查询该主机对应的所有事件详情和事件id
    middle_host_id = input("请输入你想要查询的主机id：")
    host_id = "hostid" + "=" + middle_host_id
    items = query(building_query_statements("items", "itemid,name,delay", host_id))
    # print(building_query_statements("items", "itemid,name,delay", host_id))
    for i in range(len(items)):
        print("%s \t %s \t %s \t %s" % (i, items[i][0], items[i][1], items[i][2]))

    # 根据输入的事件id查询历史数据
    middle_item_id = input("请输入你想查询的事件id：")
    item_id = "itemid" + "=" + middle_item_id
    try:
        middle_value_type = query(building_query_statements("items", "itemid,name,delay,value_type", item_id))
        value_type = middle_value_type[0][3]

        if value_type == 0:
            select_table = "history"
        elif value_type == 1:
            select_table = "history_str"
        elif value_type == 2:
            select_table = "history_log"
        elif value_type == 3:
            select_table = "history_uint"
        elif value_type == 4:
            select_table = "history_text"

        print("""
        请选择你想查询的时间段：
        1  ---> 过去1小时
        2  ---> 过去2小时
        3  ---> 今天开始到现在
        4  ---> 全部数据
        """)
        what_time = input("请输入你的选择")

        if what_time == "1":
            a, b = count_time.count_lost_n_hour(1)
            value = query(building_query_statements(select_table, "itemid,clock,value,ns", item_id, limit_one= a, limit_two= b))
        elif what_time == "2":
            a, b = count_time.count_lost_n_hour(2)
            value = query(building_query_statements(select_table, "itemid,clock,value,ns", item_id, limit_one= a, limit_two= b))
        elif what_time == "3":
            a, b = count_time.count_today_start_time()
            value = query(building_query_statements(select_table, "itemid,clock,value,ns", item_id, limit_one= a, limit_two= b))
        elif what_time == "4":
            value = query(building_query_statements(select_table, "itemid,clock,value,ns", item_id))
        else:
            print("臣妾做不到")

        # print(building_query_statements(select_table, "itemid,clock,value,ns", item_id, start_time, end_time))
        if len(value) != 0:
            print("你正在查看的数据是来自%s" % middle_value_type[0][1])
            for i in range(len(value)):
                print("%s : %s" % (datetime.datetime.fromtimestamp(value[i][1]), value[i][2]))
        elif len(value) == 0:
            print("该事件在选定时间段不存在数据")
            return

        print("""是否将数据发送到邮箱？
        1  -->  send
        2  -->  do not send""")
        select_send_value = input("请输入选择：")

        if select_send_value == "1":
            current_path = os.path.split(os.path.realpath(__file__))[0]
            file = current_path + "\\" + middle_value_type[0][1] + ".xls"  # 附件路径
            data_write(file, value)
            filename = middle_value_type[0][1] + ".xls"
            contents = middle_value_type[0][1] + "---" + "start:" + str(datetime.datetime.fromtimestamp(a)) + "---" + "to:" + str(datetime.datetime.fromtimestamp(b)) + "---" + "value "
            send_to = zabbix_config.email
            send_value(filename, send_to, contents)
        elif select_send_value == 2:
            pass
        elif select_send_value != 1 or select_send_value != 2:
            print("输入有误")
        try:
            if os.path.exists(file):
                os.remove(file)
                print("原始文件删除成功")
        except UnboundLocalError as f:
            pass
    except IndexError as e:
        print("wrong hostid or itemid")