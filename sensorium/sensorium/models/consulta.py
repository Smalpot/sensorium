class Consulta:
    """
    Clase que representa una consulta realizada (sesión completada)
    """
    def __init__(self, id_consulta=None, id_cita=None, notas=None,
                 duracion=None, diagnostico=None, recomend=None):
        self.id_consulta = id_consulta
        self.id_cita = id_cita  # Foreign Key a Cita
        self.notas = notas
        self.duracion = duracion  # Duración en minutos
        self.diagnostico = diagnostico
        self.recomend = recomend
        
        # Datos relacionados (se llenan al consultar)
        self.fecha_cita = None
        self.nombre_paciente = None
        self.nombre_psicologo = None
    
    def validar_datos(self):
        """Valida que los datos de la consulta sean correctos"""
        if not self.id_cita:
            return False, "Debe asociarse a una cita"
        
        if self.duracion and (self.duracion < 0 or self.duracion > 300):
            return False, "La duración debe estar entre 0 y 300 minutos"
        
        if self.notas and len(self.notas) > 200:
            return False, "Las notas no pueden exceder 200 caracteres"
        
        if self.diagnostico and len(self.diagnostico) > 150:
            return False, "El diagnóstico no puede exceder 150 caracteres"
        
        if self.recomend and len(self.recomend) > 150:
            return False, "Las recomendaciones no pueden exceder 150 caracteres"
        
        return True, "Datos válidos"
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_consulta': self.id_consulta,
            'id_cita': self.id_cita,
            'notas': self.notas,
            'duracion': self.duracion,
            'diagnostico': self.diagnostico,
            'recomend': self.recomend,
            'fecha_cita': str(self.fecha_cita) if self.fecha_cita else None,
            'nombre_paciente': self.nombre_paciente,
            'nombre_psicologo': self.nombre_psicologo
        }
    
    def __str__(self):
        return f"Consulta(id={self.id_consulta}, cita_id={self.id_cita}, duracion={self.duracion}min)"

