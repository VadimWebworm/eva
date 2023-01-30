#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Uncomment to clear all previous data
# python manage.py flush --no-input

python manage.py migrate
python manage.py loaddata fixtures/data.json

exec "$@"
