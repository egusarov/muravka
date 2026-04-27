#!/bin/bash
set -e

echo "[1/6] Pull latest code..."
cd /home/ubuntu/apps/muravka

git pull origin main

echo "[2/6] Install dependencies..."
/home/ubuntu/apps/muravka/venv/bin/python -m pip install -r requirements.txt

echo "[3/6] Run migrations..."
/home/ubuntu/apps/muravka/venv/bin/python manage.py migrate --noinput

echo "[4/6] Collect static..."
/home/ubuntu/apps/muravka/venv/bin/python manage.py collectstatic --noinput

echo "[5/6] Restart service..."
sudo systemctl restart muravka

echo "[6/6] Deploy completed successfully"