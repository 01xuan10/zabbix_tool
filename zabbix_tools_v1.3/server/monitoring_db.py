import pymysql
import zabbix_config
import ast


def create_query(select):
    select_dict = ast.literal_eval(select)
    print(select_dict)

    select_table = ""
    select_columns = ""
    select_where = ""
    limit_one = 0
    limit_two = 0
    username = ""
    passwd = ""
    selects = []
    for key in select_dict:
        selects.append(key)
    if 'select_table' in selects:
        select_table = select_dict['select_table']
    if 'select_columns' in selects:
        select_columns = select_dict['select_columns']
    if 'select_where' in selects:
        select_where = select_dict['select_where']
    if 'limit_one' in selects:
        limit_one = select_dict['limit_one']
    if 'limit_two' in selects:
        limit_two = select_dict['limit_two']
    if 'username' in selects:
        username = select_dict['username']
    if 'passwd' in selects:
        passwd = select_dict['passwd']
    # select_table =
    # select_itemid =
    # print("start_tims = %s" % start_time)
    # print(type(start_time))

    if select_columns == "" and select_table != "" and select_where == "" and limit_one == limit_two:
        query_statements = "SELECT * FROM %s" % (select_table)
    elif select_columns != "" and select_table != "" and select_where == "" and limit_one == limit_two:
        query_statements = "SELECT %s FROM %s" % (select_columns, select_table)
    elif select_where != "" and select_table != "" and select_columns == "" and limit_one == limit_two:
        query_statements = "SELECT * FROM %s WHERE %s" % (select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and  limit_one == limit_two:
        query_statements = "SELECT %s FROM %s WHERE %s" % (select_columns, select_table, select_where)
    elif select_columns != "" and select_where != "" and select_table != "" and limit_one != limit_two:
        query_statements = "SELECT %s FROM %s WHERE %s and %s <= clock and %s >= clock " % (select_columns, select_table, select_where, limit_one, limit_two)

    # query(query_statements)
    # print(query_statements)
    return query_statements


def query_monit(create_query):
    while True:
            conn = pymysql.connect(zabbix_config.db_host, zabbix_config.db_user, zabbix_config.db_pass,
                                   port=int(zabbix_config.db_port), db="zabbix")

            cursor = conn.cursor()

            cursor.execute(create_query)

            date = cursor.fetchall()

            if date:
                print("host is up")
                break
    return date
