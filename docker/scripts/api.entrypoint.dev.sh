#!/usr/bin/env bash

./starnavi_test/docker/scripts/wait-for-it.sh postgres:5432 -s -t 30 --

python starnavi_test/src/manage.py runserver 0.0.0.0:8000 || { echo 'runserver failed' ; exit 1; }
