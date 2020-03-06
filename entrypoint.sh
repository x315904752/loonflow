#!/bin/bash
touch /opt/loonflow.sock && touch /opt/loonflow.pid && touch /var/log/loonflow.log
python /opt/loonflow/manage.py migrate
uwsgi --ini /opt/loonflow/uwsgi.ini
python /opt/loonflow/init_mysql.py
cd /opt/loonflow
nohup celery -A tasks worker -l info -Q loonflow &
tail -f /var/log/loonflow.log