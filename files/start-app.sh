#!/usr/bin/env bash

set +xeu

echo "Hello world!"

entrypoint=$1

cd /app/code || exit 1
gunicorn --bind 0.0.0.0:3000 entrypoint