from django import forms
from insect_app.models import *
from django.contrib.auth.forms import AuthenticationForm # Importa AuthenticationForm

CEPAS = [
    ("", "--- Seleccione ---"),
    ("Agua Clara", "Agua Clara"),
    ("Bajo Chiquito", "Bajo Chiquito"),
    ("Yaviza", "Yaviza"),
    ("Quebrada Peña", "Quebrada Peña"),
    ("Marragantí", "Marragantí"),
    ("Rockefeller", "Rockefeller"),
    ("24 de Diciembre", "24 de Diciembre"),
    ("Guatemala", "Guatemala"),
    ("Puerto Limón", "Puerto Limón"),
    ]

ESPECIES = [
    ("", "--- Seleccione ---"),
    ("Anopheles albimanus", "Anopheles albimanus"),
    ("Aedes aegypti", "Aedes aegypti"),
    ]

AM_PM = [
        ('', '--- Seleccione ---'),
        ('AM', 'AM'),
        ('PM', 'PM'),
    ]

AREA_DE_TRABAJO = [
        ('', '--- Seleccione ---'),
        ('Área Fase Inmadura', 'Área Fase Inmadura'),
        ('Área Fase Adulta', 'Área Fase Adulta'),
    ]

class TemperaturaForm(forms.ModelForm):
    """
    Formulario para el modelo Temperatura.
    """
    class Meta:
        model = Temperatura
        # Incluye todos los campos del modelo en el formulario,
        # excepto los que Django gestiona automáticamente como 'id'
        # y los timestamps si se usan auto_now_add/auto_now.
        fields = '__all__'
        widgets = {
            'temperatura': forms.NumberInput(attrs={'placeholder': 'Ej. 25.5','class':'form-control'}),
            'max_temperatura': forms.NumberInput(attrs={'placeholder': 'Ej. 30.0','class':'form-control'}),
            'min_temperatura': forms.NumberInput(attrs={'placeholder': 'Ej. 20.0','class':'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), # Actualizado para TimeField
            'area_de_trabajo': forms.Select(choices=AREA_DE_TRABAJO,attrs={'placeholder': '','class':'form-select'}),
            'obs': forms.Textarea(attrs={'rows': 1, 'class':'form-control'}),
            
        }
        labels = {
            'temperatura': 'Temperatura',
            'max_temperatura': 'Temperatura Máxima',
            'min_temperatura': 'Temperatura Mínima',
            'hora': 'Hora',
            'area_de_trabajo': 'Área de Trabajo',
            'obs': 'Observaciones',
        }
        help_texts = {
            'temperatura': 'Temperatura actual registrada.',
            'max_temperatura': 'Temperatura máxima registrada.',
            'min_temperatura': 'Temperatura mínima registrada.',
            'hora': 'Hora del registro (ej. HH:MM).',
            'area_de_trabajo': 'Área donde se tomó el registro.',
            'obs': 'Cualquier observación adicional.',
        }

class HumedadForm(forms.ModelForm):
    """
    Formulario para el modelo Humedad.
    """
    class Meta:
        model = Humedad
        fields = '__all__'
        widgets = {
            'humedad': forms.NumberInput(attrs={'placeholder': 'Ej. 25.5','class':'form-control'}),
            'max_humedad': forms.NumberInput(attrs={'placeholder': 'Ej. 30.0','class':'form-control'}),
            'min_humedad': forms.NumberInput(attrs={'placeholder': 'Ej. 20.0','class':'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), # Actualizado para TimeField
            'area_de_trabajo': forms.Select(choices=AREA_DE_TRABAJO,attrs={'placeholder': '','class':'form-select'}),
            'obs': forms.Textarea(attrs={'rows': 1, 'class':'form-control'}),
            
        }
        labels = {
            'humedad': 'Humedad',
            'max_humedad': 'Humedad Máxima',
            'min_humedad': 'Humedad Mínima',
            'hora': 'Hora',
            'area_de_trabajo': 'Área de Trabajo',
            'obs': 'Observaciones',
        }
        help_texts = {
            'humedad': 'Humedad actual registrada.',
            'max_humedad': 'Humedad máxima registrada.',
            'min_humedad': 'Humedad mínima registrada.',
            'hora': 'Hora del registro (ej. HH:MM).',
            'area_de_trabajo': 'Área donde se tomó el registro.',
            'obs': 'Cualquier observación adicional.',
        }

class VidaForm(forms.ModelForm):
    """
    Formulario para el modelo Vida.
    """
    
    class Meta:
        model = Vida
        fields = '__all__'
        widgets = {
            'especie': forms.Select(choices=ESPECIES,attrs={'placeholder': '','class':'form-select'}),
            'cepa': forms.Select(choices=CEPAS,attrs={'placeholder': '','class':'form-select'}),
            'fecha_inicio_bandejas': forms.DateInput(attrs={'placeholder': '','type': 'date', 'class':'form-control'}),
            'fecha_pupacion': forms.DateInput(attrs={'placeholder': '','type': 'date', 'class':'form-control'}),
            'numero_bandejas_antes_trabajo': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'pupas_vivas': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'pupas_muertas': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'total_pupas_vivas_y_muertas': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'larvas_muertas': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'bandejas_divididas': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'bandejas_existentes_despues_trabajo': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'am_pm_pupas_vivas' : forms.Select(choices=AM_PM,attrs={'placeholder': '', 'class':'form-select'}),
            'am_pm_pupas_muertas' : forms.Select(choices=AM_PM,attrs={'placeholder': '', 'class':'form-select'}),
            'am_pm_larvas_muertas' : forms.Select(choices=AM_PM,attrs={'placeholder': '', 'class':'form-select'}),
            'tiempo_bandeja': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'obs': forms.Textarea(attrs={'rows': 1, 'class':'form-control'}),
            
        }
        # Los 'labels' y 'help_texts' se pueden omitir si ya están definidos en el modelo
        # con 'verbose_name' y 'help_text' respectivamente.
        # Sin embargo, los incluyo aquí para mostrar cómo se pueden personalizar en el formulario.
        labels = {
            'especie': 'Especie',
            'cepa': 'Cepa',
            'fecha_inicio_bandejas': 'Fecha de Inicio de Bandejas',
            'fecha_pupacion': 'Fecha de Pupación',
            'numero_bandejas_antes_trabajo': 'Número de Bandejas Antes del Trabajo',
            'pupas_vivas': 'Pupas Vivas',
            'pupas_muertas': 'Pupas Muertas',
            'total_pupas_vivas_y_muertas': 'Total Pupas Vivas y Muertas',
            'larvas_muertas': 'Larvas Muertas',
            'bandejas_divididas': 'Bandejas Divididas',
            'bandejas_existentes_despues_trabajo': 'Bandejas Después del Trabajo',
            'am_pm_pupas_vivas': 'AM/PM Pupas Vivas',
            'am_pm_pupas_muertas': 'AM/PM Pupas Muertas',
            'am_pm_larvas_muertas': 'AM/PM Larvas Muertas',
            'tiempo_bandeja': 'Tiempo de Bandeja',
            'obs': 'Observaciones',
        }
        # Los 'help_texts' se heredan del modelo si no se especifican aquí.
        # help_texts = { ... }

class MortalidadPupasForm(forms.ModelForm):
    """
    Formulario para el modelo Mortalidad_pupas.
    """
    class Meta:
        model = Mortalidad_pupas
        fields = '__all__'
        widgets = {
            'cepa': forms.Select(choices=CEPAS,attrs={'placeholder': '','class':'form-select'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': '','class':'form-control'}),
            'obs': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
        }
        labels = {
            'cepa': 'Cepa',
            'cantidad': 'Cantidad',
            'obs': 'Observaciones',
        }
        help_texts = {
            'cepa': 'Cepa a la que corresponde la mortalidad.',
            'cantidad': 'Cantidad de pupas muertas registradas.',
            'obs': 'Cualquier observación adicional sobre la mortalidad.',
        }


# --- Formulario de Autenticación Personalizado ---
class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado para aplicar estilos de Bootstrap.
    """
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre de usuario'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )

class RegistroTemperaturaAguaForm(forms.ModelForm):
    """
    Formulario para el modelo RegistroTemperaturaAgua.
    """
    class Meta:
        model = RegistroTemperaturaAgua
        fields = '__all__' # Incluye todos los campos del modelo
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            'especie': forms.Select(choices=ESPECIES,attrs={'placeholder': '','class':'form-select'}),
            'cepa': forms.Select(choices=CEPAS,attrs={'placeholder': '','class':'form-select'}),
            
            'fecha_bandeja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            'temp_730am': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 25.50'}),
            'temp_max_730am': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 26.00'}),
            'temp_min_730am': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 24.00'}),
            
            'temp_1200md': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 28.15'}),
            'temp_max_1200md': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 29.00'}),
            'temp_min_1200md': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 27.50'}),
            
            'temp_1500pm': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 27.00'}),
            'temp_max_1500pm': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 27.80'}),
            'temp_min_1500pm': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Ej. 26.50'}),
            
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Añadir observaciones aquí...'}),
        
        }
        # Los 'labels' y 'help_texts' se pueden omitir si ya están definidos en el modelo
        # con 'verbose_name' y 'help_text' respectivamente.
        # Sin embargo, los incluyo aquí para mostrar cómo se pueden personalizar en el formulario.
        labels = {
            'fecha': 'Fecha',
            'fecha_bandeja': 'Fecha de Bandeja',
            'temp_730am': 'Temp. 7:30 AM',
            'temp_max_730am': 'Temp. Máx. 7:30 AM',
            'temp_min_730am': 'Temp. Mín. 7:30 AM',
            'temp_1200md': 'Temp. 12:00 MD',
            'temp_max_1200md': 'Temp. Máx. 12:00 MD',
            'temp_min_1200md': 'Temp. Mín. 12:00 MD',
            'temp_1500pm': 'Temp. 15:00 PM',
            'temp_max_1500pm': 'Temp. Máx. 15:00 PM',
            'temp_min_1500pm': 'Temp. Mín. 15:00 PM',
            'observaciones': 'Observaciones',
            
        }
        # help_texts se heredan del modelo si no se especifican aquí.