#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# No ponemos migrate ni createsuperuser para que use lo que ya está en tu db.sqlite3
mkdir -p media
chmod -R 755 media
