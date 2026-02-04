# ====================================================================================
# controllers/historial_controller.py
# ====================================================================================
"""
Controlador para gestionar historiales clínicos
"""

from config.database import db
from models.historial import Historial
from datetime import datetime

class HistorialController:
    """Controlador para operaciones CRUD de historiales"""
    
    def __init__(self):
        self.db = db
    
    def crear_historial(self, historial: Historial) -> tuple:
        """Crea un nuevo historial clínico"""
        try:
            es_valido, mensaje = historial.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            query = """
            INSERT INTO HISTORIAL (IDpaciente, antecedentes, alergias, tratamientos, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
            """
            parametros = (
                historial.id_paciente,
                historial.antecedentes,
                historial.alergias,
                historial.tratamientos,
                historial.fecha_creacion or datetime.now().date()
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Historial creado exitosamente", id_insertado
            else:
                return False, "Error al crear historial", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_historial_por_paciente(self, id_paciente: int) -> Historial:
        """Obtiene el historial de un paciente"""
        try:
            query = """
            SELECT h.*, p.nombre
            FROM HISTORIAL h
            INNER JOIN PACIENTES p ON h.IDpaciente = p.IDpaciente
            WHERE h.IDpaciente = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_paciente,))
            
            if resultado:
                historial = Historial(
                    id_historial=resultado[0],
                    id_paciente=resultado[1],
                    antecedentes=resultado[2],
                    alergias=resultado[3],
                    tratamientos=resultado[4],
                    fecha_creacion=resultado[5]
                )
                historial.nombre_paciente = resultado[6]
                return historial
            return None
            
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return None
    
    def actualizar_historial(self, historial: Historial) -> tuple:
        """Actualiza el historial de un paciente"""
        try:
            es_valido, mensaje = historial.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE HISTORIAL 
            SET antecedentes = ?, alergias = ?, tratamientos = ?
            WHERE IDhistorial = ?
            """
            parametros = (
                historial.antecedentes,
                historial.alergias,
                historial.tratamientos,
                historial.id_historial
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Historial actualizado exitosamente"
            else:
                return False, "Error al actualizar historial"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_historial(self, id_historial: int) -> tuple:
        """Elimina un historial"""
        try:
            query = "DELETE FROM HISTORIAL WHERE IDhistorial = ?"
            
            if self.db.ejecutar_query(query, (id_historial,)):
                return True, "Historial eliminado exitosamente"
            else:
                return False, "Error al eliminar historial"
                
        except Exception as e:
            return False, f"Error: {str(e)}"