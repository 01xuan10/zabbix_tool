import pymysql
import zabbix_config


def create_query(select_table, username, passwd):
    query_statements = "UPDATE %s SET PASSWD = '%s' WHERE alias = '%s'" % (select_table, passwd, username)

    return query_statements

def update_value(query):
    conn = pymysql.connect(zabbix_config.db_host, zabbix_config.db_user, zabbix_config.db_pass, db = "zabbix", port = int(zabbix_config.db_port))

    cursor = conn.cursor()

    date = cursor.execute(query)

    conn.commit()

    cursor.close()

    conn.close()

    return date