#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar estáticos (CSS/JS)
# La opción --clear es la clave: borra lo viejo y fuerza la copia nueva
python manage.py collectstatic --no-input --clear

# 3. Migraciones de base de datos
python manage.py makemigrations
python manage.py migrate
