#!/usr/bin/env bash

set +xeu

echo "Hello world!"

entrypoint=$1
gunicorn_workers=$2
app_port=$3

cd /app/code || exit 1
gunicorn --bind 0.0.0.0:${app_port} --workers "${gunicorn_workers}" "${entrypoint}"