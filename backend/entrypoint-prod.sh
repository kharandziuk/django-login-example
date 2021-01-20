#!/bin/sh
python manage.py migrate
python manage.py add_testing_data
gunicorn -b 0.0.0.0:${APP_PORT:-80} -w 2 --max-requests=500 project.wsgi:application
