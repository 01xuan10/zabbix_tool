import pymysql
import zabbix_config


def create_query(select_table, select_columns="", select_where="", limit_one=0, limit_two=0, username = "", passwd = ""):
    # select_table =
    # select_itemid =
    # print("start_tims = %s" % start_time)
    # print(type(start_time))
    if select_columns == "" and select_table != "" and select_where == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statement = "SELECT * FROM %s" % (select_table)
    elif select_columns != "" and select_table != "" and select_where == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statement = "SELECT %s FROM %s" % (select_columns, select_table)
    elif select_where != "" and select_table != "" and select_columns == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statement = "SELECT * FROM %s WHERE %s" % (select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and  limit_one == limit_two and username == "" and passwd == "":
        query_statement = "SELECT %s FROM %s WHERE %s" % (select_columns, select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and limit_one != limit_two and username == "" and passwd == "":
        query_statement = "SELECT %s FROM %s WHERE %s and %s <= clock and %s >= clock " % (select_columns, select_table, select_where, limit_one, limit_two)
    elif select_table != "" and username != "" and passwd != "":
        query_statement = "UPDATE %s SET PASSWD = '%s' WHERE alias = '%s'" % (select_table, passwd, username)
    return query_statement


def query(create_query):
    while True:
        try:
            conn = pymysql.connect(zabbix_config.db_host, zabbix_config.db_user, zabbix_config.db_pass,
                                   port=int(zabbix_config.db_port), db="zabbix")

            cursor = conn.cursor()

            cursor.execute(create_query)

            date = cursor.fetchall()

            if date:
                print("host is up")
                break

        except pymysql.err.OperationalError as e:
            print("wait zabbix hosts up")
    return date
