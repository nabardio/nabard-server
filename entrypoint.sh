#!/bin/bash
./manage.py migrate --noinput
if [[ "$*" == "django" ]]
then
    gunicorn --workers 4 --worker-class gevent --reuse-port --chdir /app --bind 0.0.0.0:8000 nabard.wsgi:application
elif [[ "$*" == "celery" ]]
then
    celery -A nabard -l info worker
else
    echo '"$*" is not a suitable input. Only "django" and "celery" are supported now.';
    exit 1;
fi
