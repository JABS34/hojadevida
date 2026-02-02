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

# --- VISTAS DE USUARIO (DASHBOARD) ---

@login_required
def dashboard(request):
    perfil, created = DatosPersonales.objects.get_or_create(
        user=request.user,
        defaults={
            'nombres': request.user.first_name or request.user.username,
            'apellidos': request.user.last_name or 'Completar',
            'fechanacimiento': '1990-01-01',
            'numerocedula': f"TEMP-{request.user.id}"
        }
    )

    if request.method == 'POST':
        perfil.nombres = request.POST.get('nombres')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.instagram = request.POST.get('instagram')
        perfil.descripcionperfil = request.POST.get('descripcionperfil')
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        perfil.save()

        seleccionados = request.POST.getlist('lenguajes')
        if seleccionados:
            Lenguaje.objects.filter(perfil=perfil).delete()
            for lang in seleccionados:
                Lenguaje.objects.create(perfil=perfil, nombre=lang)

        edu_titulo = request.POST.get('edu_titulo')
        edu_inst = request.POST.get('edu_inst')
        if edu_titulo and edu_inst:
            Educacion.objects.create(
                perfil=perfil,
                titulo=edu_titulo,
                institucion=edu_inst,
                fecha_graduacion=request.POST.get('edu_fecha') or timezone.now().date()
            )

        hab_nom = request.POST.get('hab_nombre')
        if hab_nom:
            Habilidad.objects.create(perfil=perfil, nombre=hab_nom)

        exp_puesto = request.POST.get('exp_puesto')
        exp_empresa = request.POST.get('exp_empresa')
        if exp_puesto and exp_empresa:
            ExperienciaLaboral.objects.create(
                perfil=perfil,
                puesto=exp_puesto,
                empresa=exp_empresa,
                descripcion=request.POST.get('exp_desc', '')
            )

        rec_titulo = request.POST.get('rec_titulo')
        if rec_titulo:
            Reconocimiento.objects.create(
                perfil=perfil,
                titulo=rec_titulo,
                descripcion=request.POST.get('rec_desc', ''),
                fecha=request.POST.get('rec_fecha') or timezone.now().date(),
                institucion_otorga=request.POST.get('rec_inst', 'No especificado'),
                imagen=request.FILES.get('rec_imagen')
            )

        prod_nom = request.POST.get('prod_nombre')
        if prod_nom:
            ProductoGarage.objects.create(
                nombre=prod_nom,
                precio=request.POST.get('prod_precio') or 0,
                descripcion=request.POST.get('prod_desc', ''),
                estado=request.POST.get('prod_estado', 'Nuevo'),
                imagen=request.FILES.get('prod_imagen'),
                disponible=True
            )

        return redirect('dashboard')

    lenguajes_disponibles = ['Python', 'JavaScript', 'Java', 'C#', 'PHP', 'Ruby', 'SQL', 'Swift', 'Go', 'Kotlin']
    return render(request, 'dashboard.html', {
        'perfil': perfil,
        'lenguajes_disponibles': lenguajes_disponibles
    })

# --- EXPORTACIÓN PDF ---

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
        'productos_garage': ProductoGarage.objects.filter(disponible=True),
    }
    return render(request, 'pdf_template.html', context)

# --- AUTENTICACIÓN ---

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
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'Credenciales incorrectas'})

def signout(request):
    logout(request)
    return redirect('home')

# --- GESTIÓN DE TAREAS ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks, 'tipopagina': 'Tareas Pendientes'})

@login_required
def create_task(request):
    if request.method == 'GET': 
        return render(request, 'create_task.html', {'form': TaskForm()})
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')
    return render(request, 'create_task.html', {'form': form, 'error': 'Error al crear tarea'})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST': 
        task.delete()
    return redirect('tasks')
