"""
Ventana de gestión de pacientes
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.paciente_controller import PacienteController
from models.paciente import Paciente

class PacienteView:
    """Ventana para gestionar pacientes"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.controller = PacienteController()
        
        # Variables
        self.paciente_seleccionado = None
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar pacientes
        self.cargar_pacientes()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Limpiar frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # ===== TÍTULO =====
        titulo = tk.Label(
            self.parent_frame,
            text="Gestión de Pacientes",
            font=('Arial', 24, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        titulo.pack(anchor='w', pady=(0, 20))
        
        # ===== BARRA DE HERRAMIENTAS =====
        toolbar = tk.Frame(self.parent_frame, bg='#f8fafc')
        toolbar.pack(fill=tk.X, pady=(0, 20))
        
        # Botón Nuevo
        btn_nuevo = tk.Button(
            toolbar,
            text="➕ Nuevo Paciente",
            font=('Arial', 10, 'bold'),
            bg='#10b981',
            fg='white',
            activebackground='#059669',
            cursor='hand2',
            padx=15,
            py=8,
            bd=0,
            command=self.nuevo_paciente
        )
        btn_nuevo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Editar
        btn_editar = tk.Button(
            toolbar,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.editar_paciente
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Eliminar
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
            command=self.eliminar_paciente
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Buscador
        search_frame = tk.Frame(toolbar, bg='#f8fafc')
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Arial', 12),
            bg='#f8fafc'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.buscar_pacientes())
        
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 10),
            width=30
        )
        search_entry.pack(side=tk.LEFT)
        
        # ===== TABLA DE PACIENTES =====
        table_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columnas = ('ID', 'Nombre', 'Correo', 'Teléfono', 'Dirección', 'Fecha Registro')
        
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
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Correo', text='Correo')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Dirección', text='Dirección')
        self.tree.heading('Fecha Registro', text='Fecha Registro')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=200)
        self.tree.column('Correo', width=200)
        self.tree.column('Teléfono', width=120)
        self.tree.column('Dirección', width=250)
        self.tree.column('Fecha Registro', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind doble click
        self.tree.bind('<Double-1>', lambda e: self.editar_paciente())
        
        # Bind selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def cargar_pacientes(self):
        """Carga todos los pacientes en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            pacientes = self.controller.listar_pacientes()
            
            for paciente in pacientes:
                self.tree.insert('', tk.END, values=(
                    paciente.id_paciente,
                    paciente.nombre,
                    paciente.correo or '',
                    paciente.telefono,
                    paciente.direccion or '',
                    paciente.fecha_regist
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes:\n{str(e)}")
    
    def buscar_pacientes(self):
        """Busca pacientes por nombre o teléfono"""
        busqueda = self.search_var.get()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if busqueda:
                pacientes = self.controller.listar_pacientes(buscar=busqueda)
            else:
                pacientes = self.controller.listar_pacientes()
            
            for paciente in pacientes:
                self.tree.insert('', tk.END, values=(
                    paciente.id_paciente,
                    paciente.nombre,
                    paciente.correo or '',
                    paciente.telefono,
                    paciente.direccion or '',
                    paciente.fecha_regist
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar:\n{str(e)}")
    
    def on_select(self, event):
        """Maneja la selección de un paciente"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_paciente = item['values'][0]
            self.paciente_seleccionado = self.controller.obtener_paciente_por_id(id_paciente)
    
    def nuevo_paciente(self):
        """Abre ventana para crear nuevo paciente"""
        FormularioPaciente(self.parent_frame, self.controller, None, self.cargar_pacientes)
    
    def editar_paciente(self):
        """Abre ventana para editar paciente seleccionado"""
        if not self.paciente_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un paciente")
            return
        
        FormularioPaciente(self.parent_frame, self.controller, self.paciente_seleccionado, self.cargar_pacientes)
    
    def eliminar_paciente(self):
        """Elimina el paciente seleccionado"""
        if not self.paciente_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un paciente")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar al paciente:\n{self.paciente_seleccionado.nombre}?\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.eliminar_paciente(self.paciente_seleccionado.id_paciente)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_pacientes()
                    self.paciente_seleccionado = None
                else:
                    messagebox.showerror("Error", mensaje)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar:\n{str(e)}")


class FormularioPaciente:
    """Ventana de formulario para crear/editar paciente"""
    
    def __init__(self, parent, controller, paciente=None, callback=None):
        self.controller = controller
        self.paciente = paciente
        self.callback = callback
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Paciente" if not paciente else "Editar Paciente")
        self.ventana.geometry("500x450")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()  # Modal
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear formulario
        self.crear_formulario()
        
        # Si es edición, cargar datos
        if self.paciente:
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
            text="Nuevo Paciente" if not self.paciente else "Editar Paciente",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        titulo.pack(pady=(0, 20))
        
        # Campos
        campos = [
            ("Nombre *", "nombre"),
            ("Correo", "correo"),
            ("Teléfono *", "telefono"),
            ("Dirección", "direccion")
        ]
        
        self.entries = {}
        
        for label_text, field_name in campos:
            frame = tk.Frame(main_frame, bg='white')
            frame.pack(fill=tk.X, pady=8)
            
            label = tk.Label(
                frame,
                text=label_text,
                font=('Arial', 10, 'bold'),
                bg='white',
                fg='#1e293b'
            )
            label.pack(anchor='w')
            
            entry = ttk.Entry(frame, font=('Arial', 11))
            entry.pack(fill=tk.X, ipady=6)
            
            self.entries[field_name] = entry
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        btn_cancelar = tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Arial', 11),
            bg='#64748b',
            fg='white',
            activebackground='#475569',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.ventana.destroy
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=(10, 0))
        
        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            font=('Arial', 11, 'bold'),
            bg='#10b981',
            fg='white',
            activebackground='#059669',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.guardar
        )
        btn_guardar.pack(side=tk.RIGHT)
    
    def cargar_datos(self):
        """Carga los datos del paciente en el formulario"""
        self.entries['nombre'].insert(0, self.paciente.nombre)
        self.entries['correo'].insert(0, self.paciente.correo or '')
        self.entries['telefono'].insert(0, self.paciente.telefono)
        self.entries['direccion'].insert(0, self.paciente.direccion or '')
    
    def guardar(self):
        """Guarda el paciente"""
        # Obtener valores
        nombre = self.entries['nombre'].get().strip()
        correo = self.entries['correo'].get().strip()
        telefono = self.entries['telefono'].get().strip()
        direccion = self.entries['direccion'].get().strip()
        
        # Validar
        if not nombre:
            messagebox.showwarning("Campo Requerido", "El nombre es obligatorio")
            return
        
        if not telefono:
            messagebox.showwarning("Campo Requerido", "El teléfono es obligatorio")
            return
        
        try:
            if self.paciente:  # Editar
                self.paciente.nombre = nombre
                self.paciente.correo = correo if correo else None
                self.paciente.telefono = telefono
                self.paciente.direccion = direccion if direccion else None
                
                exito, mensaje = self.controller.actualizar_paciente(self.paciente)
            else:  # Nuevo
                nuevo_paciente = Paciente(
                    nombre=nombre,
                    correo=correo if correo else None,
                    telefono=telefono,
                    direccion=direccion if direccion else None
                )
                
                exito, mensaje, id_paciente = self.controller.crear_paciente(nuevo_paciente)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                if self.callback:
                    self.callback()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")