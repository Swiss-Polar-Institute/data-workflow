#!/bin/bash

/code/wait-for-mysql.sh

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

mkdir -p /srv/logs
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

gunicorn DataWorkflow.wsgi:application \
        --bind 0.0.0.0:8086 \
        --workers 3 \
        --log-level=info \
        --log-file=/srv/logs/gunicorn.log \
        --access-logfile=/srv/logs/access.log
        "$@"
