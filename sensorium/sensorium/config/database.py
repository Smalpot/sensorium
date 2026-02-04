"""
Módulo de configuración de la base de datos SQL Server
Maneja la conexión y operaciones básicas con la base de datos
"""

import pyodbc # pyright: ignore[reportMissingImports]
from typing import Optional, List, Tuple, Any

class Database:
    """
    Clase para manejar la conexión con SQL Server
    """
    
    # Configuración de conexión
    SERVER = 'localhost'  # o '.\SQLEXPRESS' si usas la instancia por defecto
    DATABASE = 'SENSORIUM'
    DRIVER = '{ODBC Driver 17 for SQL Server}'  # Driver más común
    
    def __init__(self):
        """Inicializa la clase sin conexión activa"""
        self.connection = None
        self.cursor = None
    
    def conectar(self) -> bool:
        """
        Establece conexión con SQL Server usando autenticación de Windows
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            connection_string = (
                f'DRIVER={self.DRIVER};'
                f'SERVER={self.SERVER};'
                f'DATABASE={self.DATABASE};'
                f'Trusted_Connection=yes;'  # Autenticación de Windows
            )
            
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("✓ Conexión exitosa a SQL Server")
            return True
            
        except pyodbc.Error as e:
            print(f"✗ Error al conectar con SQL Server: {e}")
            return False
    
    def conectar_con_credenciales(self, usuario: str, contraseña: str) -> bool:
        """
        Establece conexión con SQL Server usando usuario y contraseña
        Args:
            usuario: Nombre de usuario de SQL Server
            contraseña: Contraseña del usuario
        Returns:
            bool: True si la conexión fue exitosa
        """
        try:
            connection_string = (
                f'DRIVER={self.DRIVER};'
                f'SERVER={self.SERVER};'
                f'DATABASE={self.DATABASE};'
                f'UID={usuario};'
                f'PWD={contraseña};'
            )
            
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("✓ Conexión exitosa a SQL Server")
            return True
            
        except pyodbc.Error as e:
            print(f"✗ Error al conectar: {e}")
            return False
    
    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("✓ Conexión cerrada")
        except Exception as e:
            print(f"✗ Error al cerrar conexión: {e}")
    
    def ejecutar_query(self, query: str, parametros: Optional[Tuple] = None) -> bool:
        """
        Ejecuta una query que modifica datos (INSERT, UPDATE, DELETE)
        Args:
            query: Consulta SQL a ejecutar
            parametros: Tupla con los parámetros de la query
        Returns:
            bool: True si se ejecutó correctamente
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return True
            
        except pyodbc.Error as e:
            print(f"✗ Error al ejecutar query: {e}")
            self.connection.rollback()
            return False
    
    def ejecutar_consulta(self, query: str, parametros: Optional[Tuple] = None) -> List[Tuple]:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        Args:
            query: Consulta SQL SELECT
            parametros: Tupla con los parámetros de la query
        Returns:
            List[Tuple]: Lista de tuplas con los resultados
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            resultados = self.cursor.fetchall()
            return resultados
            
        except pyodbc.Error as e:
            print(f"✗ Error al ejecutar consulta: {e}")
            return []
    
    def ejecutar_consulta_una(self, query: str, parametros: Optional[Tuple] = None) -> Optional[Tuple]:
        """
        Ejecuta una consulta SELECT y retorna solo el primer resultado
        Args:
            query: Consulta SQL SELECT
            parametros: Tupla con los parámetros de la query
        Returns:
            Optional[Tuple]: Primera fila del resultado o None
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            resultado = self.cursor.fetchone()
            return resultado
            
        except pyodbc.Error as e:
            print(f"✗ Error al ejecutar consulta: {e}")
            return None
    
    def obtener_ultimo_id(self) -> Optional[int]:
        """
        Obtiene el último ID insertado (IDENTITY)
        Returns:
            Optional[int]: Último ID generado o None
        """
        try:
            self.cursor.execute("SELECT @@IDENTITY")
            resultado = self.cursor.fetchone()
            return int(resultado[0]) if resultado else None
        except Exception as e:
            print(f"✗ Error al obtener último ID: {e}")
            return None
    
    def tabla_existe(self, nombre_tabla: str) -> bool:
        """
        Verifica si una tabla existe en la base de datos
        Args:
            nombre_tabla: Nombre de la tabla a verificar
        Returns:
            bool: True si la tabla existe
        """
        query = """
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = ?
        """
        resultado = self.ejecutar_consulta_una(query, (nombre_tabla,))
        return resultado and resultado[0] > 0
    
    def __enter__(self):
        """Permite usar la clase con context manager (with)"""
        self.conectar()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión automáticamente al salir del context manager"""
        self.desconectar()


# Instancia global de la base de datos (Singleton)
db = Database()


# Función auxiliar para testing
def probar_conexion():
    """Prueba la conexión con la base de datos"""
    print("Probando conexión con SQL Server...")
    db_test = Database()
    
    if db_test.conectar():
        print("✓ Conexión establecida correctamente")
        
        # Prueba consulta simple
        resultado = db_test.ejecutar_consulta_una("SELECT @@VERSION")
        if resultado:
            print(f"✓ Versión de SQL Server detectada")
        
        db_test.desconectar()
        return True
    else:
        print("✗ No se pudo conectar a SQL Server")
        print("\nVerifica que:")
        print("1. SQL Server Express esté instalado")
        print("2. El servicio SQL Server esté corriendo")
        print("3. El driver ODBC Driver 17 esté instalado")
        return False


if __name__ == "__main__":
    # Ejecutar prueba de conexión
    probar_conexion()