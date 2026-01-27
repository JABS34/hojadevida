from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TaskForm
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, Reconocimiento
)

# --- 1. VISTAS DE NAVEGACIÓN Y PERFIL ---

def home(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

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
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'user_viewed': user_profile,
    }
    return render(request, 'profile_cv.html', context)

@login_required
def dashboard(request):
    perfil, _ = DatosPersonales.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        perfil.nombres = request.POST.get('nombres')
        perfil.save()
        return redirect('profile_cv', username=request.user.username)
    return render(request, 'dashboard.html', {'perfil': perfil})

# --- 2. GESTIÓN DE TAREAS (Aquí están las que pedía el error) ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Completadas'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, "create_task.html", {'form': TaskForm()})
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')
    return render(request, "create_task.html", {'form': form, 'error': 'Datos incorrectos'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
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

# --- 3. VENTA DE GARAGE ---

def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- 4. AUTENTICACIÓN ---

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user:
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos'})

def signout(request):
    logout(request)
    return redirect('home')
