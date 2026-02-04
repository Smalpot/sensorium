"""
Script para inicializar la base de datos SENSORIUM en SQL Server
Ejecuta el script SQL y crea todas las tablas necesarias
"""

import pyodbc
import os
from config.settings import DATABASE_CONFIG, PATHS

def leer_script_sql():
    """Lee el archivo init_db.sql"""
    script_path = os.path.join(PATHS['database'], 'init_db.sql')
    
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo {script_path}")
        return None
    except Exception as e:
        print(f"✗ Error al leer el script SQL: {e}")
        return None

def conectar_servidor():
    """
    Conecta al servidor SQL Server (sin especificar base de datos)
    para poder crear la base de datos si no existe
    """
    try:
        connection_string = (
            f"DRIVER={DATABASE_CONFIG['driver']};"
            f"SERVER={DATABASE_CONFIG['server']};"
            f"Trusted_Connection=yes;"
        )
        
        conexion = pyodbc.connect(connection_string, autocommit=True)
        print("✓ Conexión exitosa al servidor SQL Server")
        return conexion
    
    except pyodbc.Error as e:
        print(f"✗ Error al conectar con SQL Server: {e}")
        print("\nVerifica que:")
        print("1. SQL Server Express esté instalado")
        print("2. El servicio SQL Server esté corriendo")
        print("3. El driver ODBC Driver 17 esté instalado")
        return None

def ejecutar_script_sql(conexion, script):
    """
    Ejecuta el script SQL para crear la base de datos y tablas
    """
    try:
        cursor = conexion.cursor()
        
        # Dividir el script en comandos individuales usando GO
        comandos = script.split('GO')
        
        total_comandos = len([c for c in comandos if c.strip()])
        comandos_ejecutados = 0
        
        print(f"\nEjecutando {total_comandos} comandos SQL...")
        print("-" * 50)
        
        for comando in comandos:
            comando = comando.strip()
            if comando:
                try:
                    cursor.execute(comando)
                    comandos_ejecutados += 1
                except pyodbc.Error as e:
                    # Ignorar algunos errores comunes que no son críticos
                    if "already exists" not in str(e).lower():
                        print(f"⚠ Advertencia en comando: {str(e)[:100]}")
        
        print("-" * 50)
        print(f"✓ {comandos_ejecutados}/{total_comandos} comandos ejecutados correctamente")
        
        cursor.close()
        return True
    
    except Exception as e:
        print(f"✗ Error al ejecutar script SQL: {e}")
        return False

def verificar_tablas(conexion):
    """Verifica que todas las tablas se hayan creado correctamente"""
    tablas_esperadas = [
        'USUARIO',
        'PSICOLOGOS',
        'PACIENTES',
        'CITAS',
        'CONSULTAS',
        'PAGOS',
        'HISTORIAL'
    ]
    
    try:
        cursor = conexion.cursor()
        
        # Cambiar a la base de datos SENSORIUM
        cursor.execute(f"USE {DATABASE_CONFIG['database']}")
        
        print("\nVerificando tablas creadas:")
        print("-" * 50)
        
        tablas_creadas = []
        for tabla in tablas_esperadas:
            query = f"""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = '{tabla}'
            """
            cursor.execute(query)
            resultado = cursor.fetchone()
            
            if resultado and resultado[0] > 0:
                print(f"✓ Tabla {tabla} existe")
                tablas_creadas.append(tabla)
            else:
                print(f"✗ Tabla {tabla} NO existe")
        
        cursor.close()
        
        print("-" * 50)
        print(f"Tablas creadas: {len(tablas_creadas)}/{len(tablas_esperadas)}")
        
        return len(tablas_creadas) == len(tablas_esperadas)
    
    except Exception as e:
        print(f"✗ Error al verificar tablas: {e}")
        return False

def verificar_usuario_admin(conexion):
    """Verifica que el usuario administrador se haya creado"""
    try:
        cursor = conexion.cursor()
        cursor.execute(f"USE {DATABASE_CONFIG['database']}")
        
        query = "SELECT COUNT(*) FROM USUARIO WHERE rol = 'administrador'"
        cursor.execute(query)
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] > 0:
            print("\n✓ Usuario administrador creado correctamente")
            print("   Usuario: admin@sensorium.com")
            print("   Contraseña: admin123")
            return True
        else:
            print("\n⚠ No se encontró el usuario administrador")
            return False
    
    except Exception as e:
        print(f"✗ Error al verificar usuario administrador: {e}")
        return False

def inicializar_base_datos():
    """
    Función principal que inicializa la base de datos completa
    """
    print("=" * 60)
    print("INICIALIZACIÓN DE BASE DE DATOS SENSORIUM")
    print("=" * 60)
    
    # Paso 1: Leer el script SQL
    print("\n1. Leyendo script SQL...")
    script = leer_script_sql()
    if not script:
        return False
    print("✓ Script SQL cargado correctamente")
    
    # Paso 2: Conectar al servidor
    print("\n2. Conectando al servidor SQL Server...")
    conexion = conectar_servidor()
    if not conexion:
        return False
    
    # Paso 3: Ejecutar el script
    print("\n3. Ejecutando script de inicialización...")
    if not ejecutar_script_sql(conexion, script):
        conexion.close()
        return False
    
    # Paso 4: Verificar que todo se creó correctamente
    print("\n4. Verificando instalación...")
    tablas_ok = verificar_tablas(conexion)
    admin_ok = verificar_usuario_admin(conexion)
    
    # Cerrar conexión
    conexion.close()
    
    # Resultado final
    print("\n" + "=" * 60)
    if tablas_ok and admin_ok:
        print("✓ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("=" * 60)
        print("\n¡La base de datos SENSORIUM está lista para usar!")
        print("\nPuedes iniciar sesión con:")
        print("  Usuario: admin@sensorium.com")
        print("  Contraseña: admin123")
        print("\n⚠ IMPORTANTE: Cambia la contraseña del administrador")
        return True
    else:
        print("✗ HUBO PROBLEMAS EN LA INICIALIZACIÓN")
        print("=" * 60)
        print("\nRevisa los mensajes de error anteriores")
        return False

def main():
    """Punto de entrada del script"""
    try:
        exito = inicializar_base_datos()
        
        if exito:
            print("\n✓ Proceso completado exitosamente")
            input("\nPresiona Enter para salir...")
            return 0
        else:
            print("\n✗ El proceso falló")
            input("\nPresiona Enter para salir...")
            return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠ Proceso cancelado por el usuario")
        return 1
    
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit(main())