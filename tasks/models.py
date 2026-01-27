from django.db import models
from django.contrib.auth.models import User

# --- Tus modelos actuales de CV ---

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username

class DatosPersonales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    descripcionperfil = models.TextField()
    nacionalidad = models.CharField(max_length=50)
    numerocedula = models.CharField(max_length=20, unique=True)
    fechanacimiento = models.DateField()
    direcciondomiciliaria = models.CharField(max_length=200)
    instagram = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actualidad = models.BooleanField(default=False)
    descripcion = models.TextField()

class Habilidad(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Certificado(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    imagen = models.ImageField(upload_to='certificados/')

class Educacion(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    institucion = models.CharField(max_length=150)
    fecha_graduacion = models.DateField()

    def __str__(self):
        return self.institucion

class Lenguaje(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

# --- NUEVO: Sección de Venta de Garage ---

class ProductoGarage(models.Model):
    ESTADO_CHOICES = [
        ('NUEVO', 'Nuevo'),
        ('BUENO', 'Bueno'),
        ('REGULAR', 'Regular'),
        ('MALO', 'Para repuestos'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='garage/')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BUENO')
    disponible = models.BooleanField(default=True)
    fecha_publicado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto de Garage"
        verbose_name_plural = "Venta de Garage"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
