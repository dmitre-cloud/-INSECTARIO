from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout # Importa funciones de autenticación
from django.contrib.auth.decorators import login_required # Decorador para requerir inicio de sesión
from .models import Temperatura, Humedad, Vida, Mortalidad_pupas, RegistroTemperaturaAgua
from .forms import TemperaturaForm, HumedadForm, VidaForm, MortalidadPupasForm, CustomAuthenticationForm, RegistroTemperaturaAguaForm # Asegúrate de usar el nombre correcto del formulario
import json
from datetime import datetime # ¡Importante! Necesitamos la fecha actual

def get_spanish_month(month_number):
    """Devuelve el nombre del mes en español."""
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    return meses.get(month_number, 'Mes Desconocido')


@login_required 
def dashboard_view(request):
    """
    Vista para mostrar los gráficos del dashboard con los 10 valores más altos del mes actual.
    """
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Consultas (sin cambios, asumiendo que ya tienen el fix de float())
    top_temperaturas = Temperatura.objects.filter(
        fecha_creacion__year=current_year,
        fecha_creacion__month=current_month
    ).order_by('-temperatura')[:10]

    top_humedades = Humedad.objects.filter(
        fecha_creacion__year=current_year,
        fecha_creacion__month=current_month
    ).order_by('-humedad')[:10]

    # **CORRECCIÓN DE ETIQUETAS: Usar SOLO la hora (HH:MM)**
    labels_temp = [t.fecha_creacion.strftime('%H:%M') for t in top_temperaturas]
    data_temp = [float(t.temperatura) for t in top_temperaturas]

    labels_hum = [h.fecha_creacion.strftime('%H:%M') for h in top_humedades]
    data_hum = [float(h.humedad) for h in top_humedades]

    spanish_month = get_spanish_month(now.month)
    
    context = {
        'titulo': f'Top 10 del Mes ({spanish_month})',
        'labels_temp': json.dumps(labels_temp),
        'data_temp': json.dumps(data_temp),
        'labels_hum': json.dumps(labels_hum),
        'data_hum': json.dumps(data_hum),
    }
    
    return render(request, 'dashboard.html', context)

# --- Vistas de Autenticación ---

