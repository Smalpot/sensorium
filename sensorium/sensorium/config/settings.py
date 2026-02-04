"""
Configuraciones generales del sistema SENSORIUM
"""

# ========================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ========================================================================

# Configuración de SQL Server
DATABASE_CONFIG = {
    'server': 'localhost',  # o '.\SQLEXPRESS' para SQL Server Express
    'database': 'SENSORIUM',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': True,  # True para autenticación de Windows
}

# Si prefieres usar usuario y contraseña en lugar de Windows Authentication
# Descomenta estas líneas y comenta 'trusted_connection'
# DATABASE_CONFIG['user'] = 'tu_usuario'
# DATABASE_CONFIG['password'] = 'tu_contraseña'

# ========================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ========================================================================

APP_CONFIG = {
    'nombre': 'SENSORIUM',
    'version': '1.0.0',
    'autor': 'Kevin Alonso Osorio Martínez, Emiliano Soto Mojica, Ángel Leonardo Sánchez Maya',
    'descripcion': 'Sistema de Gestión para Consultorios Psicológicos'
}

# ========================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ========================================================================

SECURITY_CONFIG = {
    'hash_algorithm': 'sha256',  # Algoritmo para encriptar contraseñas
    'session_timeout': 3600,  # Tiempo de sesión en segundos (1 hora)
    'max_login_attempts': 3,  # Intentos máximos de login
}

# ========================================================================
# CONFIGURACIÓN DE LA INTERFAZ
# ========================================================================

UI_CONFIG = {
    'theme': 'clam',  # Tema de Tkinter
    'window_size': '1200x700',  # Tamaño de ventana por defecto
    'font_family': 'Arial',
    'font_size': 10,
    'colors': {
        'primary': '#2563eb',  # Azul
        'secondary': '#64748b',  # Gris
        'success': '#10b981',  # Verde
        'danger': '#ef4444',  # Rojo
        'warning': '#f59e0b',  # Amarillo
        'background': '#f8fafc',
        'text': '#1e293b'
    }
}

# ========================================================================
# CONFIGURACIÓN DE CITAS
# ========================================================================

CITAS_CONFIG = {
    'duracion_default': 60,  # Duración por defecto en minutos
    'horario_inicio': '08:00',  # Hora de inicio de atención
    'horario_fin': '20:00',  # Hora de fin de atención
    'intervalo_citas': 30,  # Intervalo entre citas en minutos
    'dias_anticipacion': 30,  # Días máximos de anticipación para agendar
    'modalidades': ['Presencial', 'Virtual'],
    'estados': ['Programada', 'Completada', 'Cancelada']
}

# ========================================================================
# CONFIGURACIÓN DE PAGOS
# ========================================================================

PAGOS_CONFIG = {
    'metodos_pago': ['Efectivo', 'Tarjeta', 'Transferencia'],
    'moneda': 'MXN',
    'monto_minimo': 100.00,
    'monto_maximo': 5000.00,
    'estados': ['Pendiente', 'Pagado', 'Cancelado']
}

# ========================================================================
# CONFIGURACIÓN DE NOTIFICACIONES
# ========================================================================

NOTIFICACIONES_CONFIG = {
    'recordatorio_dias_antes': 1,  # Días antes de la cita para recordatorio
    'recordatorio_horas_antes': 24,  # Horas antes para recordatorio
    'activar_email': False,  # Activar notificaciones por email
    'activar_sms': False  # Activar notificaciones por SMS
}

# ========================================================================
# CONFIGURACIÓN DE VALIDACIONES
# ========================================================================

VALIDACIONES = {
    'nombre_min_length': 3,
    'nombre_max_length': 40,
    'telefono_min_length': 10,
    'telefono_max_length': 15,
    'email_regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'cedula_min_length': 8,
    'cedula_max_length': 20,
    'password_min_length': 6
}

# ========================================================================
# RUTAS DE ARCHIVOS
# ========================================================================

import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATHS = {
    'base': BASE_DIR,
    'database': os.path.join(BASE_DIR, 'database'),
    'logs': os.path.join(BASE_DIR, 'logs'),
    'backups': os.path.join(BASE_DIR, 'backups'),
    'assets': os.path.join(BASE_DIR, 'assets'),
    'reports': os.path.join(BASE_DIR, 'reports')
}

