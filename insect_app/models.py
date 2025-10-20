from django.db import models
from django.contrib.auth.models import User # Importa el modelo de usuario predeterminado de Django
# Create your models here.    

class Temperatura(models.Model):
    temperatura = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    max_temperatura = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    min_temperatura = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    hora = models.TimeField(blank=False)
    area_de_trabajo = models.CharField(max_length=20,blank=False)
    obs = models.TextField(blank=True)

    # Añadimos los campos de fecha de creación y actualización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Temperatura {self.temperatura} a las {self.hora}"

class Humedad(models.Model):
    humedad = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    max_humedad = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    min_humedad = models.DecimalField(max_digits=5, decimal_places=1,null=True, blank=False,default=0.0)
    hora = models.TimeField(blank=False)
    area_de_trabajo = models.CharField(max_length=20,blank=False)
    obs = models.TextField(blank=True)

    # Añadimos los campos de fecha de creación y actualización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Humedad {self.humedad} a las {self.hora}"

class Vida(models.Model):
    
    especie = models.CharField(max_length=50,blank=False)
    cepa = models.CharField(max_length=50,blank=False)

    # Campos de fecha
    fecha_inicio_bandejas = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de inicio de las bandejas."
    )
    fecha_pupacion = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en que las larvas comenzaron a pupar."
    )

    # Campos enteros
    numero_bandejas_antes_trabajo = models.IntegerField(
        help_text="Número de bandejas encontradas antes del trabajo."
    )
    pupas_vivas = models.IntegerField(
        help_text="Cantidad de pupas vivas."
    )
    pupas_muertas = models.IntegerField(
        help_text="Cantidad de pupas muertas."
    )
    total_pupas_vivas_y_muertas = models.IntegerField(
        help_text="Total de pupas vivas y muertas."
    )
    larvas_muertas = models.IntegerField(
        help_text="Cantidad de larvas muertas."
    )
    bandejas_divididas = models.IntegerField(
        help_text="Número de bandejas que fueron divididas."
    )
    bandejas_existentes_despues_trabajo = models.IntegerField(
        help_text="Número de bandejas existentes después de realizar el trabajo."
    )

    # Campos de caracteres/texto
    am_pm_pupas_vivas = models.CharField(
        max_length=2,
        help_text="Indicador (AM/PM) para el registro de pupas vivas."
    )
    am_pm_pupas_muertas = models.CharField(
        max_length=2,
        help_text="Indicador (AM/PM) para el registro de pupas muertas."
    )
    am_pm_larvas_muertas = models.CharField(
        max_length=2,
        help_text="Indicador (AM/PM) para el registro de larvas muertas."
    )
    tiempo_bandeja = models.CharField(
        max_length=25,
        help_text="Tiempo registrado para la bandeja (minutos y hora)."
    )
    obs = models.TextField(blank=True)


    # Campos de timestamp (Django los maneja automáticamente con auto_now_add y auto_now)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Método de representación de cadena para el objeto Live.
        """
        return f"Registro de Vida {self.id} - Inicio Bandeja: {self.fecha_inicio_bandejas}"

    def save(self, *args, **kwargs):
        pupas_vivas = self.pupas_vivas if self.pupas_vivas is not None else 0
        pupas_muertas = self.pupas_muertas if self.pupas_muertas is not None else 0
        self.total_pupas_vivas_y_muertas = pupas_vivas + pupas_muertas
        super().save(*args, **kwargs)

class Mortalidad_pupas(models.Model):
    """
    Modelo Django para representar los registros de "mortalidad de pupas en criaderos"
    basado en el esquema de Laravel proporcionado, con campos en español.
    """
    # Clave primaria auto-incrementable (Django la añade por defecto si no se especifica)
    # id = models.BigAutoField(primary_key=True) # Django crea un campo 'id' automáticamente como BigAutoField

    # Relación con el modelo Strain
    cepa = models.CharField(max_length=50,blank=False)

    # Campo entero para la cantidad
    cantidad = models.IntegerField(
        help_text="Cantidad de pupas muertas registradas."
    )

    # Campo de caracteres/texto para observaciones
    obs = models.TextField(blank=True)


    # Campos de timestamp (Django los maneja automáticamente con auto_now_add y auto_now)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
        Método de representación de cadena para el objeto PupaMortalityInBreeder.
        """
        return f"Mortalidad de Pupa ID: {self.id} - Cantidad: {self.cantidad}"

class RegistroTemperaturaAgua(models.Model):
    """
    Modelo para registrar la temperatura del agua de las bandejas de cría de mosquitos.
    Basado en la estructura del archivo 'Registro Temperatura del agua de las bandejas de cría de mosquitos.xlsx - T Agua.csv'.
    """
    # ID (Django crea un campo 'id' automáticamente como BigAutoField, no es necesario definirlo explícitamente)
    
    fecha = models.DateField(
        verbose_name="Fecha del Registro",
        help_text="Fecha en la que se realizó el registro."
    )
    especie = models.CharField(
        max_length=100,
        verbose_name="Especie",
        help_text="Especie del mosquito."
    )
    cepa = models.CharField(
        max_length=100,
        verbose_name="Cepa",
        help_text="Cepa del mosquito."
    )
    fecha_bandeja = models.DateField(
        verbose_name="Fecha de Bandeja",
        help_text="Fecha de creación o inicio de la bandeja."
    )

    # Campos de temperatura para las 7:30 am
    temp_730am = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. 7:30 AM (°C)",
        help_text="Temperatura del agua a las 7:30 AM."
    )
    temp_max_730am = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Máx. 7:30 AM (°C)",
        help_text="Temperatura máxima registrada a las 7:30 AM."
    )
    temp_min_730am = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Mín. 7:30 AM (°C)",
        help_text="Temperatura mínima registrada a las 7:30 AM."
    )

    # Campos de temperatura para las 12:00 md
    temp_1200md = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. 12:00 MD (°C)",
        help_text="Temperatura del agua a las 12:00 MD."
    )
    temp_max_1200md = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Máx. 12:00 MD (°C)",
        help_text="Temperatura máxima registrada a las 12:00 MD."
    )
    temp_min_1200md = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Mín. 12:00 MD (°C)",
        help_text="Temperatura mínima registrada a las 12:00 MD."
    )

    # Campos de temperatura para las 15:00 pm
    temp_1500pm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. 15:00 PM (°C)",
        help_text="Temperatura del agua a las 15:00 PM."
    )
    temp_max_1500pm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Máx. 15:00 PM (°C)",
        help_text="Temperatura máxima registrada a las 15:00 PM."
    )
    temp_min_1500pm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Temp. Mín. 15:00 PM (°C)",
        help_text="Temperatura mínima registrada a las 15:00 PM."
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones",
        help_text="Cualquier observación adicional sobre el registro."
    )
    

    # Campos de timestamp para auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Temperatura del Agua"
        verbose_name_plural = "Registros de Temperatura del Agua"
        ordering = ['-fecha', 'especie', 'cepa'] # Ordenar por fecha descendente, luego especie y cepa

    def __str__(self):
        return f"Registro {self.fecha} - {self.especie} ({self.cepa})"