def login_view(request):
    """
    Vista para el inicio de sesión de usuarios.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # CAMBIA ESTA LÍNEA
                return redirect('dashboard') # Redirige al dashboard
            else:
                form.add_error(None, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form, 'titulo': 'Iniciar Sesión'})

@login_required # Requiere que el usuario esté logueado para acceder a esta vista
def logout_view(request):
    """
    Vista para cerrar la sesión del usuario.
    """
    logout(request)
    return redirect('login') # Redirige a la página de login después de cerrar sesión

# --- Vistas para el modelo Temperatura ---

@login_required # Protege esta vista, solo usuarios logueados pueden acceder
def temperatura_list(request):
    """
    Muestra una lista de todos los registros de Temperatura.
    """
    temperaturas = Temperatura.objects.all().order_by('-fecha_creacion') # Ordenar por fecha de creación descendente
    return render(request, 'temperatura_list.html', {'temperaturas': temperaturas})

@login_required
def temperatura_create(request):
    """
    Permite crear un nuevo registro de Temperatura.
    """
    if request.method == 'POST':
        form = TemperaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('temperatura_list') # Redirige a la lista después de guardar
    else:
        form = TemperaturaForm()
    return render(request, 'temperatura_form.html', {'form': form, 'titulo': 'Crear Registro de Temperatura'})

@login_required
def temperatura_update(request, pk):
    """
    Permite actualizar un registro de Temperatura existente.
    """
    temperatura = get_object_or_404(Temperatura, pk=pk)
    if request.method == 'POST':
        form = TemperaturaForm(request.POST, instance=temperatura)
        if form.is_valid():
            form.save()
            return redirect('temperatura_list')
    else:
        form = TemperaturaForm(instance=temperatura)
    return render(request, 'temperatura_form.html', {'form': form, 'titulo': 'Actualizar Registro de Temperatura'})

@login_required
def temperatura_delete(request, pk):
    """
    Permite eliminar un registro de Temperatura.
    """
    temperatura = get_object_or_404(Temperatura, pk=pk)
    if request.method == 'POST':
        temperatura.delete()
        return redirect('temperatura_list')
    return render(request, 'temperatura_confirm_delete.html', {'temperatura': temperatura})


# --- Vistas para el modelo Humedad ---

@login_required
def humedad_list(request):
    """
    Muestra una lista de todos los registros de Humedad.
    """
    humedades = Humedad.objects.all().order_by('-fecha_creacion')
    return render(request, 'humedad_list.html', {'humedades': humedades})

@login_required
def humedad_create(request):
    """
    Permite crear un nuevo registro de Humedad.
    """
    if request.method == 'POST':
        form = HumedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('humedad_list')
    else:
        form = HumedadForm()
    return render(request, 'humedad_form.html', {'form': form, 'titulo': 'Crear Registro de Humedad'})

@login_required
def humedad_update(request, pk):
    """
    Permite actualizar un registro de Humedad existente.
    """
    humedad = get_object_or_404(Humedad, pk=pk)
    if request.method == 'POST':
        form = HumedadForm(request.POST, instance=humedad)
        if form.is_valid():
            form.save()
            return redirect('humedad_list')
    else:
        form = HumedadForm(instance=humedad)
    return render(request, 'humedad_form.html', {'form': form, 'titulo': 'Actualizar Registro de Humedad'})

@login_required
def humedad_delete(request, pk):
    """
    Permite eliminar un registro de Humedad.
    """
    humedad = get_object_or_404(Humedad, pk=pk)
    if request.method == 'POST':
        humedad.delete()
        return redirect('humedad_list')
    return render(request, 'humedad_confirm_delete.html', {'humedad': humedad})


# --- Vistas para el modelo Vida ---

@login_required
def vida_list(request):
    """
    Muestra una lista de todos los registros de Vida.
    """
    vidas = Vida.objects.all().order_by('-fecha_creacion')
    return render(request, 'vida_list.html', {'vidas': vidas})

@login_required
def vida_create(request):
    """
    Permite crear un nuevo registro de Vida.
    """
    if request.method == 'POST':
        form = VidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vida_list')
    else:
        form = VidaForm()
    return render(request, 'vida_form.html', {'form': form, 'titulo': 'Crear Registro de Vida'})

@login_required
def vida_update(request, pk):
    """
    Permite actualizar un registro de Vida existente.
    """
    vida = get_object_or_404(Vida, pk=pk)
    if request.method == 'POST':
        form = VidaForm(request.POST, instance=vida)
        if form.is_valid():
            form.save()
            return redirect('vida_list')
    else:
        form = VidaForm(instance=vida)
    return render(request, 'vida_form.html', {'form': form, 'titulo': 'Actualizar Registro de Vida'})

@login_required
def vida_delete(request, pk):
    """
    Permite eliminar un registro de Vida.
    """
    vida = get_object_or_404(Vida, pk=pk)
    if request.method == 'POST':
        vida.delete()
        return redirect('vida_list')
    return render(request, 'vida_confirm_delete.html', {'vida': vida})


# --- Vistas para el modelo Mortalidad_pupas ---

@login_required
def mortalidad_pupas_list(request):
    """
    Muestra una lista de todos los registros de Mortalidad_pupas.
    """
    mortalidades = Mortalidad_pupas.objects.all().order_by('-fecha_creacion')
    return render(request, 'mortalidad_pupas_list.html', {'mortalidades': mortalidades})

@login_required
def mortalidad_pupas_create(request):
    """
    Permite crear un nuevo registro de Mortalidad_pupas.
    """
    if request.method == 'POST':
        form = MortalidadPupasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mortalidad_pupas_list')
    else:
        form = MortalidadPupasForm()
    return render(request, 'mortalidad_pupas_form.html', {'form': form, 'titulo': 'Crear Registro de Mortalidad de Pupas'})

@login_required
def mortalidad_pupas_update(request, pk):
    """
    Permite actualizar un registro de Mortalidad_pupas existente.
    """
    mortalidad = get_object_or_404(Mortalidad_pupas, pk=pk)
    if request.method == 'POST':
        form = MortalidadPupasForm(request.POST, instance=mortalidad)
        if form.is_valid():
            form.save()
            return redirect('mortalidad_pupas_list')
    else:
        form = MortalidadPupasForm(instance=mortalidad)
    return render(request, 'mortalidad_pupas_form.html', {'form': form, 'titulo': 'Actualizar Registro de Mortalidad de Pupas'})

@login_required
def mortalidad_pupas_delete(request, pk):
    """
    Permite eliminar un registro de Mortalidad_pupas.
    """
    mortalidad = get_object_or_404(Mortalidad_pupas, pk=pk)
    if request.method == 'POST':
        mortalidad.delete()
        return redirect('mortalidad_pupas_list')
    return render(request, 'mortalidad_pupas_confirm_delete.html', {'mortalidad': mortalidad})


def registrotemperaturaagua_list(request):
    """
    Muestra una lista de todos los registros de Temperatura del Agua.
    """
    registros = RegistroTemperaturaAgua.objects.all().order_by('-fecha_creacion')
    return render(request, 'registrotemperaturaagua_list.html', {'registros': registros})

def registrotemperaturaagua_create(request):
    """
    Permite crear un nuevo registro de Temperatura del Agua.
    """
    if request.method == 'POST':
        form = RegistroTemperaturaAguaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrotemperaturaagua_list')
    else:
        form = RegistroTemperaturaAguaForm()
    return render(request, 'registrotemperaturaagua_form.html', {'form': form, 'titulo': 'Crear Nuevo Registro de Temperatura del Agua'})

def registrotemperaturaagua_update(request, pk):
    """
    Permite actualizar un registro de Temperatura del Agua existente.
    """
    registro = get_object_or_404(RegistroTemperaturaAgua, pk=pk)
    if request.method == 'POST':
        form = RegistroTemperaturaAguaForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('registrotemperaturaagua_list')
    else:
        form = RegistroTemperaturaAguaForm(instance=registro)
    return render(request, 'registrotemperaturaagua_form.html', {'form': form, 'titulo': 'Actualizar Registro de Temperatura del Agua'})

def registrotemperaturaagua_delete(request, pk):
    """
    Permite eliminar un registro de Temperatura del Agua.
    """
    registro = get_object_or_404(RegistroTemperaturaAgua, pk=pk)
    if request.method == 'POST':
        registro.delete()
        return redirect('registrotemperaturaagua_list')
    return render(request, 'registrotemperaturaagua_confirm_delete.html', {'registro': registro})