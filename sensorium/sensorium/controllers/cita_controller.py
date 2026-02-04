"""
Controlador para gestionar citas
"""

from config.database import db
from models.cita import Cita
from datetime import datetime, date

class CitaController:
    """Controlador para operaciones CRUD de citas"""
    
    def __init__(self):
        self.db = db
    
    def crear_cita(self, cita: Cita) -> tuple:
        """
        Crea una nueva cita en la base de datos
        Args:
            cita: Objeto Cita con los datos
        Returns:
            tuple: (exito: bool, mensaje: str, id: int)
        """
        try:
            # Validar datos
            es_valido, mensaje = cita.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            # Verificar disponibilidad
            if not self.verificar_disponibilidad(cita.id_psicologo, cita.fecha, cita.hora):
                return False, "El psicólogo no está disponible en ese horario", None
            
            query = """
            INSERT INTO CITAS (IDpaciente, IDpsicologo, fecha, hora, modalidad, estado)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            parametros = (
                cita.id_paciente,
                cita.id_psicologo,
                cita.fecha,
                cita.hora,
                cita.modalidad,
                cita.estado
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Cita programada exitosamente", id_insertado
            else:
                return False, "Error al programar cita", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_cita_por_id(self, id_cita: int) -> Cita:
        """
        Obtiene una cita por su ID con datos completos
        Args:
            id_cita: ID de la cita
        Returns:
            Cita: Objeto Cita o None
        """
        try:
            query = """
            SELECT c.*, pac.nombre, u.nombre, ps.especialidad
            FROM CITAS c
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
            INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
            WHERE c.IDcita = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_cita,))
            
            if resultado:
                cita = Cita(
                    id_cita=resultado[0],
                    id_paciente=resultado[1],
                    id_psicologo=resultado[2],
                    fecha=resultado[3],
                    hora=resultado[4],
                    modalidad=resultado[5],
                    estado=resultado[6]
                )
                cita.nombre_paciente = resultado[7]
                cita.nombre_psicologo = resultado[8]
                cita.especialidad = resultado[9]
                return cita
            return None
            
        except Exception as e:
            print(f"Error al obtener cita: {e}")
            return None
    
    def listar_citas(self, fecha_inicio: date = None, fecha_fin: date = None, 
                     id_paciente: int = None, id_psicologo: int = None,
                     estado: str = None) -> list:
        """
        Lista citas con diversos filtros
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            id_paciente: Filtrar por paciente
            id_psicologo: Filtrar por psicólogo
            estado: Filtrar por estado
        Returns:
            list: Lista de objetos Cita
        """
        try:
            query = """
            SELECT c.*, pac.nombre, u.nombre, ps.especialidad
            FROM CITAS c
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
            INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
            WHERE 1=1
            """
            parametros = []
            
            if fecha_inicio:
                query += " AND c.fecha >= ?"
                parametros.append(fecha_inicio)
            
            if fecha_fin:
                query += " AND c.fecha <= ?"
                parametros.append(fecha_fin)
            
            if id_paciente:
                query += " AND c.IDpaciente = ?"
                parametros.append(id_paciente)
            
            if id_psicologo:
                query += " AND c.IDpsicologo = ?"
                parametros.append(id_psicologo)
            
            if estado:
                query += " AND c.estado = ?"
                parametros.append(estado)
            
            query += " ORDER BY c.fecha DESC, c.hora DESC"
            
            resultados = self.db.ejecutar_consulta(query, tuple(parametros) if parametros else None)
            
            citas = []
            for resultado in resultados:
                cita = Cita(
                    id_cita=resultado[0],
                    id_paciente=resultado[1],
                    id_psicologo=resultado[2],
                    fecha=resultado[3],
                    hora=resultado[4],
                    modalidad=resultado[5],
                    estado=resultado[6]
                )
                cita.nombre_paciente = resultado[7]
                cita.nombre_psicologo = resultado[8]
                cita.especialidad = resultado[9]
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            print(f"Error al listar citas: {e}")
            return []
    
    def actualizar_cita(self, cita: Cita) -> tuple:
        """
        Actualiza los datos de una cita
        Args:
            cita: Objeto Cita con los datos actualizados
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            # Validar datos
            es_valido, mensaje = cita.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE CITAS 
            SET IDpaciente = ?, IDpsicologo = ?, fecha = ?, 
                hora = ?, modalidad = ?, estado = ?
            WHERE IDcita = ?
            """
            parametros = (
                cita.id_paciente,
                cita.id_psicologo,
                cita.fecha,
                cita.hora,
                cita.modalidad,
                cita.estado,
                cita.id_cita
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Cita actualizada exitosamente"
            else:
                return False, "Error al actualizar cita"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cancelar_cita(self, id_cita: int) -> tuple:
        """
        Cancela una cita (cambia estado a Cancelada)
        Args:
            id_cita: ID de la cita
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "UPDATE CITAS SET estado = 'Cancelada' WHERE IDcita = ?"
            
            if self.db.ejecutar_query(query, (id_cita,)):
                return True, "Cita cancelada exitosamente"
            else:
                return False, "Error al cancelar cita"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def completar_cita(self, id_cita: int) -> tuple:
        """
        Marca una cita como completada
        Args:
            id_cita: ID de la cita
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "UPDATE CITAS SET estado = 'Completada' WHERE IDcita = ?"
            
            if self.db.ejecutar_query(query, (id_cita,)):
                return True, "Cita marcada como completada"
            else:
                return False, "Error al completar cita"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_cita(self, id_cita: int) -> tuple:
        """
        Elimina una cita de la base de datos
        Args:
            id_cita: ID de la cita a eliminar
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "DELETE FROM CITAS WHERE IDcita = ?"
            
            if self.db.ejecutar_query(query, (id_cita,)):
                return True, "Cita eliminada exitosamente"
            else:
                return False, "Error al eliminar cita"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def verificar_disponibilidad(self, id_psicologo: int, fecha: date, hora) -> bool:
        """
        Verifica si un psicólogo está disponible en una fecha y hora
        Args:
            id_psicologo: ID del psicólogo
            fecha: Fecha de la cita
            hora: Hora de la cita
        Returns:
            bool: True si está disponible
        """
        try:
            query = """
            SELECT COUNT(*) FROM CITAS 
            WHERE IDpsicologo = ? AND fecha = ? AND hora = ? 
            AND estado != 'Cancelada'
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_psicologo, fecha, hora))
            return resultado[0] == 0 if resultado else True
            
        except Exception as e:
            print(f"Error al verificar disponibilidad: {e}")
            return False
    
    def obtener_citas_del_dia(self, fecha: date = None) -> list:
        """
        Obtiene las citas de un día específico
        Args:
            fecha: Fecha (por defecto hoy)
        Returns:
            list: Lista de citas
        """
        if not fecha:
            fecha = datetime.now().date()
        
        return self.listar_citas(fecha_inicio=fecha, fecha_fin=fecha)
    
    def contar_citas(self, estado: str = None) -> int:
        """
        Cuenta el número de citas
        Args:
            estado: Filtrar por estado (opcional)
        Returns:
            int: Número de citas
        """
        try:
            if estado:
                query = "SELECT COUNT(*) FROM CITAS WHERE estado = ?"
                resultado = self.db.ejecutar_consulta_una(query, (estado,))
            else:
                query = "SELECT COUNT(*) FROM CITAS"
                resultado = self.db.ejecutar_consulta_una(query)
            
            return resultado[0] if resultado else 0
            
        except Exception as e:
            print(f"Error al contar citas: {e}")
            return 0