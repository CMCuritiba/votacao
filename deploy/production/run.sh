#!/usr/bin/env bash

cd /app || exit 1

mkdir -p /app/var/run
rm -f /app/var/run/*

service nginx restart

exec "$VIRTUAL_ENV/bin/gunicorn" config.wsgi -c deploy/production/gunicorn.conf.py  --env DJANGO_SETTINGS_MODULE=config.settings.production