# Crear carpetas si no existen
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)

# ========================================================================
# CONFIGURACIÓN DE LOGS
# ========================================================================

LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join(PATHS['logs'], 'sensorium.log'),
    'max_bytes': 10485760,  # 10MB
    'backup_count': 5
}

# ========================================================================
# MENSAJES DEL SISTEMA
# ========================================================================

MENSAJES = {
    'login': {
        'exito': 'Inicio de sesión exitoso',
        'error': 'Usuario o contraseña incorrectos',
        'bloqueado': 'Usuario bloqueado. Contacte al administrador'
    },
    'registro': {
        'exito': 'Registro exitoso',
        'error': 'Error al registrar',
        'duplicado': 'El registro ya existe'
    },
    'actualizacion': {
        'exito': 'Actualización exitosa',
        'error': 'Error al actualizar'
    },
    'eliminacion': {
        'exito': 'Eliminación exitosa',
        'error': 'Error al eliminar',
        'confirmacion': '¿Está seguro de eliminar este registro?'
    },
    'validacion': {
        'campos_vacios': 'Por favor complete todos los campos obligatorios',
        'formato_invalido': 'Formato de datos inválido',
        'fecha_invalida': 'La fecha seleccionada no es válida'
    }
}

# ========================================================================
# ROLES Y PERMISOS
# ========================================================================

ROLES = {
    'administrador': {
        'nombre': 'Administrador',
        'permisos': [
            'usuarios_crear', 'usuarios_editar', 'usuarios_eliminar', 'usuarios_ver',
            'pacientes_crear', 'pacientes_editar', 'pacientes_eliminar', 'pacientes_ver',
            'psicologos_crear', 'psicologos_editar', 'psicologos_eliminar', 'psicologos_ver',
            'citas_crear', 'citas_editar', 'citas_eliminar', 'citas_ver',
            'consultas_crear', 'consultas_editar', 'consultas_ver',
            'pagos_crear', 'pagos_editar', 'pagos_ver',
            'historial_ver', 'historial_editar',
            'reportes_ver', 'reportes_generar',
            'configuracion_acceder'
        ]
    },
    'psicologo': {
        'nombre': 'Psicólogo',
        'permisos': [
            'citas_ver',
            'consultas_crear', 'consultas_ver',
            'pacientes_ver',
            'historial_ver'
        ]
    }
}


# ========================================================================
# FUNCIÓN PARA OBTENER CONFIGURACIÓN
# ========================================================================

def get_config(seccion: str) -> dict:
    """
    Obtiene una sección de configuración
    Args:
        seccion: Nombre de la sección (DATABASE, APP, UI, etc.)
    Returns:
        dict: Diccionario con la configuración solicitada
    """
    configs = {
        'DATABASE': DATABASE_CONFIG,
        'APP': APP_CONFIG,
        'SECURITY': SECURITY_CONFIG,
        'UI': UI_CONFIG,
        'CITAS': CITAS_CONFIG,
        'PAGOS': PAGOS_CONFIG,
        'NOTIFICACIONES': NOTIFICACIONES_CONFIG,
        'VALIDACIONES': VALIDACIONES,
        'PATHS': PATHS,
        'LOGGING': LOGGING_CONFIG,
        'MENSAJES': MENSAJES,
        'ROLES': ROLES
    }
    
    return configs.get(seccion.upper(), {})


if __name__ == "__main__":
    # Mostrar configuración actual
    print("=" * 50)
    print("CONFIGURACIÓN DEL SISTEMA SENSORIUM")
    print("=" * 50)
    print(f"\nAplicación: {APP_CONFIG['nombre']} v{APP_CONFIG['version']}")
    print(f"Base de datos: {DATABASE_CONFIG['database']}")
    print(f"Servidor: {DATABASE_CONFIG['server']}")
    print(f"Driver: {DATABASE_CONFIG['driver']}")
    print("\nRutas configuradas:")
    for key, path in PATHS.items():
        print(f"  {key}: {path}")
    print("\n" + "=" * 50)