from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, DatosPersonales, ExperienciaLaboral, Habilidad 
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# 1. PANTALLA DE BIENVENIDA (CON DISEÑO 3D)
def home(request):
    # Buscamos al primer superusuario (tú) para que el botón sepa a quién mostrar
    # Si no hay superusuario, usará el usuario logueado o None
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

# 2. PANEL DE CONTROL / GESTIÓN (SOLO PARA TI - ADMIN)
@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(
        user=request.user, 
        defaults={'nombres': request.user.username, 'fechanacimiento': '1990-01-01'}
    )
    
    if request.method == 'POST':
        perfil.nombres = request.POST.get('nombres')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.descripcionperfil = request.POST.get('descripcionperfil')
        perfil.nacionalidad = request.POST.get('nacionalidad')
        perfil.numerocedula = request.POST.get('numerocedula')
        perfil.direcciondomiciliaria = request.POST.get('direcciondomiciliaria')
        perfil.save()
        return redirect('profile_cv', username=request.user.username)
        
    return render(request, 'dashboard.html', {'perfil': perfil})

# 3. PERFIL INTERACTIVO / CV 3D
def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = get_object_or_404(DatosPersonales, user=user_profile)
    experiencias = ExperienciaLaboral.objects.filter(perfil=datos)
    habilidades = Habilidad.objects.filter(perfil=datos)
    
    return render(request, 'profile_cv.html', {
        'perfil': datos, 
        'experiencias': experiencias, 
        'habilidades': habilidades, 
        'user_viewed': user_profile
    })

# --- VISTAS DE AUTENTICACIÓN ---

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, "signup.html", {"form": UserCreationForm, "error": "Username already exists"})
        return render(request, "signup.html", {"form": UserCreationForm, "error": "Password do not match"})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error':'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('dashboard')

def signout(request):
    logout(request)
    return redirect('home')

# --- VISTAS DE TAREAS ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks, 'tipopagina':'Tareas Pendientes'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks':tasks,'tipopagina':'Tareas completadas'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,"create_task.html",{'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,"create_task.html",{'form': TaskForm, 'error': 'Ingrese tipos de datos correctos'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{'task':task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{'task':task, 'form': form, 'error':'Error updating tasks'})

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