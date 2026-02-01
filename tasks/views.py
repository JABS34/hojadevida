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
        return render(request, 'profile_cv.html', {'error': 'Perfil no configurado.', 'user_viewed': user_profile})
    
    config, _ = ConfiguracionVisible.objects.get_or_create(pk=1)
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
    
    context = {
        'perfil': datos, 
        'user_viewed': user_profile,
        'estudios': Educacion.objects.filter(perfil=datos),
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'show_sobre_mi': request.GET.get('sobre_mi') == 'true',
        'show_lenguajes': request.GET.get('lenguajes') == 'true',
        'show_habilidades': request.GET.get('habilidades') == 'true',
        'show_experiencia': request.GET.get('experiencia') == 'true',
        'show_cursos': request.GET.get('cursos') == 'true',
        'show_reconocimientos': request.GET.get('reconocimientos') == 'true',
    }
    return render(request, 'pdf_template.html', context)

def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

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
    return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Credenciales incorrectas'})

def signout(request):
    logout(request)
    return redirect('home')

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
    if request.method == 'GET': return render(request, 'create_task.html', {'form': TaskForm()})
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')
    return render(request, 'create_task.html', {'form': form, 'error': 'Error'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET': return render(request, 'task_detail.html', {'task': task, 'form': TaskForm(instance=task)})
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        return redirect('tasks')
    return render(request, 'task_detail.html', {'task': task, 'form': form})

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
