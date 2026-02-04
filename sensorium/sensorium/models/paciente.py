from datetime import datetime

class Paciente:
    """
    Clase que representa un paciente del consultorio
    """
    def __init__(self, id_paciente=None, nombre=None, correo=None, 
                 telefono=None, direccion=None, fecha_regist=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_regist = fecha_regist or datetime.now().date()
    
    def validar_datos(self):
        """Valida que los datos del paciente sean correctos"""
        if not self.nombre or len(self.nombre.strip()) == 0:
            return False, "El nombre es obligatorio"
        
        if not self.telefono or len(self.telefono) < 10:
            return False, "El teléfono debe tener al menos 10 dígitos"
        
        if self.correo and '@' not in self.correo:
            return False, "El correo no es válido"
        
        return True, "Datos válidos"
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_paciente': self.id_paciente,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'fecha_regist': str(self.fecha_regist)
        }
    
    def __str__(self):
        return f"Paciente(id={self.id_paciente}, nombre={self.nombre})"

