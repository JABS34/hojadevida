#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# --- PASO CRÍTICO PARA SQLITE ---
# Si estamos en Render, nos aseguramos de que el directorio del disco exista
if [ "$RENDER" ]; then
  mkdir -p /data/media
fi

# Generar y aplicar migraciones
# Si el archivo no existe, touch lo crea para evitar el error 'unable to open database file'
if [ "$RENDER" ]; then
  touch /data/db.sqlite3
  chmod 666 /data/db.sqlite3
fi

python manage.py makemigrations
python manage.py migrate
