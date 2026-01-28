from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, 
    Reconocimiento, ConfiguracionVisible
)

def home(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

@login_required
def dashboard(request):
    try:
        perfil, created = DatosPersonales.objects.get_or_create(
            user=request.user,
            defaults={
                'nombres': request.user.first_name or request.user.username,
                'apellidos': request.user.last_name or 'Completar',
                'fechanacimiento': '1990-01-01',
                'numerocedula': f"TEMP-{request.user.id}"
            }
        )
    except Exception:
        perfil = None
    return render(request, 'dashboard.html', {'perfil': perfil})

def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    if not datos:
        return render(request, 'profile_cv.html', {
            'error': 'Este perfil profesional aún no ha sido configurado.',
            'user_viewed': user_profile
        })
    
    config, created = ConfiguracionVisible.objects.get_or_create(pk=1)
    
    context = {
        'perfil': datos, 
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos), 
        'habilidades': Habilidad.objects.filter(perfil=datos), 
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'user_viewed': user_profile,
        'config': config,
    }
    return render(request, 'profile_cv.html', context)

def export_pdf(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    # Obtener preferencias de la URL
    show_sobre_mi = request.GET.get('sobre_mi') == 'true'
    show_cursos = request.GET.get('cursos') == 'true'
    show_reconocimientos = request.GET.get('reconocimientos') == 'true'
    show_garage = request.GET.get('garage') == 'true'

    context = {
        'perfil': datos,
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos) if show_cursos else [],
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos) if show_reconocimientos else [],
        'productos': ProductoGarage.objects.filter(disponible=True) if show_garage else [],
        'show_sobre_mi': show_sobre_mi,
        'show_cursos': show_cursos,
        'show_reconocimientos': show_reconocimientos,
        'show_garage': show_garage,
        'user_viewed': user_profile,
    }
    return render(request, 'pdf_template.html', context)

def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- AUTENTICACIÓN Y TAREAS SE MANTIENEN IGUAL (Omitido por brevedad pero mantenlo en tu archivo) ---
# ... (signup, signin, signout, tasks, create_task, etc.)
