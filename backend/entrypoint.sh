#!/bin/sh
python manage.py migrate
python manage.py add_testing_data
python manage.py runserver 0.0.0.0:${APP_PORT:-80}
