from django.contrib import admin
from django.urls import path, re_path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # 1. Rutas del Sistema (Prioridad Alta)
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),

    # 2. Rutas Dinámicas (Perfiles)
    # Al estar después de las fijas, Django solo entrará aquí si no coincide con las anteriores
    path('perfil/<str:username>/', views.profile_cv, name='profile_cv'),
    path('perfil/<str:username>/pdf/', views.export_pdf, name='export_pdf'),
    
    # 3. Archivos Media (Para PDFs y Fotos locales/Cloudinary)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Servir estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
