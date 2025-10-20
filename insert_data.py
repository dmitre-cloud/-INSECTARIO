import os
import re
from datetime import datetime, time
from decimal import Decimal
import django
from django.utils import timezone
from django.db import IntegrityError

# -----------------------------------------------------------------------------
# Configuración del entorno de Django
# Basado en tu estructura de archivos, el nombre del proyecto principal es
# 'insectario_project', que contiene el archivo settings.py.
# La ruta correcta para el módulo de configuración es 'insectario_project.settings'.
# -----------------------------------------------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insectario_project.settings')
django.setup()

# Asegúrate de reemplazar 'insect_app' con el nombre real de tu aplicación de Django
from insect_app.models import Temperatura, Humedad, Vida, Mortalidad_pupas, RegistroTemperaturaAgua
# Ya no necesitamos importar User si no vamos a asociar usuarios
# from django.contrib.auth.models import User

# Mapeo de IDs de cepas a nombres de texto
CEPA_MAPPING = {
    1: 'Agua Clara',
    2: 'Bajo Chiquito',
    3: 'Yaviza',
    4: 'Quebrada Peña',
    5: 'Marragantí',
    6: 'Rockefeller',
    7: '24 de Diciembre',
    8: 'New Orleans',
}

# Mapeo de IDs de especies a nombres de texto
SPECIE_MAPPING = {
    1: 'Anopheles albimanus',
    3: 'Aedes aegypti',
}

# Función auxiliar para parsear los valores de las sentencias SQL
def parse_sql_values(values_str):
    """
    Parsea una cadena de valores SQL, manejando NULLs y comillas simples.
    """
    values = []
    # Divide la cadena por comas, pero no si la coma está dentro de comillas simples
    parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", values_str)
    for part in parts:
        cleaned_part = part.strip()
        if cleaned_part.upper() == 'NULL':
            values.append(None)
        elif cleaned_part.startswith("'") and cleaned_part.endswith("'"):
            values.append(cleaned_part[1:-1].strip()) # Elimina las comillas y espacios internos
        else:
            values.append(cleaned_part)
    return values

# FUNCIÓN AUXILIAR PARA PARSEAR CADENAS DE HORA
def parse_time_string(time_str):
    """
    Convierte una cadena de hora (ej. '7:30 am', '12:00 md', '15:00 pm') a un objeto datetime.time.
    Intenta varios formatos comunes para mayor robustez. Si falla, devuelve time(0,0).
    """
    if time_str is None:
        return time(0, 0) # Default to midnight if None
    
    original_time_str = time_str.strip()

    # Check if it's a numeric string (e.g., '93', '29') - this was the previous issue
    if original_time_str.isdigit():
        # This warning is less critical now as it will simply default to 00:00:00
        # but indicates data might not be as expected in the SQL for this field.
        # print(f"ADVERTENCIA CRÍTICA: La cadena de hora '{original_time_str}' es numérica y no es un formato de hora válido. Devolviendo time(0,0) por defecto.")
        return time(0, 0)

    # Manejo específico para 'md' (mediodía) - convertir a '12:00 pm' para un parseo consistente
    if 'md' in original_time_str.lower():
        time_str_for_parse = original_time_str.lower().replace(' md', ' pm')
        try:
            parsed_time = datetime.strptime(time_str_for_parse, '%I:%M %p').time()
            return parsed_time
        except ValueError:
            pass # Continue with other formats if this fails

    # For AM/PM, the %p directive expects 'AM' or 'PM' (uppercase)
    time_str_upper_ampm = original_time_str.replace(' am', ' AM').replace(' pm', ' PM').replace('am', 'AM').replace('pm', 'PM')

    formats_to_try = [
        '%I:%M %p',  # E.g., '7:30 AM', '03:00 PM', '12:00 PM'
        '%I:%M%p',   # E.g., '7:30AM', '03:00PM' (no space)
        '%H:%M',     # E.g., '15:00', '07:30' (24-hour format)
        '%H:%M:%S',  # E.g., '07:30:00' (if seconds are present)
    ]

    for fmt in formats_to_try:
        try:
            str_to_parse = time_str_upper_ampm if '%p' in fmt else original_time_str
            parsed_time = datetime.strptime(str_to_parse, fmt).time()
            return parsed_time
        except ValueError:
            continue # If a format fails, try the next one
    
    # If no format matches, return default time
    # print(f"ADVERTENCIA: No se pudo parsear la hora '{original_time_str}'. Ninguno de los formatos intentados coincidió. Devolviendo time(0,0) por defecto.")
    return time(0, 0) # Fallback to midnight if parsing fails

