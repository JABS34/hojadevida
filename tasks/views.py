from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import (
    DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, Reconocimiento
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# --- INICIO ---
def home(request):
    # Busca al primer superusuario para mostrar su perfil por defecto
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

# --- EL CORAZÓN DE TU HOJA DE VIDA ---
def profile_cv(request, username):
    # Buscamos al usuario por su nombre de usuario en la URL
    user_profile = get_object_or_404(User, username=username)
    # Buscamos sus datos personales
    datos = get_object_or_404(DatosPersonales, user=user_profile)
    
    # Consultas para todas las secciones que alimentan tu CV
    context = {
        'perfil': datos,
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos), # Esto activa el botón de logros
        'user_viewed': user_profile,
    }
    return render(request, 'profile_cv.html', context)

# --- SECCIÓN VENTA DE GARAGE ---
def garage_store(request):
    # Filtra solo productos marcados como disponibles
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- DASHBOARD (Solo para que tú edites tus datos) ---
@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(
        user=request.user,
        defaults={
            'nombres': request.user.username, 
            'apellidos': "Actualizar", 
            'fechanacimiento': "1990-01-01", 
            'numerocedula': f"ID-{request.user.id}"
        }
    )

    if request.method == 'POST':
        perfil.nombres = request.POST.get('nombres')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.descripcionperfil = request.POST.get('descripcionperfil')
        perfil.direcciondomiciliaria = request.POST.get('direcciondomiciliaria')
        perfil.instagram = request.POST.get('instagram')
        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')
        perfil.save()

        # Agregar Habilidad rápida desde el dashboard
        if request.POST.get('hab_nombre'):
            Habilidad.objects.create(perfil=perfil, nombre=request.POST.get('hab_nombre'))

        return redirect('profile_cv', username=request.user.username)
        
    return render(request, 'dashboard.html', {'perfil': perfil})
