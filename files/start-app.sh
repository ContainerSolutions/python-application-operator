#!/usr/bin/env bash

set +xeu

echo "Hello world!"

cd /app/code || exit 1
gunicorn --bind 0.0.0.0:3000 wsgi:app