#!/usr/bin/env bash

set -e
echo "Waiting for postgres..."
while !</dev/tcp/postgres/5432;
  do sleep 1;
  done;
echo "Postgres is ready!"



chown www-data:www-data /var/log
python manage.py migrate
python manage.py collectstatic --no-input

gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 3  --bind 0.0.0.0:8000
