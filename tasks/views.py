from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TaskForm
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, 
    Reconocimiento
)

# --- VISTAS DE TAREAS (CRUD COMPLETO) ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Completadas'})

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
        return render(request, 'create_task.html', {'form': form, 'error': 'Datos inválidos'})

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
        return render(request, 'task_detail.html', {'task': task, 'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return redirect('tasks')

# --- VISTA DEL PDF CON CONFIGURACIÓN DINÁMICA ---

def export_pdf(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
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
        # Captura de parámetros de los checkboxes
        'show_sobre_mi': to_bool(request.GET.get('sobre_mi', 'true')),
        'show_lenguajes': to_bool(request.GET.get('lenguajes', 'true')),
        'show_habilidades': to_bool(request.GET.get('habilidades', 'true')),
        'show_experiencia': to_bool(request.GET.get('experiencia', 'true')),
        'show_formacion': to_bool(request.GET.get('formacion', 'true')),
        'show_cursos': to_bool(request.GET.get('cursos', 'true')),
        'show_reconocimientos': to_bool(request.GET.get('reconocimientos', 'true')),
    }
    return render(request, 'pdf_template.html', context)

# --- VISTA DEL GARAGE ---

def garage_store(request, username):
    user_profile = get_object_or_404(User, username=username)
    productos = ProductoGarage.objects.filter(disponible=True)
    return render(request, 'garage.html', {
        'productos': productos,
        'user_viewed': user_profile
    })

# --- PERFIL Y DASHBOARD ---

def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
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

@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        perfil.nombres = request.POST.get('nombres')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.descripcionperfil = request.POST.get('descripcionperfil')
        perfil.direcciondomiciliaria = request.POST.get('direcciondomiciliaria')
        if 'foto' in request.FILES: perfil.foto = request.FILES['foto']
        perfil.save()
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'perfil': perfil})

# --- AUTENTICACIÓN ---

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'welcome.html')