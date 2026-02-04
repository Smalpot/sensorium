"""
Ventana principal del sistema (Dashboard)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.auth_controller import AuthController
from controllers.paciente_controller import PacienteController
from controllers.psicologo_controller import PsicologoController
from controllers.cita_controller import CitaController

class MainView:
    """Ventana principal del sistema"""
    
    def __init__(self, usuario):
        self.root = tk.Tk()
        self.root.title("SENSORIUM - Sistema de Gestión")
        self.root.geometry("1200x700")
        
        # Usuario actual
        self.usuario = usuario
        
        # Controladores
        self.auth_controller = AuthController()
        self.auth_controller.usuario_actual = usuario
        self.auth_controller.sesion_activa = True
        
        self.paciente_controller = PacienteController()
        self.psicologo_controller = PsicologoController()
        self.cita_controller = CitaController()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar estadísticas
        self.cargar_estadisticas()
        
        # Actualizar reloj
        self.actualizar_reloj()
    
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
        
        # Estilo para tarjetas
        style.configure('Card.TFrame', background='white', relief='raised')
        
        # Estilo para botones del menú
        style.configure('Menu.TButton',
                       font=('Arial', 11),
                       padding=15,
                       background='#f1f5f9')
        
        style.map('Menu.TButton',
                 background=[('active', '#e2e8f0')])
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # ===== BARRA SUPERIOR =====
        top_bar = tk.Frame(self.root, bg='#2563eb', height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo y título
        titulo = tk.Label(
            top_bar,
            text="SENSORIUM",
            font=('Arial', 18, 'bold'),
            bg='#2563eb',
            fg='white'
        )
        titulo.pack(side=tk.LEFT, padx=20)
        
        # Información del usuario
        user_frame = tk.Frame(top_bar, bg='#2563eb')
        user_frame.pack(side=tk.RIGHT, padx=20)
        
        user_name = tk.Label(
            user_frame,
            text=f"👤 {self.usuario.nombre}",
            font=('Arial', 10, 'bold'),
            bg='#2563eb',
            fg='white'
        )
        user_name.pack(side=tk.TOP, anchor='e')
        
        user_rol = tk.Label(
            user_frame,
            text=self.usuario.rol.capitalize(),
            font=('Arial', 9),
            bg='#2563eb',
            fg='#bfdbfe'
        )
        user_rol.pack(side=tk.TOP, anchor='e')
        
        # Reloj
        self.reloj_label = tk.Label(
            top_bar,
            text="",
            font=('Arial', 10),
            bg='#2563eb',
            fg='white'
        )
        self.reloj_label.pack(side=tk.RIGHT, padx=20)
        
        # ===== CONTENEDOR PRINCIPAL =====
        main_container = tk.Frame(self.root, bg='#f8fafc')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== MENÚ LATERAL =====
        sidebar = tk.Frame(main_container, bg='#1e293b', width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Título del menú
        menu_titulo = tk.Label(
            sidebar,
            text="MENÚ PRINCIPAL",
            font=('Arial', 12, 'bold'),
            bg='#1e293b',
            fg='white',
            pady=20
        )
        menu_titulo.pack(fill=tk.X)
        
        # Botones del menú
        menu_items = [
            ("🏠 Dashboard", self.mostrar_dashboard),
            ("👥 Pacientes", self.abrir_pacientes),
            ("👨‍⚕️ Psicólogos", self.abrir_psicologos),
            ("📅 Citas", self.abrir_citas),
            ("📋 Consultas", self.abrir_consultas),
            ("💰 Pagos", self.abrir_pagos),
            ("📊 Reportes", self.abrir_reportes),
            ("⚙️ Configuración", self.abrir_configuracion),
        ]
        
        for texto, comando in menu_items:
            btn = tk.Button(
                sidebar,
                text=texto,
                font=('Arial', 11),
                bg='#1e293b',
                fg='white',
                activebackground='#334155',
                activeforeground='white',
                bd=0,
                cursor='hand2',
                anchor='w',
                padx=20,
                pady=15,
                command=comando
            )
            btn.pack(fill=tk.X)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#334155'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#1e293b'))
        
        # Botón cerrar sesión
        tk.Frame(sidebar, bg='#1e293b', height=1).pack(fill=tk.X, pady=20)
        
        logout_btn = tk.Button(
            sidebar,
            text="🚪 Cerrar Sesión",
            font=('Arial', 11, 'bold'),
            bg='#dc2626',
            fg='white',
            activebackground='#b91c1c',
            activeforeground='white',
            bd=0,
            cursor='hand2',
            pady=15,
            command=self.cerrar_sesion
        )
        logout_btn.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        # ===== ÁREA DE CONTENIDO =====
        self.content_area = tk.Frame(main_container, bg='#f8fafc')
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mostrar dashboard por defecto
        self.mostrar_dashboard()
    
    def limpiar_contenido(self):
        """Limpia el área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard con estadísticas"""
        self.limpiar_contenido()
        
        # Título
        titulo = tk.Label(
            self.content_area,
            text="Dashboard",
            font=('Arial', 24, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        titulo.pack(anchor='w', pady=(0, 20))
        
        # Frame para las tarjetas de estadísticas
        stats_frame = tk.Frame(self.content_area, bg='#f8fafc')
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Tarjetas de estadísticas
        self.crear_tarjeta_estadistica(
            stats_frame,
            "Total Pacientes",
            self.total_pacientes,
            "#10b981",
            "👥"
        ).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.crear_tarjeta_estadistica(
            stats_frame,
            "Total Psicólogos",
            self.total_psicologos,
            "#3b82f6",
            "👨‍⚕️"
        ).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.crear_tarjeta_estadistica(
            stats_frame,
            "Citas Programadas",
            self.total_citas_programadas,
            "#f59e0b",
            "📅"
        ).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.crear_tarjeta_estadistica(
            stats_frame,
            "Citas Hoy",
            self.citas_hoy,
            "#8b5cf6",
            "📆"
        ).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Mensaje de bienvenida
        bienvenida_frame = tk.Frame(self.content_area, bg='white', relief='solid', bd=1)
        bienvenida_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        hora_actual = datetime.now().hour
        if hora_actual < 12:
            saludo = "Buenos días"
        elif hora_actual < 18:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
        
        mensaje = tk.Label(
            bienvenida_frame,
            text=f"{saludo}, {self.usuario.nombre}",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#1e293b'
        )
        mensaje.pack(pady=20)
        
        submensaje = tk.Label(
            bienvenida_frame,
            text="Bienvenido al Sistema de Gestión SENSORIUM\n"
                 "Selecciona una opción del menú lateral para comenzar",
            font=('Arial', 12),
            bg='white',
            fg='#64748b',
            justify='center'
        )
        submensaje.pack(pady=10)
    
    def crear_tarjeta_estadistica(self, parent, titulo, valor, color, icono):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        
        # Barra de color superior
        color_bar = tk.Frame(card, bg=color, height=5)
        color_bar.pack(fill=tk.X)
        
        # Contenido
        content = tk.Frame(card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icono y valor
        valor_label = tk.Label(
            content,
            text=f"{icono} {valor}",
            font=('Arial', 28, 'bold'),
            bg='white',
            fg=color
        )
        valor_label.pack()
        
        # Título
        titulo_label = tk.Label(
            content,
            text=titulo,
            font=('Arial', 11),
            bg='white',
            fg='#64748b'
        )
        titulo_label.pack()
        
        return card
    
    def cargar_estadisticas(self):
        """Carga las estadísticas desde la base de datos"""
        try:
            self.total_pacientes = self.paciente_controller.contar_pacientes()
            self.total_psicologos = self.psicologo_controller.contar_psicologos()
            self.total_citas_programadas = self.cita_controller.contar_citas('Programada')
            
            # Citas de hoy
            citas_hoy = self.cita_controller.obtener_citas_del_dia()
            self.citas_hoy = len(citas_hoy)
            
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
            self.total_pacientes = 0
            self.total_psicologos = 0
            self.total_citas_programadas = 0
            self.citas_hoy = 0
    
    def actualizar_reloj(self):
        """Actualiza el reloj en tiempo real"""
        now = datetime.now()
        tiempo = now.strftime("%H:%M:%S")
        fecha = now.strftime("%d/%m/%Y")
        self.reloj_label.config(text=f"🕐 {tiempo} | {fecha}")
        self.root.after(1000, self.actualizar_reloj)
    
    # ===== FUNCIONES PARA ABRIR MÓDULOS =====
    
    def abrir_pacientes(self):
        """Abre el módulo de pacientes"""
        from views.paciente_view import PacienteView
        PacienteView(self.content_area)
    
    def abrir_psicologos(self):
        """Abre el módulo de psicólogos"""
        self.limpiar_contenido()
        label = tk.Label(
            self.content_area,
            text="Módulo de Psicólogos\n(En desarrollo)",
            font=('Arial', 20),
            bg='#f8fafc'
        )
        label.pack(expand=True)
    
    def abrir_citas(self):
        """Abre el módulo de citas"""
        self.limpiar_contenido()
        label = tk.Label(
            self.content_area,
            text="Módulo de Citas\n(En desarrollo)",
            font=('Arial', 20),
            bg='#f8fafc'
        )
        label.pack(expand=True)
    
    def abrir_consultas(self):
        """Abre el módulo de consultas"""
        from views.consulta_view import ConsultaView
        ConsultaView(self.content_area)
    
    def abrir_pagos(self):
        """Abre el módulo de pagos"""
        from views.pago_view import PagoView
        PagoView(self.content_area)
    
    def abrir_reportes(self):
        """Abre el módulo de reportes"""
        self.limpiar_contenido()
        label = tk.Label(
            self.content_area,
            text="Módulo de Reportes\n(En desarrollo)",
            font=('Arial', 20),
            bg='#f8fafc'
        )
        label.pack(expand=True)
    
    def abrir_configuracion(self):
        """Abre el módulo de configuración"""
        self.limpiar_contenido()
        label = tk.Label(
            self.content_area,
            text="Módulo de Configuración\n(En desarrollo)",
            font=('Arial', 20),
            bg='#f8fafc'
        )
        label.pack(expand=True)
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?"
        )
        
        if respuesta:
            self.auth_controller.cerrar_sesion()
            self.root.destroy()
    
    def ejecutar(self):
        """Ejecuta la ventana principal"""
        self.root.mainloop()


# Para pruebas individuales
if __name__ == "__main__":
    from models.usuario import Usuario
    
    # Usuario de prueba
    usuario_prueba = Usuario(
        id_usuario=1,
        nombre="Administrador",
        correo="admin@sensorium.com",
        rol="administrador"
    )
    
    main = MainView(usuario_prueba)
    main.ejecutar()