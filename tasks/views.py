# ... (manten tus imports iguales)
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Habilidad, 
    Certificado, Educacion, Lenguaje, ProductoGarage, Reconocimiento, ConfiguracionVisible
)

# ... (home, dashboard, etc. quedan igual)

def profile_cv(request, username):
    user_profile = get_object_or_404(User, username=username)
    datos = DatosPersonales.objects.filter(user=user_profile).first()
    
    if not datos:
        return render(request, 'profile_cv.html', {
            'error': 'Este perfil profesional aún no ha sido configurado.',
            'user_viewed': user_profile
        })
    
    # Obtenemos la configuración de visibilidad (o una por defecto si no existe)
    config, created = ConfiguracionVisible.objects.get_or_create(pk=1)
    
    context = {
        'perfil': datos, 
        'experiencias': ExperienciaLaboral.objects.filter(perfil=datos), 
        'habilidades': Habilidad.objects.filter(perfil=datos), 
        'certificados': Certificado.objects.filter(perfil=datos),
        'estudios': Educacion.objects.filter(perfil=datos),
        'lenguajes': Lenguaje.objects.filter(perfil=datos),
        'reconocimientos': Reconocimiento.objects.filter(perfil=datos),
        'user_viewed': user_profile,
        'config': config,  # Enviamos los interruptores
    }
    return render(request, 'profile_cv.html', context)

# ... (el resto de las funciones quedan igual)
