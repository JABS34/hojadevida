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

# --- VISTAS PÚBLICAS ---

def home(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    return render(request, "welcome.html", {"admin_user": admin_user})

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

def garage_store(request):
    productos = ProductoGarage.objects.filter(disponible=True).order_by('-fecha_publicado')
    return render(request, 'garage.html', {'productos': productos})

# --- DASHBOARD (GESTIÓN DE PERFIL) ---

@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(
        user=request.user,
        defaults={'nombres': request.user.username, 'fechanacimiento': '1990-01-01', 'numerocedula': f"T-{request.user.id}"}
    )

    if request.method == 'POST':
        # Actualización de datos personales
        perfil.nombres = request.POST.get('nombres')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.instagram = request.POST.get('instagram')
        perfil.descripcionperfil = request.POST.get('descripcionperfil')
        if 'foto' in request.FILES: 
            perfil.foto = request.FILES['foto']
        perfil.save()

        # Gestión de Lenguajes
        seleccionados = request.POST.getlist('lenguajes')
        if seleccionados:
            Lenguaje.objects.filter(perfil=perfil).delete()
            for lang in seleccionados: 
                Lenguaje.objects.create(perfil=perfil, nombre=lang)

        # Agregar Educación
        edu_t = request.POST.get('edu_titulo')
        if edu_t: 
            Educacion.objects.create(
                perfil=perfil, 
                titulo=edu_t, 
                institucion=request.POST.get('edu_inst'), 
                fecha_graduacion=request.POST.get('edu_fecha') or timezone.now().date()
            )

        # Agregar Experiencia
        exp_p = request.POST.get('exp_puesto')
        if exp_p: 
            ExperienciaLaboral.objects.create(
                perfil=perfil, 
                puesto=exp_p, 
                empresa=request.POST.get('exp_empresa'), 
                descripcion=request.POST.get('exp_desc', '')
            )

        # Agregar Reconocimiento
        rec_t = request.POST.get('rec_titulo')
        if rec_t: 
            Reconocimiento.objects.create(
                perfil=perfil, 
                titulo=rec_t, 
                institucion_otorga=request.POST.get('rec_inst'), 
                fecha=request.POST.get('rec_fecha') or timezone.now().date(), 
                imagen=request.FILES.get('rec_imagen')
            )

        # Agregar Producto al Garage
        prod_n = request.POST.get('prod_nombre')
        if prod_n: 
            ProductoGarage.objects.create(
                nombre=prod_n, 
                precio=request.POST.get('prod_precio') or 0, 
                estado=request.POST.get('prod_estado'), 
                imagen=request.FILES.get('prod_imagen'), 
                disponible=True
            )

        return redirect('dashboard')

    lenguajes_disponibles = ['Python', 'JavaScript', 'Java', 'C#', 'PHP', 'SQL', 'Swift', 'Go', 'Kotlin']
    return render(request, 'dashboard.html', {'perfil': perfil, 'lenguajes_disponibles': lenguajes_disponibles})

# --- EXPORTACIÓN PDF CON FILTROS ---

def export_pdf(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    context = {
        'perfil': datos, 
        'user_viewed': user_profile,
        # Consultas de datos para llenar el PDF
        'estudios': Educacion.objects.filter(perfil=datos),
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos),
        'habilidades': Habilidad.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'certificados': Certificado.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'productos_garage': ProductoGarage.objects.filter(disponible=True),
        
        # Captura de checkboxes (filtros de visibilidad)
        'show_sobre_mi': request.GET.get('sobre_mi') == 'true',
        'show_lenguajes': request.GET.get('lenguajes') == 'true',
        'show_habilidades': request.GET.get('habilidades') == 'true',
        'show_experiencia': request.GET.get('experiencia') == 'true',
        'show_cursos': request.GET.get('cursos') == 'true',
        'show_reconocimientos': request.GET.get('reconocimientos') == 'true',
        'show_garage': request.GET.get('garage') == 'true',
    }
    return render(request, 'pdf_template.html', context)

# --- GESTIÓN DE TAREAS ---

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
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('tasks')
    return render(request, 'create_task.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    return render(request, 'task_detail.html', {'task': task, 'form': TaskForm(instance=task)})

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

# --- AUTENTICACIÓN ---

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html', {'form': form})

def signin(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')
