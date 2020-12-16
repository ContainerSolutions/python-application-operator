#!/usr/bin/env bash

set -eux

ls /app
ls /data

gitRepo=$1
entrypoint=$2
gunicorn_workers=$3
app_port=$4

export DEBIAN_FRONTEND=noninteractive
apt update
apt -yq install git curl
cd /app || exit 1
git clone "${gitRepo}" code
cd code || exit 1
pip install -r requirements.txt
pip install gunicorn

bash /data/start-app.sh "${entrypoint}" "${gunicorn_workers}" "${app_port}"