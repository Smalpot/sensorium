from datetime import datetime, time

class Cita:
    """
    Clase que representa una cita entre paciente y psicólogo
    """
    def __init__(self, id_cita=None, id_paciente=None, id_psicologo=None,
                 fecha=None, hora=None, modalidad=None, estado="Programada"):
        self.id_cita = id_cita
        self.id_paciente = id_paciente  # Foreign Key a Paciente
        self.id_psicologo = id_psicologo  # Foreign Key a Psicologo
        self.fecha = fecha
        self.hora = hora
        self.modalidad = modalidad  # 'Presencial', 'Virtual'
        self.estado = estado  # 'Programada', 'Completada', 'Cancelada'
        
        # Datos relacionados (se llenan al consultar)
        self.nombre_paciente = None
        self.nombre_psicologo = None
        self.especialidad = None
    
    def validar_datos(self):
        """Valida que los datos de la cita sean correctos"""
        if not self.id_paciente:
            return False, "Debe seleccionar un paciente"
        
        if not self.id_psicologo:
            return False, "Debe seleccionar un psicólogo"
        
        if not self.fecha:
            return False, "La fecha es obligatoria"
        
        if not self.hora:
            return False, "La hora es obligatoria"
        
        if self.modalidad not in ['Presencial', 'Virtual']:
            return False, "La modalidad debe ser Presencial o Virtual"
        
        return True, "Datos válidos"
    
    def cancelar(self):
        """Cancela la cita"""
        self.estado = "Cancelada"
    
    def completar(self):
        """Marca la cita como completada"""
        self.estado = "Completada"
    
    def esta_disponible(self):
        """Verifica si la cita está en estado programada"""
        return self.estado == "Programada"
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_cita': self.id_cita,
            'id_paciente': self.id_paciente,
            'id_psicologo': self.id_psicologo,
            'fecha': str(self.fecha) if self.fecha else None,
            'hora': str(self.hora) if self.hora else None,
            'modalidad': self.modalidad,
            'estado': self.estado,
            'nombre_paciente': self.nombre_paciente,
            'nombre_psicologo': self.nombre_psicologo,
            'especialidad': self.especialidad
        }
    
    def __str__(self):
        return f"Cita(id={self.id_cita}, fecha={self.fecha}, hora={self.hora}, estado={self.estado})"

