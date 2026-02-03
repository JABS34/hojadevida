from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales, ConfiguracionVisible
)

def home(request):
    # Filtramos solo los perfiles activos
    perfiles_activos = DatosPersonales.objects.filter(activarparaqueseveaenfront=True)
    total_activos = perfiles_activos.count()
    
    # Intentamos obtener el primer perfil activo para el caso de redirección única
    primer_perfil = perfiles_activos.first()
    username_unico = primer_perfil.user.username if primer_perfil else ""

    contexto = {
        'perfiles_activos': perfiles_activos,
        'total_activos': total_activos,
        'username_unico': username_unico,
        'config': ConfiguracionVisible.objects.first(),
    }
    return render(request, 'welcome.html', contexto)

# --- El resto de tus vistas se mantienen igual ---
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

def profile_cv(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    if perfil and not perfil.activarparaqueseveaenfront:
        return redirect('home')
    contexto = {
        'user_viewed': user_viewed,
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else [],
        'cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else [],
        'reconocimientos': Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else [],
        'productos_academicos': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else [],
        'productos_laborales': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else [],
        'config': ConfiguracionVisible.objects.first(),
    }
    return render(request, 'profile_cv.html', contexto)

def garage_store(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    productos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    return render(request, 'garage.html', {'user_viewed': user_viewed, 'productos': productos})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        try:
            form = UserCreationForm(request.POST)
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        except ValueError:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Datos inválidos.'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos.'})
        else:
            login(request, user)
            return redirect('dashboard')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def export_pdf(request, username):
    from django.http import HttpResponse
    return HttpResponse(f"Generando PDF para {username}...")