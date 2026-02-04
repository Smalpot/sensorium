class Psicologo:
    """
    Clase que representa un psicólogo del consultorio
    Relacionado con la tabla USUARIO
    """
    def __init__(self, id_psicologo=None, id_usuario=None, 
                 especialidad=None, experiencia=None, cedula=None):
        self.id_psicologo = id_psicologo
        self.id_usuario = id_usuario  # Foreign Key a Usuario
        self.especialidad = especialidad
        self.experiencia = experiencia
        self.cedula = cedula
        
        # Datos del usuario relacionado (se llenan al consultar)
        self.nombre = None
        self.correo = None
    
    def validar_datos(self):
        """Valida que los datos del psicólogo sean correctos"""
        if not self.especialidad or len(self.especialidad.strip()) == 0:
            return False, "La especialidad es obligatoria"
        
        if not self.cedula or len(self.cedula) < 8:
            return False, "La cédula profesional no es válida"
        
        return True, "Datos válidos"
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_psicologo': self.id_psicologo,
            'id_usuario': self.id_usuario,
            'especialidad': self.especialidad,
            'experiencia': self.experiencia,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'correo': self.correo
        }
    
    def __str__(self):
        nombre = self.nombre or "Sin nombre"
        return f"Psicologo(id={self.id_psicologo}, nombre={nombre}, especialidad={self.especialidad})"

