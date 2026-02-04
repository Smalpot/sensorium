from datetime import datetime

class Historial:
    """
    Clase que representa el historial clínico de un paciente
    """
    def __init__(self, id_historial=None, id_paciente=None, 
                 antecedentes=None, alergias=None, tratamientos=None,
                 fecha_creacion=None):
        self.id_historial = id_historial
        self.id_paciente = id_paciente  # Foreign Key a Paciente
        self.antecedentes = antecedentes
        self.alergias = alergias
        self.tratamientos = tratamientos
        self.fecha_creacion = fecha_creacion or datetime.now().date()
        
        # Datos relacionados (se llenan al consultar)
        self.nombre_paciente = None
    
    def validar_datos(self):
        """Valida que los datos del historial sean correctos"""
        if not self.id_paciente:
            return False, "Debe asociarse a un paciente"
        
        if self.antecedentes and len(self.antecedentes) > 150:
            return False, "Los antecedentes no pueden exceder 150 caracteres"
        
        if self.alergias and len(self.alergias) > 100:
            return False, "Las alergias no pueden exceder 100 caracteres"
        
        if self.tratamientos and len(self.tratamientos) > 200:
            return False, "Los tratamientos no pueden exceder 200 caracteres"
        
        return True, "Datos válidos"
    
    def agregar_antecedente(self, nuevo_antecedente):
        """Agrega un nuevo antecedente al historial"""
        if self.antecedentes:
            self.antecedentes += f"; {nuevo_antecedente}"
        else:
            self.antecedentes = nuevo_antecedente
    
    def agregar_alergia(self, nueva_alergia):
        """Agrega una nueva alergia al historial"""
        if self.alergias:
            self.alergias += f"; {nueva_alergia}"
        else:
            self.alergias = nueva_alergia
    
    def agregar_tratamiento(self, nuevo_tratamiento):
        """Agrega un nuevo tratamiento al historial"""
        if self.tratamientos:
            self.tratamientos += f"; {nuevo_tratamiento}"
        else:
            self.tratamientos = nuevo_tratamiento
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_historial': self.id_historial,
            'id_paciente': self.id_paciente,
            'antecedentes': self.antecedentes,
            'alergias': self.alergias,
            'tratamientos': self.tratamientos,
            'fecha_creacion': str(self.fecha_creacion) if self.fecha_creacion else None,
            'nombre_paciente': self.nombre_paciente
        }
    
    def __str__(self):
        return f"Historial(id={self.id_historial}, paciente_id={self.id_paciente})"

