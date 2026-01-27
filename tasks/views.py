from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, Reconocimiento
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# --- HOJA DE VIDA ---
def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = get_object_or_404(DatosPersonales, user=user_profile)
    
    context = {
        'perfil': datos, 
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos), 
        'habilidades': Habilidad.objects.filter(perfil=datos), 
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos), # Activa el botón
        'user_viewed': user_profile,
    }
    return render(request, 'profile_cv.html', context)

# --- VENTA DE GARAGE ---
def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- AUTENTICACIÓN (Obligatorio para que no falle el Build) ---
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html', {'form': form, 'error': 'Datos inválidos'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user:
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Error de acceso'})

def signout(request):
    logout(request)
    return redirect('home')

def home(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

@login_required
def dashboard(request):
    perfil, _ = DatosPersonales.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'perfil': perfil})
