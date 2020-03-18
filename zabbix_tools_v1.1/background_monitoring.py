from monitoring_db import *
import send_mail
import zabbix_config


def background_monitoring():
    while True:
        eventid_first_value = query(create_query("events"))[-1][0]

        limit = "eventid > %s" % eventid_first_value

        while True:
            dates = query(create_query("events", select_where=limit))
            if len(dates) == 1:
                break

        subject = "zabbix_error"
        content = dates[0][8]
        send_mail.send_mail(zabbix_config.email, subject, content)
