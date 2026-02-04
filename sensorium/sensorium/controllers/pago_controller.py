# ====================================================================================
# controllers/pago_controller.py
# ====================================================================================
"""
Controlador para gestionar pagos
"""

from config.database import db
from models.pago import Pago
from datetime import datetime

class PagoController:
    """Controlador para operaciones CRUD de pagos"""
    
    def __init__(self):
        self.db = db
    
    def crear_pago(self, pago: Pago) -> tuple:
        """Crea un nuevo pago en la base de datos"""
        try:
            es_valido, mensaje = pago.validar_datos()
            if not es_valido:
                return False, mensaje, None
            
            query = """
            INSERT INTO PAGOS (IDconsulta, monto, metodo, fecha_pago, estatus_pago)
            VALUES (?, ?, ?, ?, ?)
            """
            parametros = (
                pago.id_consulta,
                pago.monto,
                pago.metodo,
                pago.fecha_pago or datetime.now().date(),
                pago.estatus_pago
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Pago registrado exitosamente", id_insertado
            else:
                return False, "Error al registrar pago", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_pago_por_id(self, id_pago: int) -> Pago:
        """Obtiene un pago por su ID"""
        try:
            query = """
            SELECT p.*, pac.nombre, c.fecha
            FROM PAGOS p
            INNER JOIN CONSULTAS co ON p.IDconsulta = co.IDconsulta
            INNER JOIN CITAS c ON co.IDcita = c.IDcita
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            WHERE p.IDpago = ?
            """
            resultado = self.db.ejecutar_consulta_una(query, (id_pago,))
            
            if resultado:
                pago = Pago(
                    id_pago=resultado[0],
                    id_consulta=resultado[1],
                    monto=resultado[2],
                    metodo=resultado[3],
                    fecha_pago=resultado[4],
                    estatus_pago=resultado[5]
                )
                pago.nombre_paciente = resultado[6]
                pago.fecha_consulta = resultado[7]
                return pago
            return None
            
        except Exception as e:
            print(f"Error al obtener pago: {e}")
            return None
    
    def listar_pagos(self, estatus: str = None) -> list:
        """Lista todos los pagos o filtra por estatus"""
        try:
            query = """
            SELECT p.*, pac.nombre, c.fecha
            FROM PAGOS p
            INNER JOIN CONSULTAS co ON p.IDconsulta = co.IDconsulta
            INNER JOIN CITAS c ON co.IDcita = c.IDcita
            INNER JOIN PACIENTES pac ON c.IDpaciente = pac.IDpaciente
            WHERE 1=1
            """
            parametros = []
            
            if estatus:
                query += " AND p.estatus_pago = ?"
                parametros.append(estatus)
            
            query += " ORDER BY p.fecha_pago DESC"
            
            resultados = self.db.ejecutar_consulta(query, tuple(parametros) if parametros else None)
            
            pagos = []
            for resultado in resultados:
                pago = Pago(
                    id_pago=resultado[0],
                    id_consulta=resultado[1],
                    monto=resultado[2],
                    metodo=resultado[3],
                    fecha_pago=resultado[4],
                    estatus_pago=resultado[5]
                )
                pago.nombre_paciente = resultado[6]
                pago.fecha_consulta = resultado[7]
                pagos.append(pago)
            
            return pagos
            
        except Exception as e:
            print(f"Error al listar pagos: {e}")
            return []
    
    def actualizar_pago(self, pago: Pago) -> tuple:
        """Actualiza los datos de un pago"""
        try:
            es_valido, mensaje = pago.validar_datos()
            if not es_valido:
                return False, mensaje
            
            query = """
            UPDATE PAGOS 
            SET monto = ?, metodo = ?, fecha_pago = ?, estatus_pago = ?
            WHERE IDpago = ?
            """
            parametros = (
                pago.monto,
                pago.metodo,
                pago.fecha_pago,
                pago.estatus_pago,
                pago.id_pago
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Pago actualizado exitosamente"
            else:
                return False, "Error al actualizar pago"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def marcar_como_pagado(self, id_pago: int) -> tuple:
        """Marca un pago como completado"""
        try:
            query = """
            UPDATE PAGOS 
            SET estatus_pago = 'Pagado', fecha_pago = ?
            WHERE IDpago = ?
            """
            
            if self.db.ejecutar_query(query, (datetime.now().date(), id_pago)):
                return True, "Pago marcado como pagado"
            else:
                return False, "Error al marcar pago"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_pago(self, id_pago: int) -> tuple:
        """Elimina un pago"""
        try:
            query = "DELETE FROM PAGOS WHERE IDpago = ?"
            
            if self.db.ejecutar_query(query, (id_pago,)):
                return True, "Pago eliminado exitosamente"
            else:
                return False, "Error al eliminar pago"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_total_ingresos(self, fecha_inicio=None, fecha_fin=None) -> float:
        """Calcula el total de ingresos en un período"""
        try:
            query = """
            SELECT SUM(monto) FROM PAGOS 
            WHERE estatus_pago = 'Pagado'
            """
            parametros = []
            
            if fecha_inicio:
                query += " AND fecha_pago >= ?"
                parametros.append(fecha_inicio)
            
            if fecha_fin:
                query += " AND fecha_pago <= ?"
                parametros.append(fecha_fin)
            
            resultado = self.db.ejecutar_consulta_una(query, tuple(parametros) if parametros else None)
            return float(resultado[0]) if resultado and resultado[0] else 0.0
            
        except Exception as e:
            print(f"Error al calcular ingresos: {e}")
            return 0.0
