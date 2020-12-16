#!/usr/bin/env bash

set -eux

ls /app
ls /data

gitRepo=$1
packageName=$2
appName=$3

export DEBIAN_FRONTEND=noninteractive
apt update
apt -yq install git curl
cd /app || exit 1
git clone "${gitRepo}" code
cd code || exit 1
pip install -r requirements.txt
pip install gunicorn
cat > wsgi.py <<EOF
from ${packageName} import ${appName}

if __name__ == "__main__":
    ${appName}.run()
EOF

bash /data/start-app.sh "${appName}"