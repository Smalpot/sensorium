from datetime import datetime
from decimal import Decimal

class Pago:
    """
    Clase que representa un pago realizado por una consulta
    """
    def __init__(self, id_pago=None, id_consulta=None, monto=None,
                 metodo=None, fecha_pago=None, estatus_pago="Pendiente"):
        self.id_pago = id_pago
        self.id_consulta = id_consulta  # Foreign Key a Consulta
        self.monto = monto
        self.metodo = metodo  # 'Efectivo', 'Tarjeta', 'Transferencia'
        self.fecha_pago = fecha_pago or datetime.now().date()
        self.estatus_pago = estatus_pago  # 'Pendiente', 'Pagado', 'Cancelado'
        
        # Datos relacionados (se llenan al consultar)
        self.nombre_paciente = None
        self.fecha_consulta = None
    
    def validar_datos(self):
        """Valida que los datos del pago sean correctos"""
        if not self.id_consulta:
            return False, "Debe asociarse a una consulta"
        
        if not self.monto or self.monto <= 0:
            return False, "El monto debe ser mayor a 0"
        
        if self.monto > 99999999.99:
            return False, "El monto excede el límite permitido"
        
        if self.metodo not in ['Efectivo', 'Tarjeta', 'Transferencia']:
            return False, "Método de pago no válido"
        
        return True, "Datos válidos"
    
    def marcar_como_pagado(self):
        """Marca el pago como completado"""
        self.estatus_pago = "Pagado"
        self.fecha_pago = datetime.now().date()
    
    def cancelar_pago(self):
        """Cancela el pago"""
        self.estatus_pago = "Cancelado"
    
    def esta_pagado(self):
        """Verifica si el pago está completado"""
        return self.estatus_pago == "Pagado"
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_pago': self.id_pago,
            'id_consulta': self.id_consulta,
            'monto': float(self.monto) if self.monto else 0.0,
            'metodo': self.metodo,
            'fecha_pago': str(self.fecha_pago) if self.fecha_pago else None,
            'estatus_pago': self.estatus_pago,
            'nombre_paciente': self.nombre_paciente,
            'fecha_consulta': str(self.fecha_consulta) if self.fecha_consulta else None
        }
    
    def __str__(self):
        return f"Pago(id={self.id_pago}, monto=${self.monto}, estatus={self.estatus_pago})"

