#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Esto creará la tabla que falta en PostgreSQL
python manage.py migrate --noinput

mkdir -p media
chmod -R 755 media
