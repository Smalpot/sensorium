"""
Ventana de inicio de sesión (Login)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController
from config.database import db

class LoginView:
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SENSORIUM - Inicio de Sesión")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Controlador de autenticación
        self.auth_controller = AuthController()
        
        # Usuario autenticado (se retorna al cerrar)
        self.usuario_autenticado = None
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Conectar a la base de datos
        self.conectar_bd()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def configurar_estilos(self):
        """Configura los estilos de los widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Primary.TButton',
                       font=('Arial', 11, 'bold'),
                       background='#2563eb',
                       foreground='white',
                       padding=10)
        
        style.map('Primary.TButton',
                 background=[('active', '#1d4ed8')])
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.pack(pady=(0, 30))
        
        titulo = tk.Label(
            titulo_frame,
            text="SENSORIUM",
            font=('Arial', 32, 'bold'),
            fg='#2563eb'
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            titulo_frame,
            text="Sistema de Gestión para Consultorios",
            font=('Arial', 10),
            fg='#64748b'
        )
        subtitulo.pack()
        
        # Frame del formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Campo: Correo electrónico
        correo_label = tk.Label(
            form_frame,
            text="Correo electrónico",
            font=('Arial', 10, 'bold'),
            fg='#1e293b'
        )
        correo_label.pack(anchor='w', pady=(0, 5))
        
        self.correo_entry = ttk.Entry(form_frame, font=('Arial', 11))
        self.correo_entry.pack(fill=tk.X, ipady=8)
        self.correo_entry.insert(0, "admin@sensorium.com")  # Valor por defecto para pruebas
        
        # Campo: Contraseña
        password_label = tk.Label(
            form_frame,
            text="Contraseña",
            font=('Arial', 10, 'bold'),
            fg='#1e293b'
        )
        password_label.pack(anchor='w', pady=(20, 5))
        
        self.password_entry = ttk.Entry(form_frame, font=('Arial', 11), show='•')
        self.password_entry.pack(fill=tk.X, ipady=8)
        self.password_entry.insert(0, "admin123")  # Valor por defecto para pruebas
        
        # Checkbox: Mostrar contraseña
        self.mostrar_password_var = tk.BooleanVar()
        mostrar_check = ttk.Checkbutton(
            form_frame,
            text="Mostrar contraseña",
            variable=self.mostrar_password_var,
            command=self.toggle_password
        )
        mostrar_check.pack(anchor='w', pady=(5, 0))
        
        # Botón de inicio de sesión
        login_btn = ttk.Button(
            form_frame,
            text="Iniciar Sesión",
            style='Primary.TButton',
            command=self.iniciar_sesion
        )
        login_btn.pack(fill=tk.X, pady=(30, 10))
        
        # Label de estado de conexión
        self.estado_label = tk.Label(
            form_frame,
            text="",
            font=('Arial', 9),
            fg='#64748b'
        )
        self.estado_label.pack(pady=(10, 0))
        
        # Footer
        footer = tk.Label(
            main_frame,
            text="© 2024 SENSORIUM - Todos los derechos reservados",
            font=('Arial', 8),
            fg='#94a3b8'
        )
        footer.pack(side=tk.BOTTOM, pady=(20, 0))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.iniciar_sesion())
    
    def toggle_password(self):
        """Muestra u oculta la contraseña"""
        if self.mostrar_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='•')
    
    def conectar_bd(self):
        """Conecta a la base de datos"""
        try:
            if db.conectar():
                self.estado_label.config(
                    text="✓ Conectado a la base de datos",
                    fg='#10b981'
                )
            else:
                self.estado_label.config(
                    text="✗ Error de conexión a la base de datos",
                    fg='#ef4444'
                )
                messagebox.showerror(
                    "Error de Conexión",
                    "No se pudo conectar a la base de datos.\n"
                    "Verifica que SQL Server esté corriendo."
                )
        except Exception as e:
            self.estado_label.config(
                text=f"✗ Error: {str(e)}",
                fg='#ef4444'
            )
    
    def iniciar_sesion(self):
        """Procesa el inicio de sesión"""
        correo = self.correo_entry.get().strip()
        password = self.password_entry.get()
        
        # Validar campos
        if not correo:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa tu correo electrónico"
            )
            self.correo_entry.focus()
            return
        
        if not password:
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor ingresa tu contraseña"
            )
            self.password_entry.focus()
            return
        
        # Intentar iniciar sesión
        try:
            exito, usuario, mensaje = self.auth_controller.iniciar_sesion(correo, password)
            
            if exito:
                self.usuario_autenticado = usuario
                messagebox.showinfo(
                    "Éxito",
                    f"¡Bienvenido {usuario.nombre}!\n"
                    f"Rol: {usuario.rol.capitalize()}"
                )
                self.root.destroy()  # Cerrar ventana de login
            else:
                messagebox.showerror(
                    "Error de Autenticación",
                    mensaje
                )
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al iniciar sesión:\n{str(e)}"
            )
    
    def ejecutar(self):
        """Ejecuta la ventana y retorna el usuario autenticado"""
        self.root.mainloop()
        return self.usuario_autenticado


# Para pruebas individuales
if __name__ == "__main__":
    login = LoginView()
    usuario = login.ejecutar()
    
    if usuario:
        print(f"Usuario autenticado: {usuario.nombre}")
        print(f"Rol: {usuario.rol}")
    else:
        print("No se inició sesión")