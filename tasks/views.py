from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales, ConfiguracionVisible,
    LenguajeProgramacion, Habilidad
)

# --- VISTA PRINCIPAL CON FILTRO ESTRICTO Y SALTO DIRECTO ---
def home(request):
    try:
        # 1. Filtramos estrictamente los perfiles habilitados
        perfiles_activos = DatosPersonales.objects.filter(activarparaqueseveaenfront=True)
        total_activos = perfiles_activos.count()

        # 2. Lógica de redirección automática:
        # Si hay exactamente 1 perfil y tiene un usuario vinculado, entramos directo
        if total_activos == 1:
            perfil_unico = perfiles_activos.first()
            if perfil_unico.user:
                return redirect('profile_cv', username=perfil_unico.user.username)

        # 3. Si hay 0 o más de 1, preparamos el contexto para el selector
        username_unico = ""
        # Esto es por si el botón "Empezar" en el JS necesita un valor base
        if total_activos > 0:
            primer_perfil = perfiles_activos.first()
            if primer_perfil.user:
                username_unico = primer_perfil.user.username

        # Obtenemos configuración global (ID 1)
        config_botones, _ = ConfiguracionVisible.objects.get_or_create(id=1)

        contexto = {
            'perfiles_activos': perfiles_activos,
            'total_activos': total_activos,
            'username_unico': username_unico,
            'config': config_botones,
        }
    except Exception as e:
        print(f"Error detectado: {e}")
        contexto = {
            'perfiles_activos': [], 
            'total_activos': 0, 
            'username_unico': "", 
            'config': None
        }
    
    return render(request, 'welcome.html', contexto)

# --- LAS DEMÁS VISTAS SE MANTIENEN IGUAL ---

# --- AUTENTICACIÓN ---
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
    
    if not perfil:
        return redirect('home')

    config_botones, _ = ConfiguracionVisible.objects.get_or_create(id=1)

    contexto = {
        'user_viewed': user_viewed,
        'perfil': perfil,
        'experiencias': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'reconocimientos': Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'productos_academicos': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True), 
        'productos_laborales': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'lenguajes': LenguajeProgramacion.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'habilidades': Habilidad.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True),
        'config': config_botones,
    }
    return render(request, 'profile_cv.html', contexto)

# --- GARAGE ---
def garage_store(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    
    config_botones, _ = ConfiguracionVisible.objects.get_or_create(id=1)
    
    if not config_botones.mostrar_garage:
        return redirect('profile_cv', username=username)

    productos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    
    return render(request, 'garage.html', {
        'user_viewed': user_viewed, 
        'productos': productos,
        'config': config_botones
    })

# --- EXPORTAR PDF ---
def export_pdf(request, username):
    user_viewed = get_object_or_404(User, username=username)
    perfil = DatosPersonales.objects.filter(user=user_viewed).first()
    
    if not perfil:
        return redirect('home')

    show_options = {
        'show_sobre_mi': request.GET.get('sobre_mi') == 'on',
        'show_lenguajes': request.GET.get('lenguajes') == 'on',
        'show_productos_acad': request.GET.get('productos_acad') == 'on',
        'show_habilidades': request.GET.get('habilidades') == 'on',
        'show_experiencia': request.GET.get('experiencia') == 'on',
        'show_certificados': request.GET.get('certificados') == 'on',
        'show_garage': request.GET.get('garage') == 'on',
    }

    contexto = {
        'user_viewed': user_viewed,
        'perfil': perfil,
        **show_options
    }

    if show_options['show_experiencia']:
        contexto['experiencias'] = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if show_options['show_habilidades']:
        contexto['habilidades'] = Habilidad.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if show_options['show_lenguajes']:
        contexto['lenguajes'] = LenguajeProgramacion.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if show_options['show_productos_acad']:
        contexto['productos_academicos'] = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if show_options['show_certificados']:
        contexto['cursos'] = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
        contexto['reconocimientos'] = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if show_options['show_garage']:
        contexto['productos_garage'] = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)

    return render(request, 'pdf_template.html', contexto)

# --- TAREAS Y DASHBOARD ---
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})