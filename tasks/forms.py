from django import forms
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, Reconocimiento, VentaGarage,
    ProductosAcademicos, ProductosLaborales
)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escribe un título'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Escribe una descripción'}),                               
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }

# Formulario para Datos Personales (incluye numerocedula y sexo)
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        exclude = ['user', 'perfilactivo']
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'numerocedula': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
        }

# Formulario para Garage (maneja numeric(5,2))
class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        exclude = ['idperfilconqueestaactivo']
        widgets = {
            'valordelbien': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'estadoproducto': forms.Select(attrs={'class': 'form-select'}),
        }

# Formulario para Cursos (maneja totalhoras y emails)
class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        exclude = ['idperfilconqueestaactivo']
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fechafin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'totalhoras': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para Reconocimientos (maneja el check de tipos)
class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = ['idperfilconqueestaactivo']
        widgets = {
            'tiporeconocimiento': forms.Select(attrs={'class': 'form-select'}),
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }