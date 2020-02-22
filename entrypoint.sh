#!/bin/bash
python /opt/loonflow/manage.py migrate
uwsgi --ini /opt/loonflow/uwsgi.ini
tail -f /var/log/loonflow.log