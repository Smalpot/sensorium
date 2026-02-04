"""
Controlador para gestionar usuarios del sistema
"""

from config.database import db
from models.usuario import Usuario
from datetime import datetime

class UsuarioController:
    """Controlador para operaciones CRUD de usuarios"""
    
    def __init__(self):
        self.db = db
    
    def crear_usuario(self, usuario: Usuario) -> tuple:
        """
        Crea un nuevo usuario en la base de datos
        Args:
            usuario: Objeto Usuario con los datos
        Returns:
            tuple: (exito: bool, mensaje: str, id: int)
        """
        try:
            # Encriptar contraseña
            contraseña_hash = usuario.encriptar_contraseña(usuario.contraseña)
            
            query = """
            INSERT INTO USUARIO (nombre, correo, contraseña, rol, fecha_regist)
            VALUES (?, ?, ?, ?, ?)
            """
            parametros = (
                usuario.nombre,
                usuario.correo,
                contraseña_hash,
                usuario.rol,
                usuario.fecha_regist or datetime.now().date()
            )
            
            if self.db.ejecutar_query(query, parametros):
                id_insertado = self.db.obtener_ultimo_id()
                return True, "Usuario creado exitosamente", id_insertado
            else:
                return False, "Error al crear usuario", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def obtener_usuario_por_id(self, id_usuario: int) -> Usuario:
        """
        Obtiene un usuario por su ID
        Args:
            id_usuario: ID del usuario
        Returns:
            Usuario: Objeto Usuario o None
        """
        try:
            query = "SELECT * FROM USUARIO WHERE IDusuario = ?"
            resultado = self.db.ejecutar_consulta_una(query, (id_usuario,))
            
            if resultado:
                return Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    contraseña=resultado[3],
                    rol=resultado[4],
                    fecha_regist=resultado[5]
                )
            return None
            
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_usuario_por_correo(self, correo: str) -> Usuario:
        """
        Obtiene un usuario por su correo electrónico
        Args:
            correo: Correo electrónico del usuario
        Returns:
            Usuario: Objeto Usuario o None
        """
        try:
            query = "SELECT * FROM USUARIO WHERE correo = ?"
            resultado = self.db.ejecutar_consulta_una(query, (correo,))
            
            if resultado:
                return Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    contraseña=resultado[3],
                    rol=resultado[4],
                    fecha_regist=resultado[5]
                )
            return None
            
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def listar_usuarios(self, rol: str = None) -> list:
        """
        Lista todos los usuarios o filtra por rol
        Args:
            rol: Rol a filtrar (opcional)
        Returns:
            list: Lista de objetos Usuario
        """
        try:
            if rol:
                query = "SELECT * FROM USUARIO WHERE rol = ? ORDER BY nombre"
                resultados = self.db.ejecutar_consulta(query, (rol,))
            else:
                query = "SELECT * FROM USUARIO ORDER BY nombre"
                resultados = self.db.ejecutar_consulta(query)
            
            usuarios = []
            for resultado in resultados:
                usuarios.append(Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    correo=resultado[2],
                    contraseña=resultado[3],
                    rol=resultado[4],
                    fecha_regist=resultado[5]
                ))
            
            return usuarios
            
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
    
    def actualizar_usuario(self, usuario: Usuario) -> tuple:
        """
        Actualiza los datos de un usuario
        Args:
            usuario: Objeto Usuario con los datos actualizados
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = """
            UPDATE USUARIO 
            SET nombre = ?, correo = ?, rol = ?
            WHERE IDusuario = ?
            """
            parametros = (
                usuario.nombre,
                usuario.correo,
                usuario.rol,
                usuario.id_usuario
            )
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Usuario actualizado exitosamente"
            else:
                return False, "Error al actualizar usuario"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cambiar_contraseña(self, id_usuario: int, contraseña_nueva: str) -> tuple:
        """
        Cambia la contraseña de un usuario
        Args:
            id_usuario: ID del usuario
            contraseña_nueva: Nueva contraseña (sin encriptar)
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            # Crear objeto usuario temporal para encriptar
            usuario_temp = Usuario()
            contraseña_hash = usuario_temp.encriptar_contraseña(contraseña_nueva)
            
            query = "UPDATE USUARIO SET contraseña = ? WHERE IDusuario = ?"
            parametros = (contraseña_hash, id_usuario)
            
            if self.db.ejecutar_query(query, parametros):
                return True, "Contraseña actualizada exitosamente"
            else:
                return False, "Error al actualizar contraseña"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def eliminar_usuario(self, id_usuario: int) -> tuple:
        """
        Elimina un usuario de la base de datos
        Args:
            id_usuario: ID del usuario a eliminar
        Returns:
            tuple: (exito: bool, mensaje: str)
        """
        try:
            query = "DELETE FROM USUARIO WHERE IDusuario = ?"
            
            if self.db.ejecutar_query(query, (id_usuario,)):
                return True, "Usuario eliminado exitosamente"
            else:
                return False, "Error al eliminar usuario"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def verificar_credenciales(self, correo: str, contraseña: str) -> tuple:
        """
        Verifica las credenciales de un usuario para login
        Args:
            correo: Correo electrónico
            contraseña: Contraseña sin encriptar
        Returns:
            tuple: (exito: bool, usuario: Usuario o None, mensaje: str)
        """
        try:
            usuario = self.obtener_usuario_por_correo(correo)
            
            if not usuario:
                return False, None, "Usuario no encontrado"
            
            if usuario.verificar_contraseña(contraseña):
                return True, usuario, "Credenciales correctas"
            else:
                return False, None, "Contraseña incorrecta"
                
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def contar_usuarios(self, rol: str = None) -> int:
        """
        Cuenta el número de usuarios
        Args:
            rol: Filtrar por rol (opcional)
        Returns:
            int: Número de usuarios
        """
        try:
            if rol:
                query = "SELECT COUNT(*) FROM USUARIO WHERE rol = ?"
                resultado = self.db.ejecutar_consulta_una(query, (rol,))
            else:
                query = "SELECT COUNT(*) FROM USUARIO"
                resultado = self.db.ejecutar_consulta_una(query)
            
            return resultado[0] if resultado else 0
            
        except Exception as e:
            print(f"Error al contar usuarios: {e}")
            return 0