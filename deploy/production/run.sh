#!/usr/bin/env bash

cd /usr/share/webapps/votacao

mkdir -p /usr/share/webapps/votacao/var/run
rm -f /usr/share/webapps/votacao/var/run/*

exec /usr/share/envs/votacao/bin/gunicorn config.wsgi -c deploy/production/gunicorn.conf.py  --env DJANGO_SETTINGS_MODULE=config.settings.production
