# ====================================================================================
# controllers/auth_controller.py
# ====================================================================================
"""
Controlador de autenticación para el sistema SENSORIUM
Maneja login, sesiones y permisos
"""

from config.database import db
from models.usuario import Usuario
from datetime import datetime

class AuthController:
    """Controlador para autenticación y autorización"""
    
    def __init__(self):
        self.db = db
        self.usuario_actual = None
        self.sesion_activa = False
        self.hora_inicio_sesion = None
    
    def iniciar_sesion(self, correo: str, contraseña: str) -> tuple:
        """
        Inicia sesión con correo y contraseña
        Args:
            correo: Correo electrónico del usuario
            contraseña: Contraseña sin encriptar
        Returns:
            tuple: (exito: bool, usuario: Usuario o None, mensaje: str)
        """
        try:
            # Buscar usuario por correo
            query = "SELECT * FROM USUARIO WHERE correo = ?"
            resultado = self.db.ejecutar_consulta_una(query, (correo,))
            
            if not resultado:
                return False, None, "Usuario no encontrado"
            
            # Crear objeto usuario
            usuario = Usuario(
                id_usuario=resultado[0],
                nombre=resultado[1],
                correo=resultado[2],
                contraseña=resultado[3],
                rol=resultado[4],
                fecha_regist=resultado[5]
            )
            
            # Verificar contraseña
            if usuario.verificar_contraseña(contraseña):
                self.usuario_actual = usuario
                self.sesion_activa = True
                self.hora_inicio_sesion = datetime.now()
                return True, usuario, "Inicio de sesión exitoso"
            else:
                return False, None, "Contraseña incorrecta"
                
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def cerrar_sesion(self) -> bool:
        """
        Cierra la sesión actual
        Returns:
            bool: True si se cerró correctamente
        """
        try:
            self.usuario_actual = None
            self.sesion_activa = False
            self.hora_inicio_sesion = None
            return True
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            return False
    
    def verificar_sesion(self) -> bool:
        """
        Verifica si hay una sesión activa
        Returns:
            bool: True si hay sesión activa
        """
        return self.sesion_activa and self.usuario_actual is not None
    
    def obtener_usuario_actual(self) -> Usuario:
        """
        Obtiene el usuario de la sesión actual
        Returns:
            Usuario: Objeto Usuario o None
        """
        return self.usuario_actual if self.verificar_sesion() else None
    
    def es_administrador(self) -> bool:
        """
        Verifica si el usuario actual es administrador
        Returns:
            bool: True si es administrador
        """
        if not self.verificar_sesion():
            return False
        return self.usuario_actual.rol == 'administrador'
    
    def es_psicologo(self) -> bool:
        """
        Verifica si el usuario actual es psicólogo
        Returns:
            bool: True si es psicólogo
        """
        if not self.verificar_sesion():
            return False
        return self.usuario_actual.rol == 'psicologo'
    
    def tiene_permiso(self, permiso: str) -> bool:
        """
        Verifica si el usuario actual tiene un permiso específico
        Args:
            permiso: Nombre del permiso a verificar
        Returns:
            bool: True si tiene el permiso
        """
        if not self.verificar_sesion():
            return False
        
        from config.settings import ROLES
        
        rol = self.usuario_actual.rol
        if rol in ROLES:
            return permiso in ROLES[rol]['permisos']
        
        return False
    
    def tiempo_sesion(self) -> int:
        """
        Obtiene el tiempo de la sesión actual en segundos
        Returns:
            int: Segundos desde el inicio de sesión
        """
        if not self.verificar_sesion() or not self.hora_inicio_sesion:
            return 0
        
        delta = datetime.now() - self.hora_inicio_sesion
        return int(delta.total_seconds())
    
    def renovar_sesion(self) -> bool:
        """
        Renueva el tiempo de la sesión actual
        Returns:
            bool: True si se renovó correctamente
        """
        if self.verificar_sesion():
            self.hora_inicio_sesion = datetime.now()
            return True
        return False
    
    def cambiar_contraseña_actual(self, contraseña_actual: str, contraseña_nueva: str) -> tuple:
        """
        Cambia la contraseña del usuario actual
        Args:
            contraseña_actual: Contraseña actual sin encriptar
            contraseña_nueva: Nueva contraseña sin encriptar
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            if not self.verificar_sesion():
                return False, "No hay sesión activa"
            
            # Verificar contraseña actual
            if not self.usuario_actual.verificar_contraseña(contraseña_actual):
                return False, "Contraseña actual incorrecta"
            
            # Validar nueva contraseña
            if len(contraseña_nueva) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            
            # Actualizar contraseña
            contraseña_hash = self.usuario_actual.encriptar_contraseña(contraseña_nueva)
            query = "UPDATE USUARIO SET contraseña = ? WHERE IDusuario = ?"
            
            if self.db.ejecutar_query(query, (contraseña_hash, self.usuario_actual.id_usuario)):
                self.usuario_actual.contraseña = contraseña_hash
                return True, "Contraseña actualizada exitosamente"
            else:
                return False, "Error al actualizar contraseña"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def obtener_info_sesion(self) -> dict:
        """
        Obtiene información de la sesión actual
        Returns:
            dict: Información de la sesión
        """
        if not self.verificar_sesion():
            return {
                'activa': False,
                'usuario': None,
                'tiempo_sesion': 0
            }
        
        return {
            'activa': True,
            'usuario': self.usuario_actual.to_dict(),
            'rol': self.usuario_actual.rol,
            'tiempo_sesion': self.tiempo_sesion(),
            'hora_inicio': self.hora_inicio_sesion.strftime('%H:%M:%S') if self.hora_inicio_sesion else None
        }
