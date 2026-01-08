#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Crear carpetas para estáticos y fotos con permisos
mkdir -p staticfiles
mkdir -p media
chmod -R 755 media

python manage.py collectstatic --no-input
python manage.py migrate