from django.db import models
from django.contrib.auth.models import User

# --- PERFIL PRINCIPAL ---
class DatosPersonales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fechanacimiento = models.DateField()
    numerocedula = models.CharField(max_length=15, unique=True)
    direcciondomiciliaria = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)
    descripcionperfil = models.TextField(blank=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# --- SECCIONES DEL CV ---
class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    descripcion = models.TextField()

class Habilidad(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Certificado(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='certificados/')

class Educacion(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    institucion = models.CharField(max_length=200)
    fecha_graduacion = models.DateField()

class Lenguaje(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

# --- NUEVA SECCIÓN: RECONOCIMIENTOS ---
class Reconocimiento(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    institucion_otorga = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.titulo} - {self.perfil.nombres}"

# --- SECCIÓN: VENTA DE GARAGE ---
class ProductoGarage(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='garage/')
    disponible = models.BooleanField(default=True)
    fecha_publicado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# --- TAREAS (DEL CRUD ORIGINAL) ---
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username
