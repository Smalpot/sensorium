"""
Controlador para gestionar psicólogos
"""

from config.database import db
from models.psicologo import Psicologo

class PsicologoController:
    """Controlador para operaciones CRUD de psicólogos"""
    
    def __init__(self):
        self.db = db
    
    def crear_psicologo(self, psicologo: Psicologo) -> tuple:
        """
        Crea un nuevo psicólogo en la base de datos
        Args:
            psicologo: Objeto Psicologo con los datos
        Returns:
            tuple: (exito: bool, mensaje: str, id: int)
        """
        try:
            # Validar datos
            es_valido, mensaje = psicologo.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            query = """
            INSERT INTO PSICOLOGOS (IDusuario, especialidad, experiencia, cedula)
            VALUES (?, ?, ?, ?)
            """
            parametros = (
                psicologo.id_usuario,
                psicologo.especialidad,
                psicologo.experiencia,
                psicologo.cedula
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Psicólogo registrado exitosamente", id_insertado
            else:
                return False, "Error al registrar psicólogo", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_psicologo_por_id(self, id_psicologo: int) -> Psicologo:
        """
        Obtiene un psicólogo por su ID con datos del usuario
        Args:
            id_psicologo: ID del psicólogo
        Returns:
            Psicologo: Objeto Psicologo o None
        """
        try:
            query = """
            SELECT p.*, u.nombre, u.correo
            FROM PSICOLOGOS p
            INNER JOIN USUARIO u ON p.IDusuario = u.IDusuario
            WHERE p.IDpsicologo = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_psicologo,))
            
            if resultado:
                psicologo = Psicologo(
                    id_psicologo=resultado[0],
                    id_usuario=resultado[1],
                    especialidad=resultado[2],
                    experiencia=resultado[3],
                    cedula=resultado[4]
                )
                psicologo.nombre = resultado[5]
                psicologo.correo = resultado[6]
                return psicologo
            return None
            
        except Exception as e:
            print(f"Error al obtener psicólogo: {e}")
            return None
    
    def obtener_psicologo_por_usuario(self, id_usuario: int) -> Psicologo:
        """
        Obtiene un psicólogo por su ID de usuario
        Args:
            id_usuario: ID del usuario
        Returns:
            Psicologo: Objeto Psicologo o None
        """
        try:
            query = """
            SELECT p.*, u.nombre, u.correo
            FROM PSICOLOGOS p
            INNER JOIN USUARIO u ON p.IDusuario = u.IDusuario
            WHERE p.IDusuario = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_usuario,))
            
            if resultado:
                psicologo = Psicologo(
                    id_psicologo=resultado[0],
                    id_usuario=resultado[1],
                    especialidad=resultado[2],
                    experiencia=resultado[3],
                    cedula=resultado[4]
                )
                psicologo.nombre = resultado[5]
                psicologo.correo = resultado[6]
                return psicologo
            return None
            
        except Exception as e:
            print(f"Error al obtener psicólogo: {e}")
            return None
    
    def listar_psicologos(self, especialidad: str = None) -> list:
        """
        Lista todos los psicólogos o filtra por especialidad
        Args:
            especialidad: Especialidad a filtrar (opcional)
        Returns:
            list: Lista de objetos Psicologo
        """
        try:
            if especialidad:
                query = """
                SELECT p.*, u.nombre, u.correo
                FROM PSICOLOGOS p
                INNER JOIN USUARIO u ON p.IDusuario = u.IDusuario
                WHERE p.especialidad = ?
                ORDER BY u.nombre
                """
                resultados = self.db.ejecutar_consulta(query, (especialidad,))
            else:
                query = """
                SELECT p.*, u.nombre, u.correo
                FROM PSICOLOGOS p
                INNER JOIN USUARIO u ON p.IDusuario = u.IDusuario
                ORDER BY u.nombre
                """
                resultados = self.db.ejecutar_consulta(query)
            
            psicologos = []
            for resultado in resultados:
                psicologo = Psicologo(
                    id_psicologo=resultado[0],
                    id_usuario=resultado[1],
                    especialidad=resultado[2],
                    experiencia=resultado[3],
                    cedula=resultado[4]
                )
                psicologo.nombre = resultado[5]
                psicologo.correo = resultado[6]
                psicologos.append(psicologo)
            
            return psicologos
            
        except Exception as e:
            print(f"Error al listar psicólogos: {e}")
            return []
    
    def actualizar_psicologo(self, psicologo: Psicologo) -> tuple:
        """
        Actualiza los datos de un psicólogo
        Args:
            psicologo: Objeto Psicologo con los datos actualizados
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            # Validar datos
            es_valido, mensaje = psicologo.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE PSICOLOGOS 
            SET especialidad = ?, experiencia = ?, cedula = ?
            WHERE IDpsicologo = ?
            """
            parametros = (
                psicologo.especialidad,
                psicologo.experiencia,
                psicologo.cedula,
                psicologo.id_psicologo
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Psicólogo actualizado exitosamente"
            else:
                return False, "Error al actualizar psicólogo"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_psicologo(self, id_psicologo: int) -> tuple:
        """
        Elimina un psicólogo de la base de datos
        Args:
            id_psicologo: ID del psicólogo a eliminar
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "DELETE FROM PSICOLOGOS WHERE IDpsicologo = ?"
            
            if self.db.ejecutar_query(query, (id_psicologo,)):
                return True, "Psicólogo eliminado exitosamente"
            else:
                return False, "Error al eliminar psicólogo"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_especialidades(self) -> list:
        """
        Obtiene lista de especialidades únicas
        Returns:
            list: Lista de especialidades
        """
        try:
            query = "SELECT DISTINCT especialidad FROM PSICOLOGOS ORDER BY especialidad"
            resultados = self.db.ejecutar_consulta(query)
            return [r[0] for r in resultados]
            
        except Exception as e:
            print(f"Error al obtener especialidades: {e}")
            return []
    
    def contar_psicologos(self) -> int:
        """
        Cuenta el número total de psicólogos
        Returns:
            int: Número de psicólogos
        """
        try:
            query = "SELECT COUNT(*) FROM PSICOLOGOS"
            resultado = self.db.ejecutar_consulta_una(query)
            return resultado[0] if resultado else 0
            
        except Exception as e:
            print(f"Error al contar psicólogos: {e}")
            return 0
    
    def buscar_por_cedula(self, cedula: str) -> Psicologo:
        """
        Busca un psicólogo por su cédula profesional
        Args:
            cedula: Cédula profesional
        Returns:
            Psicologo: Objeto Psicologo o None
        """
        try:
            query = """
            SELECT p.*, u.nombre, u.correo
            FROM PSICOLOGOS p
            INNER JOIN USUARIO u ON p.IDusuario = u.IDusuario
            WHERE p.cedula = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (cedula,))
            
            if resultado:
                psicologo = Psicologo(
                    id_psicologo=resultado[0],
                    id_usuario=resultado[1],
                    especialidad=resultado[2],
                    experiencia=resultado[3],
                    cedula=resultado[4]
                )
                psicologo.nombre = resultado[5]
                psicologo.correo = resultado[6]
                return psicologo
            return None
            
        except Exception as e:
            print(f"Error al buscar psicólogo: {e}")
            return None