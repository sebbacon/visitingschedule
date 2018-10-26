#!/usr/bin/env bash

cd /var/www/visitingschedule/

exec ../../venv/bin/gunicorn visitingschedule.wsgi -c ../deploy/gunicorn-visitingschedule.conf.py