def insert_data_from_sql_file():
    """
    Inserta datos desde el archivo SQL 'bd_insecta.sql' en los modelos de Django.
    Se adapta a la estructura de los modelos proporcionados por el usuario.
    """
    file_path = 'bd_insecta.sql'
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró en la ruta esperada.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # --- Inserción para la tabla `environmental_temperatures` -> modelo `Temperatura` ---
    temperatura_insert_pattern = re.compile(
        r"INSERT INTO `environmental_temperatures` \([^)]+\) VALUES\s*((?:\([^)]+\)(?:,\s*)?)+);"
    )
    temperatura_matches = temperatura_insert_pattern.findall(sql_content)

    temperatura_creados = 0
    for values_block_str in temperatura_matches:
        individual_value_sets = re.findall(r"\(([^)]+)\)", values_block_str)
        for values_str in individual_value_sets:
            parsed_values = parse_sql_values(values_str)
            
            # Orden esperado de los valores SQL (índices):
            # id (0), temperature (1), max_temperature (2), min_temperature (3),
            # hour (4), work_area (5), observations (6), user_id (7),
            # created_at (8), updated_at (9)
            
            try:
                # Se parsean las fechas de created_at y updated_at
                created_at = datetime.strptime(parsed_values[8], '%Y-%m-%d %H:%M:%S') if parsed_values[8] is not None else timezone.now()
                updated_at = datetime.strptime(parsed_values[9], '%Y-%m-%d %H:%M:%S') if parsed_values[9] is not None else timezone.now()

                data = {
                    'temperatura': Decimal(parsed_values[1]) if parsed_values[1] is not None else Decimal('0.0'),
                    'max_temperatura': Decimal(parsed_values[2]) if parsed_values[2] is not None else Decimal('0.0'),
                    'min_temperatura': Decimal(parsed_values[3]) if parsed_values[3] is not None else Decimal('0.0'),
                    'hora': parse_time_string(parsed_values[4]),
                    'area_de_trabajo': parsed_values[5],
                    'obs': parsed_values[6] if parsed_values[6] is not None else '',
                    'fecha_creacion': created_at,
                    'fecha_actualizacion': updated_at,
                }
                Temperatura.objects.create(**data)
                temperatura_creados += 1
            except IntegrityError:
                print(f"Advertencia: El registro de Temperatura (ID SQL: {parsed_values[0]}) ya existe o hay un conflicto. Saltando...")
            except Exception as e:
                print(f"Error al insertar datos de Temperatura (ID SQL: {parsed_values[0]}): {e} - Datos: {parsed_values}")
        
    print(f"Se insertaron {temperatura_creados} registros en el modelo Temperatura.")

    # --- Inserción para la tabla `humidities` -> modelo `Humedad` ---
    humedades_insert_pattern = re.compile(
        r"INSERT INTO `humidities` \([^)]+\) VALUES\s*((?:\([^)]+\)(?:,\s*)?)+);"
    )
    humedades_matches = humedades_insert_pattern.findall(sql_content)

    humedades_creados = 0
    for values_block_str in humedades_matches:
        individual_value_sets = re.findall(r"\(([^)]+)\)", values_block_str)
        for values_str in individual_value_sets:
            parsed_values = parse_sql_values(values_str)
            
            # Orden esperado de los valores SQL (índices):
            # id (0), humidity (1), max_humidity (2), min_humidity (3),
            # hour (4), work_area (5), observations (6), user_id (7),
            # created_at (8), updated_at (9)
            
            try:
                # Se parsean las fechas de created_at y updated_at
                created_at = datetime.strptime(parsed_values[8], '%Y-%m-%d %H:%M:%S') if parsed_values[8] is not None else timezone.now()
                updated_at = datetime.strptime(parsed_values[9], '%Y-%m-%d %H:%M:%S') if parsed_values[9] is not None else timezone.now()

                data = {
                    'humedad': Decimal(parsed_values[1]) if parsed_values[1] is not None else Decimal('0.0'),
                    'max_humedad': Decimal(parsed_values[2]) if parsed_values[2] is not None else Decimal('0.0'),
                    'min_humedad': Decimal(parsed_values[3]) if parsed_values[3] is not None else Decimal('0.0'),
                    'hora': parse_time_string(parsed_values[4]),
                    'area_de_trabajo': parsed_values[5],
                    'obs': parsed_values[6] if parsed_values[6] is not None else '',
                    'fecha_creacion': created_at,
                    'fecha_actualizacion': updated_at,
                }
                Humedad.objects.create(**data)
                humedades_creados += 1
            except IntegrityError:
                print(f"Advertencia: El registro de Humedad (ID SQL: {parsed_values[0]}) ya existe o hay un conflicto. Saltando...")
            except Exception as e:
                print(f"Error al insertar datos de Humedad (ID SQL: {parsed_values[0]}): {e} - Datos: {parsed_values}")
        
    print(f"Se insertaron {humedades_creados} registros en el modelo Humedad.")


    # --- Inserción para la tabla `lives` -> modelo `Vida` ---
    lives_insert_pattern = re.compile(
        r"INSERT INTO `lives` \([^)]+\) VALUES\s*((?:\([^)]+\)(?:,\s*)?)+);"
    )
    lives_matches = lives_insert_pattern.findall(sql_content)

    lives_creados = 0
    for values_block_str in lives_matches:
        individual_value_sets = re.findall(r"\(([^)]+)\)", values_block_str)
        for values_str in individual_value_sets:
            parsed_values = parse_sql_values(values_str)

            # Orden esperado de los valores SQL (índices):
            # id (0), specie_id (1), strain_id (2), tray_start_date (3), pupating_date (4),
            # number_of_trays_fbw (5), live_pupae (6), am_pm_live_pupae (7), dead_pupae (8),
            # am_pm_dead_pupae (9), total_live_and_dead_pupae (10), dead_larvae (11),
            # am_pm_dead_larvae (12), divided_trays (13), tray_time (14),
            # existing_trays_after_work_is_done (15), observations (16), user_id (17),
            # created_at (18), updated_at (19)
            
            # Conversión para 'bandejas_divididas' (SQL: VARCHAR, Django: IntegerField)
            bandejas_divididas_val = 0
            if parsed_values[13] is not None:
                if parsed_values[13].lower() == 'no':
                    bandejas_divididas_val = 0
                elif parsed_values[13].lower() == 'yes':
                    bandejas_divididas_val = 1
                else:
                    try:
                        bandejas_divididas_val = int(parsed_values[13])
                    except ValueError:
                        print(f"Advertencia: Valor no numérico para 'bandejas_divididas' en Vida (ID SQL: {parsed_values[0]}): '{parsed_values[13]}'. Se usará 0.")
                        bandejas_divididas_val = 0

            # Convertir el ID numérico de la especie a su nombre de texto
            especie_id = int(parsed_values[1]) if parsed_values[1] is not None else None
            especie_nombre = SPECIE_MAPPING.get(especie_id, f"Especie Desconocida ({especie_id})" if especie_id is not None else '')

            # Convertir el ID numérico de la cepa a su nombre de texto
            cepa_id = int(parsed_values[2]) if parsed_values[2] is not None else None
            cepa_nombre = CEPA_MAPPING.get(cepa_id, f"Cepa Desconocida ({cepa_id})" if cepa_id is not None else '')

            try:
                # Se parsean las fechas de created_at y updated_at
                created_at = datetime.strptime(parsed_values[18], '%Y-%m-%d %H:%M:%S') if parsed_values[18] is not None else timezone.now()
                updated_at = datetime.strptime(parsed_values[19], '%Y-%m-%d %H:%M:%S') if parsed_values[19] is not None else timezone.now()
                
                data = {
                    'especie': especie_nombre, # Usar el nombre de texto de la especie
                    'cepa': cepa_nombre, # Usar el nombre de texto de la cepa
                    'fecha_inicio_bandejas': datetime.strptime(parsed_values[3], '%Y-%m-%d').date() if parsed_values[3] is not None else None,
                    'fecha_pupacion': datetime.strptime(parsed_values[4], '%Y-%m-%d').date() if parsed_values[4] is not None else None,
                    'numero_bandejas_antes_trabajo': int(parsed_values[5]) if parsed_values[5] is not None else 0,
                    'pupas_vivas': int(parsed_values[6]) if parsed_values[6] is not None else 0,
                    'am_pm_pupas_vivas': parsed_values[7] if parsed_values[7] is not None else '',
                    'pupas_muertas': int(parsed_values[8]) if parsed_values[8] is not None else 0,
                    'am_pm_pupas_muertas': parsed_values[9] if parsed_values[9] is not None else '',
                    # 'total_pupas_vivas_y_muertas' se calcula en el método save del modelo, no se pasa aquí
                    'larvas_muertas': int(parsed_values[11]) if parsed_values[11] is not None else 0,
                    'am_pm_larvas_muertas': parsed_values[12] if parsed_values[12] is not None else '',
                    'bandejas_divididas': bandejas_divididas_val,
                    'tiempo_bandeja': parsed_values[14] if parsed_values[14] is not None else '',
                    'bandejas_existentes_despues_trabajo': int(parsed_values[15]) if parsed_values[15] is not None else 0,
                    'obs': parsed_values[16] if parsed_values[16] is not None else '',
                    'fecha_creacion': created_at,
                    'fecha_actualizacion': updated_at,
                }
                Vida.objects.create(**data)
                lives_creados += 1
            except IntegrityError:
                print(f"Advertencia: El registro de Vida (ID SQL: {parsed_values[0]}) ya existe o hay un conflicto. Saltando...")
            except Exception as e:
                print(f"Error al insertar datos de Vida (ID SQL: {parsed_values[0]}): {e} - Datos: {parsed_values}")

    print(f"Se insertaron {lives_creados} registros en el modelo Vida.")
    
    # --- Inserción para la tabla `pupa_mortality_in_breeders` -> modelo `Mortalidad_pupas` ---
    pupa_mortality_insert_pattern = re.compile(
        r"INSERT INTO `pupa_mortality_in_breeders` \([^)]+\) VALUES\s*((?:\([^)]+\)(?:,\s*)?)+);"
    )
    pupa_matches = pupa_mortality_insert_pattern.findall(sql_content)

    pupa_creados = 0
    for values_block_str in pupa_matches:
        individual_value_sets = re.findall(r"\(([^)]+)\)", values_block_str)
        for values_str in individual_value_sets:
            parsed_values = parse_sql_values(values_str)
            
            # Orden esperado de los valores SQL (índices):
            # id (0), breeder_code (1), dead_pupae_count (2), observations (3),
            # user_id (4), created_at (5), updated_at (6)

            # Convertir el ID numérico de la cepa a su nombre de texto
            cepa_id = int(parsed_values[1]) if parsed_values[1] is not None else None
            cepa_nombre = CEPA_MAPPING.get(cepa_id, f"Cepa Desconocida ({cepa_id})" if cepa_id is not None else '')
            
            try:
                # Se parsean las fechas de created_at y updated_at
                created_at = datetime.strptime(parsed_values[5], '%Y-%m-%d %H:%M:%S') if parsed_values[5] is not None else timezone.now()
                updated_at = datetime.strptime(parsed_values[6], '%Y-%m-%d %H:%M:%S') if parsed_values[6] is not None else timezone.now()
                
                data = {
                    'cepa': cepa_nombre, # Usar el nombre de texto de la cepa
                    'cantidad': int(parsed_values[2]) if parsed_values[2] is not None else 0,
                    'obs': parsed_values[3] if parsed_values[3] is not None else '',
                    'fecha_creacion': created_at,
                    'fecha_actualizacion': updated_at,
                }
                Mortalidad_pupas.objects.create(**data)
                pupa_creados += 1
            except IntegrityError:
                print(f"Advertencia: El registro de Mortalidad_pupas (ID SQL: {parsed_values[0]}) ya existe o hay un conflicto. Saltando...")
            except Exception as e:
                print(f"Error al insertar datos de Mortalidad_pupas (ID SQL: {parsed_values[0]}): {e} - Datos: {parsed_values}")
        
    print(f"Se insertaron {pupa_creados} registros en el modelo Mortalidad_pupas.")

    # --- Inserción para la tabla `tray_water_temperatures` -> modelo `RegistroTemperaturaAgua` ---
    registro_temp_agua_insert_pattern = re.compile(
        r"INSERT INTO `tray_water_temperatures` \([^)]+\) VALUES\s*((?:\([^)]+\)(?:,\s*)?)+);"
    )
    registro_temp_agua_matches = registro_temp_agua_insert_pattern.findall(sql_content)

    registro_temp_agua_creados = 0
    for values_block_str in registro_temp_agua_matches:
        individual_value_sets = re.findall(r"\(([^)]+)\)", values_block_str)
        for values_str in individual_value_sets:
            parsed_values = parse_sql_values(values_str)

            # Orden esperado de los valores SQL para `tray_water_temperatures` (índices):
            # id (0), date (1), specie_id (2), strain_id (3), tray_date (4),
            # temp_730am (5), temp_max_730am (6), temp_min_730am (7),
            # temp_1200md (8), temp_max_1200md (9), temp_min_1200md (10),
            # temp_1500pm (11), temp_max_1500pm (12), temp_min_1500pm (13),
            # observations (14), user_id (15), created_at (16), updated_at (17)

            # Convertir el ID numérico de la especie a su nombre de texto
            especie_id = int(parsed_values[2]) if parsed_values[2] is not None else None
            especie_nombre = SPECIE_MAPPING.get(especie_id, f"Especie Desconocida ({especie_id})" if especie_id is not None else '')

            # Convertir el ID numérico de la cepa a su nombre de texto
            cepa_id = int(parsed_values[3]) if parsed_values[3] is not None else None
            cepa_nombre = CEPA_MAPPING.get(cepa_id, f"Cepa Desconocida ({cepa_id})" if cepa_id is not None else '')
            
            try:
                data = {
                    'fecha': datetime.strptime(parsed_values[1], '%Y-%m-%d').date() if parsed_values[1] is not None else None,
                    'especie': especie_nombre,
                    'cepa': cepa_nombre,
                    'fecha_bandeja': datetime.strptime(parsed_values[4], '%Y-%m-%d').date() if parsed_values[4] is not None else None,
                    'temp_730am': Decimal(parsed_values[5]) if parsed_values[5] is not None else None,
                    'temp_max_730am': Decimal(parsed_values[6]) if parsed_values[6] is not None else None,
                    'temp_min_730am': Decimal(parsed_values[7]) if parsed_values[7] is not None else None,
                    'temp_1200md': Decimal(parsed_values[8]) if parsed_values[8] is not None else None,
                    'temp_max_1200md': Decimal(parsed_values[9]) if parsed_values[9] is not None else None,
                    'temp_min_1200md': Decimal(parsed_values[10]) if parsed_values[10] is not None else None,
                    'temp_1500pm': Decimal(parsed_values[11]) if parsed_values[11] is not None else None,
                    'temp_max_1500pm': Decimal(parsed_values[12]) if parsed_values[12] is not None else None,
                    'temp_min_1500pm': Decimal(parsed_values[13]) if parsed_values[13] is not None else None,
                    'observaciones': parsed_values[14] if parsed_values[14] is not None else '',
                }
                RegistroTemperaturaAgua.objects.create(**data)
                registro_temp_agua_creados += 1
            except IntegrityError:
                print(f"Advertencia: El registro de RegistroTemperaturaAgua (ID SQL: {parsed_values[0]}) ya existe o hay un conflicto. Saltando...")
            except Exception as e:
                print(f"Error al insertar datos de RegistroTemperaturaAgua (ID SQL: {parsed_values[0]}): {e} - Datos: {parsed_values}")
        
    print(f"Se insertaron {registro_temp_agua_creados} registros en el modelo RegistroTemperaturaAgua.")


if __name__ == '__main__':
    insert_data_from_sql_file()
