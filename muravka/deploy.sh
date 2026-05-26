#!/bin/bash
set -e

echo "[1/7] Pull latest code..."
cd /home/ubuntu/apps/muravka

git pull origin main

echo "[2/7] Install dependencies..."
/home/ubuntu/apps/muravka/venv/bin/python -m pip install -r requirements.txt

echo "[3/7] Run migrations..."
/home/ubuntu/apps/muravka/venv/bin/python manage.py migrate --noinput

echo "[4/7] Generate sitemap..."
/home/ubuntu/apps/muravka/venv/bin/python manage.py generate_sitemap || {
  echo "SITEMAP GENERATION FAILED"
  exit 1
}

echo "[5/7] Collect static..."
/home/ubuntu/apps/muravka/venv/bin/python manage.py collectstatic --noinput

echo "[6/7] Restart service..."
sudo systemctl restart muravka

echo "[7/7] Deploy completed successfully"