"""
Controlador para gestionar pacientes
"""

from config.database import db
from models.paciente import Paciente
from datetime import datetime

class PacienteController:
    """Controlador para operaciones CRUD de pacientes"""
    
    def __init__(self):
        self.db = db
    
    def crear_paciente(self, paciente: Paciente) -> tuple:
        """
        Crea un nuevo paciente en la base de datos
        Args:
            paciente: Objeto Paciente con los datos
        Returns:
            tuple: (exito: bool, mensaje: str, id: int)
        """
        try:
            # Validar datos
            es_valido, mensaje = paciente.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            query = """
            INSERT INTO PACIENTES (nombre, correo, telefono, direccion, fecha_regist)
            VALUES (?, ?, ?, ?, ?)
            """
            parametros = (
                paciente.nombre,
                paciente.correo,
                paciente.telefono,
                paciente.direccion,
                paciente.fecha_regist or datetime.now().date()
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Paciente registrado exitosamente", id_insertado
            else:
                return False, "Error al registrar paciente", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_paciente_por_id(self, id_paciente: int) -> Paciente:
        """
        Obtiene un paciente por su ID
        Args:
            id_paciente: ID del paciente
        Returns:
            Paciente: Objeto Paciente o None
        """
        try:
            query = "SELECT * FROM PACIENTES WHERE IDpaciente = ?"
            resultado = self.db.ejecutar_consulta_una(query, (id_paciente,))
            
            if resultado:
                return Paciente(
                    id_paciente=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    telefono=resultado[3],
                    direccion=resultado[4],
                    fecha_regist=resultado[5]
                )
            return None
            
        except Exception as e:
            print(f"Error al obtener paciente: {e}")
            return None
    
    def listar_pacientes(self, buscar: str = None) -> list:
        """
        Lista todos los pacientes o busca por nombre
        Args:
            buscar: Texto para buscar en nombre (opcional)
        Returns:
            list: Lista de objetos Paciente
        """
        try:
            if buscar:
                query = """
                SELECT * FROM PACIENTES 
                WHERE nombre LIKE ? OR telefono LIKE ?
                ORDER BY nombre
                """
                parametro = f"%{buscar}%"
                resultados = self.db.ejecutar_consulta(query, (parametro, parametro))
            else:
                query = "SELECT * FROM PACIENTES ORDER BY nombre"
                resultados = self.db.ejecutar_consulta(query)
            
            pacientes = []
            for resultado in resultados:
                pacientes.append(Paciente(
                    id_paciente=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    telefono=resultado[3],
                    direccion=resultado[4],
                    fecha_regist=resultado[5]
                ))
            
            return pacientes
            
        except Exception as e:
            print(f"Error al listar pacientes: {e}")
            return []
    
    def actualizar_paciente(self, paciente: Paciente) -> tuple:
        """
        Actualiza los datos de un paciente
        Args:
            paciente: Objeto Paciente con los datos actualizados
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            # Validar datos
            es_valido, mensaje = paciente.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE PACIENTES 
            SET nombre = ?, correo = ?, telefono = ?, direccion = ?
            WHERE IDpaciente = ?
            """
            parametros = (
                paciente.nombre,
                paciente.correo,
                paciente.telefono,
                paciente.direccion,
                paciente.id_paciente
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Paciente actualizado exitosamente"
            else:
                return False, "Error al actualizar paciente"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_paciente(self, id_paciente: int) -> tuple:
        """
        Elimina un paciente de la base de datos
        Args:
            id_paciente: ID del paciente a eliminar
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "DELETE FROM PACIENTES WHERE IDpaciente = ?"
            
            if self.db.ejecutar_query(query, (id_paciente,)):
                return True, "Paciente eliminado exitosamente"
            else:
                return False, "Error al eliminar paciente"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def contar_pacientes(self) -> int:
        """
        Cuenta el número total de pacientes
        Returns:
            int: Número de pacientes
        """
        try:
            query = "SELECT COUNT(*) FROM PACIENTES"
            resultado = self.db.ejecutar_consulta_una(query)
            return resultado[0] if resultado else 0
            
        except Exception as e:
            print(f"Error al contar pacientes: {e}")
            return 0
    
    def obtener_pacientes_recientes(self, limite: int = 10) -> list:
        """
        Obtiene los pacientes más recientes
        Args:
            limite: Número máximo de pacientes a retornar
        Returns:
            list: Lista de objetos Paciente
        """
        try:
            query = """
            SELECT TOP (?) * FROM PACIENTES 
            ORDER BY fecha_regist DESC
            """
            resultados = self.db.ejecutar_consulta(query, (limite,))
            
            pacientes = []
            for resultado in resultados:
                pacientes.append(Paciente(
                    id_paciente=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    telefono=resultado[3],
                    direccion=resultado[4],
                    fecha_regist=resultado[5]
                ))
            
            return pacientes
            
        except Exception as e:
            print(f"Error al obtener pacientes recientes: {e}")
            return []
    
    def buscar_por_telefono(self, telefono: str) -> Paciente:
        """
        Busca un paciente por su teléfono
        Args:
            telefono: Número de teléfono
        Returns:
            Paciente: Objeto Paciente o None
        """
        try:
            query = "SELECT * FROM PACIENTES WHERE telefono = ?"
            resultado = self.db.ejecutar_consulta_una(query, (telefono,))
            
            if resultado:
                return Paciente(
                    id_paciente=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    telefono=resultado[3],
                    direccion=resultado[4],
                    fecha_regist=resultado[5]
                )
            return None
            
        except Exception as e:
            print(f"Error al buscar paciente: {e}")
            return None