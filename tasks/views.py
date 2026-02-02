from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales
)
from .forms import TaskForm, DatosPersonalesForm, VentaGarageForm # Importamos los nuevos forms

# --- VISTA PERFIL CV (Muestra TODOS los atributos SQL) ---
def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    context = {
        'perfil': datos, 
        # Orden cronológico según requerimiento
        'experiencias': ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=datos, 
            activarparaqueseveaenfront=True
        ).order_by('-fechainiciogestion'), 
        
        'cursos': CursosRealizados.objects.filter(
            idperfilconqueestaactivo=datos, 
            activarparaqueseveaenfront=True
        ),
        
        'reconocimientos': Reconocimiento.objects.filter(
            idperfilconqueestaactivo=datos, 
            activarparaqueseveaenfront=True
        ),
        
        'productos_academicos': ProductosAcademicos.objects.filter(
            idperfilconqueestaactivo=datos, 
            activarparaqueseveaenfront=True
        ),

        # Se agrega Productos Laborales que faltaba en tu vista anterior
        'productos_laborales': ProductosLaborales.objects.filter(
            idperfilconqueestaactivo=datos, 
            activarparaqueseveaenfront=True
        ),
        'user_viewed': user_profile, 
    }
    return render(request, 'profile_cv.html', context)

# --- VISTA GARAGE (Cumple con numeric 5,2 y estado producto) ---
def garage_store(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    productos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=datos, 
        activarparaqueseveaenfront=True
    )
    
    return render(request, 'garage.html', {
        'productos': productos,
        'user_viewed': user_profile
    })

# --- GESTIÓN DE TAREAS Y DASHBOARD ---
@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Usamos el Form para procesar todos los campos SQL de un solo golpe
        form = DatosPersonalesForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DatosPersonalesForm(instance=perfil)
        
    return render(request, 'dashboard.html', {'perfil': perfil, 'form': form})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Pendientes'})

# --- VISTAS DE AUTENTICACIÓN (Mantener según tu lógica original) ---
def home(request): 
    return render(request, 'welcome.html')

def signout(request):
    logout(request)
    return redirect('home')

# Agrega aquí tus funciones de signup y signin si necesitas editarlas