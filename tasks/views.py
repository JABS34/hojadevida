from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import (
    DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, Reconocimiento, ProductoGarage
)

# 1. La vista del PDF: Solo datos, sin lógica de administración
def export_pdf(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    # Convierte los parámetros de la URL en booleanos para los {% if %}
    def to_bool(val):
        return str(val).lower() == 'true'

    context = {
        'perfil': datos, 
        'user_viewed': user_profile,
        'estudios': Educacion.objects.filter(perfil=datos),
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        
        # Filtros de visibilidad
        'show_sobre_mi': to_bool(request.GET.get('sobre_mi', 'true')),
        'show_habilidades': to_bool(request.GET.get('habilidades', 'true')),
        'show_experiencia': to_bool(request.GET.get('experiencia', 'true')),
        'show_formacion': to_bool(request.GET.get('formacion', 'true')),
        'show_cursos': to_bool(request.GET.get('cursos', 'true')),
        'show_reconocimientos': to_bool(request.GET.get('reconocimientos', 'true')),
    }
    return render(request, 'pdf_template.html', context)

# 2. Vista del Garage (Para que Render no de error)
def garage_store(request, username):
    user_profile = get_object_or_404(User, username=username)
    productos = ProductoGarage.objects.filter(disponible=True)
    return render(request, 'garage_store.html', {'productos': productos, 'user_viewed': user_profile})

# 3. Vista de Tareas (Para que Render no de error si la ruta existe en urls.py)
def tasks(request):
    return render(request, 'tasks.html')

# 4. Vista de Perfil Público
def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    context = {
        'perfil': datos,
        'user_viewed': user_profile,
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
    }
    return render(request, 'profile_cv.html', context)

# ... (Manten tus funciones de signup/signin/home abajo si las usas)