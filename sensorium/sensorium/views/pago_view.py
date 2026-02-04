"""
Ventana de gestión de consultas
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controllers.consulta_controller import ConsultaController
from controllers.cita_controller import CitaController
from models.consulta import Consulta

class ConsultaView:
    """Ventana para gestionar consultas"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.controller = ConsultaController()
        self.cita_controller = CitaController()
        
        # Variables
        self.consulta_seleccionada = None
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar consultas
        self.cargar_consultas()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Limpiar frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # ===== TÍTULO =====
        titulo = tk.Label(
            self.parent_frame,
            text="Gestión de Consultas",
            font=('Arial', 24, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        titulo.pack(anchor='w', pady=(0, 20))
        
        # ===== BARRA DE HERRAMIENTAS =====
        toolbar = tk.Frame(self.parent_frame, bg='#f8fafc')
        toolbar.pack(fill=tk.X, pady=(0, 20))
        
        # Botones
        btn_nueva = tk.Button(
            toolbar,
            text="➕ Nueva Consulta",
            font=('Arial', 10, 'bold'),
            bg='#10b981',
            fg='white',
            activebackground='#059669',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.nueva_consulta
        )
        btn_nueva.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_ver = tk.Button(
            toolbar,
            text="👁️ Ver Detalles",
            font=('Arial', 10, 'bold'),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.ver_consulta
        )
        btn_ver.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_editar = tk.Button(
            toolbar,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#f59e0b',
            fg='white',
            activebackground='#d97706',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.editar_consulta
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_eliminar = tk.Button(
            toolbar,
            text="🗑️ Eliminar",
            font=('Arial', 10, 'bold'),
            bg='#ef4444',
            fg='white',
            activebackground='#dc2626',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.eliminar_consulta
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        
        # ===== TABLA DE CONSULTAS =====
        table_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columnas = ('ID', 'Fecha', 'Paciente', 'Psicólogo', 'Duración', 'Diagnóstico')
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columnas,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse'
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Paciente', text='Paciente')
        self.tree.heading('Psicólogo', text='Psicólogo')
        self.tree.heading('Duración', text='Duración (min)')
        self.tree.heading('Diagnóstico', text='Diagnóstico')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Fecha', width=100, anchor='center')
        self.tree.column('Paciente', width=200)
        self.tree.column('Psicólogo', width=200)
        self.tree.column('Duración', width=100, anchor='center')
        self.tree.column('Diagnóstico', width=300)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind eventos
        self.tree.bind('<Double-1>', lambda e: self.ver_consulta())
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def cargar_consultas(self):
        """Carga todas las consultas en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            consultas = self.controller.listar_consultas()
            
            for consulta in consultas:
                diagnostico = consulta.diagnostico[:50] + '...' if consulta.diagnostico and len(consulta.diagnostico) > 50 else consulta.diagnostico or ''
                
                self.tree.insert('', tk.END, values=(
                    consulta.id_consulta,
                    consulta.fecha_cita or '',
                    consulta.nombre_paciente or '',
                    consulta.nombre_psicologo or '',
                    consulta.duracion or '',
                    diagnostico
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar consultas:\n{str(e)}")
    
    def on_select(self, event):
        """Maneja la selección de una consulta"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_consulta = item['values'][0]
            self.consulta_seleccionada = self.controller.obtener_consulta_por_id(id_consulta)
    
    def nueva_consulta(self):
        """Abre ventana para crear nueva consulta"""
        FormularioConsulta(self.parent_frame, self.controller, self.cita_controller, None, self.cargar_consultas)
    
    def ver_consulta(self):
        """Muestra los detalles completos de la consulta"""
        if not self.consulta_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una consulta")
            return
        
        DetalleConsulta(self.parent_frame, self.consulta_seleccionada)
    
    def editar_consulta(self):
        """Abre ventana para editar consulta seleccionada"""
        if not self.consulta_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una consulta")
            return
        
        FormularioConsulta(self.parent_frame, self.controller, self.cita_controller, 
                          self.consulta_seleccionada, self.cargar_consultas)
    
    def eliminar_consulta(self):
        """Elimina la consulta seleccionada"""
        if not self.consulta_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una consulta")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar esta consulta?\n\n"
            f"Paciente: {self.consulta_seleccionada.nombre_paciente}\n"
            f"Fecha: {self.consulta_seleccionada.fecha_cita}\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.eliminar_consulta(self.consulta_seleccionada.id_consulta)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_consultas()
                    self.consulta_seleccionada = None
                else:
                    messagebox.showerror("Error", mensaje)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar:\n{str(e)}")


class FormularioConsulta:
    """Ventana de formulario para crear/editar consulta"""
    
    def __init__(self, parent, controller, cita_controller, consulta=None, callback=None):
        self.controller = controller
        self.cita_controller = cita_controller
        self.consulta = consulta
        self.callback = callback
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nueva Consulta" if not consulta else "Editar Consulta")
        self.ventana.geometry("600x650")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Cargar citas completadas
        self.citas = self.cita_controller.listar_citas(estado='Completada')
        
        # Crear formulario
        self.crear_formulario()
        
        # Si es edición, cargar datos
        if self.consulta:
            self.cargar_datos()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_formulario(self):
        """Crea el formulario"""
        main_frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Nueva Consulta" if not self.consulta else "Editar Consulta",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        titulo.pack(pady=(0, 20))
        
        # Cita (solo en nuevo)
        if not self.consulta:
            tk.Label(main_frame, text="Cita Completada *", font=('Arial', 10, 'bold'),
                    bg='white', fg='#1e293b').pack(anchor='w')
            
            self.cita_var = tk.StringVar()
            cita_combo = ttk.Combobox(
                main_frame,
                textvariable=self.cita_var,
                font=('Arial', 10),
                state='readonly'
            )
            cita_combo['values'] = [
                f"{c.id_cita} - {c.nombre_paciente} - {c.fecha} {c.hora}" 
                for c in self.citas
            ]
            cita_combo.pack(fill=tk.X, ipady=6, pady=(5, 10))
            self.cita_combo = cita_combo
        
        # Duración
        tk.Label(main_frame, text="Duración (minutos)", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.duracion_entry = ttk.Entry(main_frame, font=('Arial', 11))
        self.duracion_entry.pack(fill=tk.X, ipady=6, pady=(5, 10))
        
        # Notas
        tk.Label(main_frame, text="Notas de la Consulta", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.notas_text = scrolledtext.ScrolledText(
            main_frame,
            font=('Arial', 10),
            height=4,
            wrap=tk.WORD
        )
        self.notas_text.pack(fill=tk.X, pady=(5, 10))
        
        # Diagnóstico
        tk.Label(main_frame, text="Diagnóstico", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.diagnostico_text = scrolledtext.ScrolledText(
            main_frame,
            font=('Arial', 10),
            height=4,
            wrap=tk.WORD
        )
        self.diagnostico_text.pack(fill=tk.X, pady=(5, 10))
        
        # Recomendaciones
        tk.Label(main_frame, text="Recomendaciones", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.recomend_text = scrolledtext.ScrolledText(
            main_frame,
            font=('Arial', 10),
            height=4,
            wrap=tk.WORD
        )
        self.recomend_text.pack(fill=tk.X, pady=(5, 10))
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Arial', 11),
            bg='#64748b',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.ventana.destroy
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Guardar",
            font=('Arial', 11, 'bold'),
            bg='#10b981',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.guardar
        ).pack(side=tk.RIGHT)
    
    def cargar_datos(self):
        """Carga los datos de la consulta en el formulario"""
        self.duracion_entry.insert(0, str(self.consulta.duracion) if self.consulta.duracion else '')
        
        if self.consulta.notas:
            self.notas_text.insert('1.0', self.consulta.notas)
        
        if self.consulta.diagnostico:
            self.diagnostico_text.insert('1.0', self.consulta.diagnostico)
        
        if self.consulta.recomend:
            self.recomend_text.insert('1.0', self.consulta.recomend)
    
    def guardar(self):
        """Guarda la consulta"""
        # Obtener valores
        duracion = self.duracion_entry.get().strip()
        notas = self.notas_text.get('1.0', tk.END).strip()
        diagnostico = self.diagnostico_text.get('1.0', tk.END).strip()
        recomend = self.recomend_text.get('1.0', tk.END).strip()
        
        # Validar duración
        if duracion:
            try:
                duracion = int(duracion)
            except:
                messagebox.showerror("Error", "La duración debe ser un número entero")
                return
        else:
            duracion = None
        
        try:
            if self.consulta:  # Editar
                self.consulta.duracion = duracion
                self.consulta.notas = notas if notas else None
                self.consulta.diagnostico = diagnostico if diagnostico else None
                self.consulta.recomend = recomend if recomend else None
                
                exito, mensaje = self.controller.actualizar_consulta(self.consulta)
            else:  # Nueva
                if not self.cita_var.get():
                    messagebox.showwarning("Campo Requerido", "Selecciona una cita")
                    return
                
                id_cita = int(self.cita_var.get().split(' - ')[0])
                
                nueva_consulta = Consulta(
                    id_cita=id_cita,
                    duracion=duracion,
                    notas=notas if notas else None,
                    diagnostico=diagnostico if diagnostico else None,
                    recomend=recomend if recomend else None
                )
                
                exito, mensaje, id_consulta = self.controller.crear_consulta(nueva_consulta)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                if self.callback:
                    self.callback()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")


class DetalleConsulta:
    """Ventana para ver detalles completos de una consulta"""
    
    def __init__(self, parent, consulta):
        self.consulta = consulta
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Detalles de la Consulta")
        self.ventana.geometry("600x550")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear contenido
        self.crear_widgets()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_widgets(self):
        """Crea el contenido de la ventana"""
        main_frame = tk.Frame(self.ventana, bg='white', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="Detalles de la Consulta",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(pady=(0, 20))
        
        # Información básica
        info_frame = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_data = [
            ("📅 Fecha:", self.consulta.fecha_cita or 'N/A'),
            ("👤 Paciente:", self.consulta.nombre_paciente or 'N/A'),
            ("👨‍⚕️ Psicólogo:", self.consulta.nombre_psicologo or 'N/A'),
            ("⏱️ Duración:", f"{self.consulta.duracion} minutos" if self.consulta.duracion else 'N/A')
        ]
        
        for label, value in info_data:
            row = tk.Frame(info_frame, bg='#f8fafc')
            row.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(
                row,
                text=label,
                font=('Arial', 10, 'bold'),
                bg='#f8fafc',
                fg='#64748b',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=value,
                font=('Arial', 10),
                bg='#f8fafc',
                fg='#1e293b',
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Notas
        if self.consulta.notas:
            self.crear_seccion(main_frame, "📝 Notas", self.consulta.notas)
        
        # Diagnóstico
        if self.consulta.diagnostico:
            self.crear_seccion(main_frame, "🔍 Diagnóstico", self.consulta.diagnostico)
        
        # Recomendaciones
        if self.consulta.recomend:
            self.crear_seccion(main_frame, "💡 Recomendaciones", self.consulta.recomend)
        
        # Botón cerrar
        tk.Button(
            main_frame,
            text="Cerrar",
            font=('Arial', 11, 'bold'),
            bg='#64748b',
            fg='white',
            cursor='hand2',
            padx=30,
            pady=10,
            bd=0,
            command=self.ventana.destroy
        ).pack(pady=(15, 0))
    
    def crear_seccion(self, parent, titulo, contenido):
        """Crea una sección con título y contenido"""
        tk.Label(
            parent,
            text=titulo,
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(anchor='w', pady=(10, 5))
        
        text_frame = tk.Frame(parent, bg='#f8fafc', relief='solid', bd=1)
        text_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        text_widget = tk.Text(
            text_frame,
            font=('Arial', 10),
            bg='#f8fafc',
            fg='#1e293b',
            height=3,
            wrap=tk.WORD,
            relief='flat',
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', contenido)
        text_widget.config(state='disabled')