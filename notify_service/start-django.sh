#!/bin/sh

wait_database()
{
  HOST=$1
  PORT=$2
  TYPE=$3

  echo "Waiting for $TYPE..."

  while ! nc -z $HOST $PORT; do
    sleep 0.1
  done

  echo "$TYPE started"
}

if [ ${DB_TYPE} = "postgres" ]
  then
    wait_database $DB_HOST $DB_PORT $DB_TYPE
fi

chown www-data:www-data /var/log
python manage.py migrate
python manage.py createsuperuser_if_not_exists --user=admin --password=admin
python manage.py collectstatic --no-input

gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 3  --bind 0.0.0.0:8000
