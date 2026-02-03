from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# 1. PERFIL PRINCIPAL
class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    descripcionperfil = models.CharField(max_length=800, blank=True, null=True)
    perfilactivo = models.IntegerField(default=1)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60)
    fechanacimiento = models.DateField()
    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=[('H', 'M'), ('M', 'F')])
    estadocivil = models.CharField(max_length=50)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    
    activarparaqueseveaenfront = models.BooleanField(default=False, verbose_name="Activar para ver en Web")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# 2. EXPERIENCIA LABORAL
class ExperienciaLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50)
    emailempresa = models.CharField(max_length=100)
    sitiowebempresa = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100)
    telefonocontactoempresarial = models.CharField(max_length=60)
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField()
    descripcionfunciones = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
        upload_to='certificados/experiencia/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"

# 3. CURSOS REALIZADOS
class CursosRealizados(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrerecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    totalhoras = models.IntegerField()
    descripcioncurso = models.CharField(max_length=100)
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)
    emailempresapatrocinadora = models.CharField(max_length=60)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
        upload_to='certificados/cursos/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return self.nombrerecurso

# 4. RECONOCIMIENTOS
class Reconocimiento(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    tiporeconocimiento = models.CharField(max_length=100, choices=[('Académico', 'Académico'), ('Público', 'Público'), ('Privado', 'Privado')])
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.CharField(max_length=100)
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
        upload_to='certificados/reconocimientos/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return self.descripcionreconocimiento

# 5. PRODUCTOS ACADEMICOS
class ProductosAcademicos(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=800)
    activarparaqueseveaenfront = models.BooleanField(default=True)

# 6. PRODUCTOS LABORALES
class ProductosLaborales(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)

# 7. VENTA DE GARAGE
class VentaGarage(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=[('Bueno', 'Bueno'), ('Regular', 'Regular')])
    descripcion = models.CharField(max_length=100)
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='garage/', null=True, blank=True)

    def __str__(self):
        return self.nombreproducto

# 8. SISTEMA DE TAREAS
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - by {self.user.username}"

# 9. CONTROL DE VISIBILIDAD
class ConfiguracionVisible(models.Model):
    mostrar_garage = models.BooleanField(default=True, verbose_name="Mostrar Botón Garage")
    mostrar_cursos = models.BooleanField(default=True, verbose_name="Mostrar Botón Cursos")
    mostrar_reconocimientos = models.BooleanField(default=True, verbose_name="Mostrar Botón Reconocimientos")

    class Meta:
        verbose_name = "Configuración de Botones"
        verbose_name_plural = "Configuración de Botones"

    def __str__(self):
        return "Interruptores de Visibilidad"

# 10. LENGUAJES DE PROGRAMACIÓN
class LenguajeProgramacion(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    nivel_porcentaje = models.IntegerField(default=50, help_text="Nivel del 1 al 100")
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# 11. HABILIDADES
class Habilidad(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombre_habilidad = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[('Blanda', 'Habilidad Blanda'), ('Tecnica', 'Habilidad Técnica')], default='Tecnica')
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_habilidad