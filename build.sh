#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar las migraciones a la base de datos (PostgreSQL o SQLite)
# Esto asegura que las tablas se creen sin borrar los datos existentes
python manage.py migrate

# Crear carpeta de fotos para evitar errores de ruta
mkdir -p media
chmod -R 755 media
