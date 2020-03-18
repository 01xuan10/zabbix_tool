import send_mail
import zabbix_config
import client
import time


def background_monitoring(monitoring_sym_key, monitoring_tcp_client_socket):
    while True:
        select = {'select_table': "events"}
        # print(select)
        # print(type(select))
        client.send_monit_date(monitoring_sym_key, monitoring_tcp_client_socket, str(select))
        # 输出所有的主机id和主机的对应关系
        # host = query(building_query_statements("hosts", "hostid,host"))
        eventid = client.recv_monit_date(monitoring_sym_key, monitoring_tcp_client_socket)
        # time.sleep(2)
        eventid_first = eval(eventid)

        eventid_first_value = eventid_first[-1][0]

        limit = "eventid > %s" % eventid_first_value
        #
        while True:
            time.sleep(5)
            select = {'select_table': "events", 'select_where':limit}
            client.send_monit_date(monitoring_sym_key, monitoring_tcp_client_socket, str(select))
            str_datas = client.recv_monit_date(monitoring_sym_key, monitoring_tcp_client_socket)
            datas = eval(str_datas)
            # dates = query(create_query("events", select_where=limit))
            if len(datas) == 1:
                break

        subject = "zabbix_error"
        content = datas[0][8]
        send_mail.send_mail(zabbix_config.email, subject, content)
