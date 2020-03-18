import pymysql
import zabbix_config


def building_query_statements(select_table, select_columns="", select_where="", limit_one=0, limit_two=0, username="", passwd=""):
    # select_table =
    # select_itemid =
    # print("start_tims = %s" % start_time)
    # print(type(start_time))
    if select_columns == "" and select_table != "" and select_where == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statements = "SELECT * FROM %s" % (select_table)
    elif select_columns != "" and select_table != "" and select_where == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statements = "SELECT %s FROM %s" % (select_columns, select_table)
    elif select_where != "" and select_table != "" and select_columns == "" and limit_one == limit_two and username == "" and passwd == "":
        query_statements = "SELECT * FROM %s WHERE %s" % (select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and  limit_one == limit_two and username == "" and passwd == "":
        query_statements = "SELECT %s FROM %s WHERE %s" % (select_columns, select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and limit_one != limit_two and username == "" and passwd == "":
        query_statements = "SELECT %s FROM %s WHERE %s and %s <= clock and %s >= clock " % (select_columns, select_table, select_where, limit_one, limit_two)
    elif username != "" and passwd != "":
        query_statements = "UPDATE %s SET PASSWD = '%s' WHERE alias = '%s'" % (select_table, passwd, username)

    # query(query_statements)
    # print(query_statements)
    return query_statements


def query(query_statements):
    # 打开数据库连接
    db = pymysql.connect(zabbix_config.db_host, zabbix_config.db_user, zabbix_config.db_pass, port=int(zabbix_config.db_port), db="zabbix", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("connect databases success")
    # print(cursor)
    # 使用execute方法执行SQL语句
    cursor.execute(query_statements)

    # 使用 fetchone() 方法获取一条数据
    date_list = []
    while True:
        date = cursor.fetchone()
        if date:
            date_list.append(date)
        else:
            break

    return date_list

    # 关闭数据库连接
    db.close()