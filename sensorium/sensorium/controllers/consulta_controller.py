# ====================================================================================
# controllers/consulta_controller.py
# ====================================================================================
"""
Controlador para gestionar consultas
"""

from config.database import db
from models.consulta import Consulta

class ConsultaController:
    """Controlador para operaciones CRUD de consultas"""
    
    def __init__(self):
        self.db = db
    
    def crear_consulta(self, consulta: Consulta) -> tuple:
        """
        Crea una nueva consulta en la base de datos
        Args:
            consulta: Objeto Consulta con los datos
        Returns:
            tuple: (exito: bool, mensaje: str, id: int)
        """
        try:
            # Validar datos
            es_valido, mensaje = consulta.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            query = """
            INSERT INTO CONSULTAS (IDcita, notas, duracion, diagnostico, recomend)
            VALUES (?, ?, ?, ?, ?)
            """
            parametros = (
                consulta.id_cita,
                consulta.notas,
                consulta.duracion,
                consulta.diagnostico,
                consulta.recomend
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Consulta registrada exitosamente", id_insertado
            else:
                return False, "Error al registrar consulta", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_consulta_por_id(self, id_consulta: int) -> Consulta:
        """
        Obtiene una consulta por su ID con datos completos
        """
        try:
            query = """
            SELECT co.*, c.fecha, pac.nombre, u.nombre
            FROM CONSULTAS co
            INNER JOIN CITAS c ON co.IDcita = c.IDcita
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
            INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
            WHERE co.IDconsulta = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_consulta,))
            
            if resultado:
                consulta = Consulta(
                    id_consulta=resultado[0],
                    id_cita=resultado[1],
                    notas=resultado[2],
                    duracion=resultado[3],
                    diagnostico=resultado[4],
                    recomend=resultado[5]
                )
                consulta.fecha_cita = resultado[6]
                consulta.nombre_paciente = resultado[7]
                consulta.nombre_psicologo = resultado[8]
                return consulta
            return None
            
        except Exception as e:
            print(f"Error al obtener consulta: {e}")
            return None
    
    def obtener_consulta_por_cita(self, id_cita: int) -> Consulta:
        """Obtiene la consulta asociada a una cita"""
        try:
            query = """
            SELECT co.*, c.fecha, pac.nombre, u.nombre
            FROM CONSULTAS co
            INNER JOIN CITAS c ON co.IDcita = c.IDcita
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
            INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
            WHERE co.IDcita = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_cita,))
            
            if resultado:
                consulta = Consulta(
                    id_consulta=resultado[0],
                    id_cita=resultado[1],
                    notas=resultado[2],
                    duracion=resultado[3],
                    diagnostico=resultado[4],
                    recomend=resultado[5]
                )
                consulta.fecha_cita = resultado[6]
                consulta.nombre_paciente = resultado[7]
                consulta.nombre_psicologo = resultado[8]
                return consulta
            return None
            
        except Exception as e:
            print(f"Error al obtener consulta: {e}")
            return None
    
    def listar_consultas(self, id_paciente: int = None, id_psicologo: int = None) -> list:
        """Lista todas las consultas o filtra por paciente/psicólogo"""
        try:
            query = """
            SELECT co.*, c.fecha, pac.nombre, u.nombre
            FROM CONSULTAS co
            INNER JOIN CITAS c ON co.IDcita = c.IDcita
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
            INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
            WHERE 1=1
            """
            parametros = []
            
            if id_paciente:
                query += " AND c.IDpaciente = ?"
                parametros.append(id_paciente)
            
            if id_psicologo:
                query += " AND c.IDpsicologo = ?"
                parametros.append(id_psicologo)
            
            query += " ORDER BY c.fecha DESC"
            
            resultados = self.db.ejecutar_consulta(query, tuple(parametros) if parametros else None)
            
            consultas = []
            for resultado in resultados:
                consulta = Consulta(
                    id_consulta=resultado[0],
                    id_cita=resultado[1],
                    notas=resultado[2],
                    duracion=resultado[3],
                    diagnostico=resultado[4],
                    recomend=resultado[5]
                )
                consulta.fecha_cita = resultado[6]
                consulta.nombre_paciente = resultado[7]
                consulta.nombre_psicologo = resultado[8]
                consultas.append(consulta)
            
            return consultas
            
        except Exception as e:
            print(f"Error al listar consultas: {e}")
            return []
    
    def actualizar_consulta(self, consulta: Consulta) -> tuple:
        """Actualiza los datos de una consulta"""
        try:
            es_valido, mensaje = consulta.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE CONSULTAS 
            SET notas = ?, duracion = ?, diagnostico = ?, recomend = ?
            WHERE IDconsulta = ?
            """
            parametros = (
                consulta.notas,
                consulta.duracion,
                consulta.diagnostico,
                consulta.recomend,
                consulta.id_consulta
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Consulta actualizada exitosamente"
            else:
                return False, "Error al actualizar consulta"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_consulta(self, id_consulta: int) -> tuple:
        """Elimina una consulta"""
        try:
            query = "DELETE FROM CONSULTAS WHERE IDconsulta = ?"
            
            if self.db.ejecutar_query(query, (id_consulta,)):
                return True, "Consulta eliminada exitosamente"
            else:
                return False, "Error al eliminar consulta"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def contar_consultas(self) -> int:
        """Cuenta el número total de consultas"""
        try:
            query = "SELECT COUNT(*) FROM CONSULTAS"
            resultado = self.db.ejecutar_consulta_una(query)
            return resultado[0] if resultado else 0
            
        except Exception as e:
            print(f"Error al contar consultas: {e}")
            return 0

