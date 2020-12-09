#!/usr/bin/env bash

set -eux

ls /app
ls /data

echo "Hello world!"
export DEBIAN_FRONTEND=noninteractive
apt update
apt -yq install git curl
cd /app || exit 1
git clone https://github.com/kirek007/python-hello-web.git code
cd code || exit 1
pip install -r requirements.txt
pip install gunicorn
cat > wsgi.py <<EOF
from app import app

if __name__ == "__main__":
    app.run()
EOF

bash /data/start-app.sh