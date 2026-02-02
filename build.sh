#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Archivos estáticos
python manage.py collectstatic --no-input

# 3. CREAR TABLAS FALTANTES (Esto arregla el error 'no such table')
# Django buscará en tu carpeta 'migrations' y creará lo que falte en db.sqlite3
python manage.py migrate --noinput

# 4. Limpieza de permisos
mkdir -p media
chmod -R 755 media
