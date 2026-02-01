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

# ... (otras funciones: home, dashboard, profile_cv se mantienen igual) ...

def export_pdf(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    # Captura de parámetros para visibilidad
    context = {
        'perfil': datos, 
        'user_viewed': user_profile,
        'estudios': Educacion.objects.filter(perfil=datos),
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        # Flags de visibilidad (vienen del modal de exportación)
        'show_sobre_mi': request.GET.get('sobre_mi') == 'true',
        'show_lenguajes': request.GET.get('lenguajes') == 'true',
        'show_habilidades': request.GET.get('habilidades') == 'true',
        'show_experiencia': request.GET.get('experiencia') == 'true',
        'show_cursos': request.GET.get('cursos') == 'true',
        'show_reconocimientos': request.GET.get('reconocimientos') == 'true',
    }
    return render(request, 'pdf_template.html', context)

# ... (resto de funciones de tareas y auth se mantienen igual) ...
