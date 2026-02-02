#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones a PostgreSQL
# No usamos makemigrations en el servidor, solo migrate
python manage.py migrate

# Asegurar que la carpeta media local tenga permisos de escritura
mkdir -p media
chmod -R 755 media
