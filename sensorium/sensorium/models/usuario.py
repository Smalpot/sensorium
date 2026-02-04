import hashlib
from datetime import datetime

class Usuario:
    """
    Clase que representa un usuario del sistema SENSORIUM
    """
    def __init__(self, id_usuario=None, nombre=None, correo=None, 
                 contraseña=None, rol=None, fecha_regist=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol  # 'administrador', 'psicologo'
        self.fecha_regist = fecha_regist or datetime.now().date()
    
    def encriptar_contraseña(self, contraseña_plana):
        """Encripta la contraseña usando SHA256"""
        return hashlib.sha256(contraseña_plana.encode()).hexdigest()
    
    def verificar_contraseña(self, contraseña_plana):
        """Verifica si la contraseña es correcta"""
        return self.contraseña == self.encriptar_contraseña(contraseña_plana)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'correo': self.correo,
            'rol': self.rol,
            'fecha_regist': str(self.fecha_regist)
        }
    
    def __str__(self):
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre}, rol={self.rol})"
    
    def __repr__(self):
        return self.__str__()