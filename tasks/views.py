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

# --- VISTA PRINCIPAL (LÓGICA DE ACTIVACIÓN) ---
def home(request):
    try:
        # Buscamos perfiles que tengan el check de activo en el Admin
        perfiles_activos = DatosPersonales.objects.filter(activarparaqueseveaenfront=True)
        total_activos = perfiles_activos.count()
        
        # Preparamos el username si solo hay uno para ir directo
        primer_perfil = perfiles_activos.first()
        username_unico = primer_perfil.user.username if primer_perfil else ""

        contexto = {
            'perfiles_activos': perfiles_activos,
            'total_activos': total_activos,
            'username_unico': username_unico,
            'config': ConfiguracionVisible.objects.first(),
        }
    except Exception:
        # Si la tabla no existe o el campo está mal, evitamos el Error 500
        contexto = {
            'perfiles_activos': [],
            'total_activos': 0,
            'username_unico': "",
            'config': None,
        }
    
    return render(request, 'welcome.html', contexto)

# --- VISTAS DE AUTENTICACIÓN ---
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

# --- PERFIL CV PÚBLICO ---
def profile_cv(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    
    # Si el perfil existe pero no está activo, no dejamos entrar
    if perfil and not getattr(perfil, 'activarparaqueseveaenfront', False):
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

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

def garage_store(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    productos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    return render(request, 'garage.html', {'user_viewed': user_viewed, 'productos': productos})

def export_pdf(request, username):
    from django.http import HttpResponse
    return HttpResponse(f"Generando PDF para {username}...")