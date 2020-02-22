#!/bin/bash
/usr/sbin/groupadd loonflow
/usr/sbin/useradd -g loonflow loonflow
touch /opt/loonflow.sock && touch /opt/loonflow.pid && touch /var/log/loonflow.log
python /opt/loonflow/manage.py migrate
uwsgi --ini /opt/loonflow/uwsgi.ini
tail -f /var/log/loonflow.log