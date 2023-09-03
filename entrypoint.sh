#!/bin/sh

gunicorn django_configurations_wsgi:application -b 0.0.0.0:8080 --workers ${DJANGO_GUNICORN_WORKERS-1}
