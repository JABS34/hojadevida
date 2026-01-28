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
    Certificado, Educacion, Lenguaje, ProductoGarage, Reconocimiento
)

def home(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

@login_required
def dashboard(request):
    # Obtiene o crea el perfil automáticamente al entrar para evitar errores
    perfil, created = DatosPersonales.objects.get_or_create(
        user=request.user,
        defaults={
            'nombres': request.user.first_name or request.user.username,
            'apellidos': request.user.last_name or '',
            'fechanacimiento': '1990-01-01',
            'numerocedula': request.user.id # Valor temporal para evitar errores de integridad
        }
    )
    return render(request, 'dashboard.html', {'perfil': perfil})

def profile_cv(request, username):
    # Buscamos al usuario por su nombre de usuario
    user_profile = get_object_or_404(User, username=username)
    
    # IMPORTANTE: Cambiamos get_object_or_404 por filter().first() para manejar el error 500
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    if not datos:
        # Si el usuario no tiene perfil creado, enviamos un mensaje en lugar de romper la web
        return render(request, 'profile_cv.html', {
            'error': 'Este perfil profesional aún no ha sido configurado.',
            'user_viewed': user_profile
        })
    
    context = {
        'perfil': datos, 
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos), 
        'habilidades': Habilidad.objects.filter(perfil=datos), 
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'user_viewed': user_profile,
    }
    return render(request, 'profile_cv.html', context)

def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- AUTENTICACIÓN ---

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'error': 'El usuario ya existe'})
        return render(request, 'signup.html', {'form': form, 'error': 'Datos inválidos'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos'})
        login(request, user)
        return redirect('dashboard')

def signout(request):
    logout(request)
    return redirect('home')

# --- GESTIÓN DE TAREAS ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas completadas'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm()})
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        return render(request, 'create_task.html', {'form': form, 'error': 'Datos incorrectos'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error al actualizar'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('tasks')
