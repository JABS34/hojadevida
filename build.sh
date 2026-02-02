#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones a PostgreSQL
python manage.py migrate

# Asegurar que la carpeta media local tenga permisos
mkdir -p media
chmod -R 755 media
