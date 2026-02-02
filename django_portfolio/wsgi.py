import os
from django.core.wsgi import get_wsgi_application

# Asegúrate de que apunte a tu carpeta correcta 'django_portfolio'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_portfolio.settings')

application = get_wsgi_application()

# --- BLOQUE DE CREACIÓN DE SUPERUSUARIO ---
from django.contrib.auth import get_user_model

try:
    User = get_user_model()
    # Personaliza estos datos:
    username = 'jabs6393'
    email = 'admin@ejemplo.com'
    password = 'TuContraseñaSegura123' # <--- PON LA CLAVE QUE QUIERAS USAR

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"EXITO: Superusuario '{username}' creado.")
    else:
        print(f"AVISO: El usuario '{username}' ya existe.")
except Exception as e:
    # Esto evita que el servidor falle si la base de datos no está lista
    print(f"LOG: No se pudo crear el usuario (posiblemente falta migrate): {e}")
