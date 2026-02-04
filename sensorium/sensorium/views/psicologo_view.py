"""
Ventana de gestión de psicólogos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.psicologo_controller import PsicologoController
from controllers.usuario_controller import UsuarioController
from models.psicologo import Psicologo
from models.usuario import Usuario

class PsicologoView:
    """Ventana para gestionar psicólogos"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.controller = PsicologoController()
        self.usuario_controller = UsuarioController()
        
        # Variables
        self.psicologo_seleccionado = None
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar psicólogos
        self.cargar_psicologos()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Limpiar frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # ===== TÍTULO =====
        titulo = tk.Label(
            self.parent_frame,
            text="Gestión de Psicólogos",
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
            text="➕ Nuevo Psicólogo",
            font=('Arial', 10, 'bold'),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.nuevo_psicologo
        )
        btn_nuevo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Editar
        btn_editar = tk.Button(
            toolbar,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#10b981',
            fg='white',
            activebackground='#059669',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.editar_psicologo
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
            command=self.eliminar_psicologo
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Filtro por especialidad
        tk.Label(
            toolbar,
            text="Especialidad:",
            font=('Arial', 10),
            bg='#f8fafc'
        ).pack(side=tk.RIGHT, padx=(10, 5))
        
        self.filtro_var = tk.StringVar(value="Todas")
        filtro_combo = ttk.Combobox(
            toolbar,
            textvariable=self.filtro_var,
            font=('Arial', 10),
            width=20,
            state='readonly'
        )
        filtro_combo.pack(side=tk.RIGHT)
        filtro_combo.bind('<<ComboboxSelected>>', lambda e: self.filtrar_por_especialidad())
        
        self.filtro_combo = filtro_combo
        
        # ===== TABLA DE PSICÓLOGOS =====
        table_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columnas = ('ID', 'Nombre', 'Correo', 'Especialidad', 'Cédula', 'Experiencia')
        
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
        self.tree.heading('Especialidad', text='Especialidad')
        self.tree.heading('Cédula', text='Cédula Profesional')
        self.tree.heading('Experiencia', text='Experiencia')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=200)
        self.tree.column('Correo', width=220)
        self.tree.column('Especialidad', width=180)
        self.tree.column('Cédula', width=120, anchor='center')
        self.tree.column('Experiencia', width=280)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind doble click
        self.tree.bind('<Double-1>', lambda e: self.editar_psicologo())
        
        # Bind selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def cargar_psicologos(self):
        """Carga todos los psicólogos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            psicologos = self.controller.listar_psicologos()
            
            # Actualizar filtro de especialidades
            especialidades = ['Todas'] + self.controller.obtener_especialidades()
            self.filtro_combo['values'] = especialidades
            
            for psicologo in psicologos:
                self.tree.insert('', tk.END, values=(
                    psicologo.id_psicologo,
                    psicologo.nombre or 'Sin nombre',
                    psicologo.correo or '',
                    psicologo.especialidad,
                    psicologo.cedula,
                    psicologo.experiencia or ''
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar psicólogos:\n{str(e)}")
    
    def filtrar_por_especialidad(self):
        """Filtra psicólogos por especialidad"""
        especialidad = self.filtro_var.get()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if especialidad == "Todas":
                psicologos = self.controller.listar_psicologos()
            else:
                psicologos = self.controller.listar_psicologos(especialidad=especialidad)
            
            for psicologo in psicologos:
                self.tree.insert('', tk.END, values=(
                    psicologo.id_psicologo,
                    psicologo.nombre or 'Sin nombre',
                    psicologo.correo or '',
                    psicologo.especialidad,
                    psicologo.cedula,
                    psicologo.experiencia or ''
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def on_select(self, event):
        """Maneja la selección de un psicólogo"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_psicologo = item['values'][0]
            self.psicologo_seleccionado = self.controller.obtener_psicologo_por_id(id_psicologo)
    
    def nuevo_psicologo(self):
        """Abre ventana para crear nuevo psicólogo"""
        FormularioPsicologo(self.parent_frame, self.controller, self.usuario_controller, None, self.cargar_psicologos)
    
    def editar_psicologo(self):
        """Abre ventana para editar psicólogo seleccionado"""
        if not self.psicologo_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un psicólogo")
            return
        
        FormularioPsicologo(self.parent_frame, self.controller, self.usuario_controller, self.psicologo_seleccionado, self.cargar_psicologos)
    
    def eliminar_psicologo(self):
        """Elimina el psicólogo seleccionado"""
        if not self.psicologo_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un psicólogo")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar al psicólogo:\n{self.psicologo_seleccionado.nombre}?\n\n"
            "Esto también eliminará su usuario del sistema.\n"
            "Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.eliminar_psicologo(self.psicologo_seleccionado.id_psicologo)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_psicologos()
                    self.psicologo_seleccionado = None
                else:
                    messagebox.showerror("Error", mensaje)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar:\n{str(e)}")


class FormularioPsicologo:
    """Ventana de formulario para crear/editar psicólogo"""
    
    def __init__(self, parent, controller, usuario_controller, psicologo=None, callback=None):
        self.controller = controller
        self.usuario_controller = usuario_controller
        self.psicologo = psicologo
        self.callback = callback
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Psicólogo" if not psicologo else "Editar Psicólogo")
        self.ventana.geometry("550x650")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear formulario
        self.crear_formulario()
        
        # Si es edición, cargar datos
        if self.psicologo:
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
            text="Nuevo Psicólogo" if not self.psicologo else "Editar Psicólogo",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        titulo.pack(pady=(0, 20))
        
        # Nota sobre usuario
        if not self.psicologo:
            nota = tk.Label(
                main_frame,
                text="Se creará un usuario de acceso al sistema",
                font=('Arial', 9, 'italic'),
                bg='white',
                fg='#64748b'
            )
            nota.pack(pady=(0, 10))
        
        # Campos
        campos = [
            ("Nombre Completo *", "nombre"),
            ("Correo Electrónico *", "correo"),
            ("Especialidad *", "especialidad"),
            ("Cédula Profesional *", "cedula"),
            ("Experiencia", "experiencia")
        ]
        
        if not self.psicologo:
            campos.append(("Contraseña *", "password"))
        
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
            
            if field_name == "experiencia":
                # Text area para experiencia
                text = tk.Text(frame, font=('Arial', 10), height=3, width=40)
                text.pack(fill=tk.X)
                self.entries[field_name] = text
            elif field_name == "password":
                # Entry con show para contraseña
                entry = ttk.Entry(frame, font=('Arial', 11), show='•')
                entry.pack(fill=tk.X, ipady=6)
                self.entries[field_name] = entry
            else:
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
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.guardar
        )
        btn_guardar.pack(side=tk.RIGHT)
    
    def cargar_datos(self):
        """Carga los datos del psicólogo en el formulario"""
        self.entries['nombre'].insert(0, self.psicologo.nombre or '')
        self.entries['correo'].insert(0, self.psicologo.correo or '')
        self.entries['especialidad'].insert(0, self.psicologo.especialidad)
        self.entries['cedula'].insert(0, self.psicologo.cedula)
        
        if self.psicologo.experiencia:
            self.entries['experiencia'].insert('1.0', self.psicologo.experiencia)
    
    def guardar(self):
        """Guarda el psicólogo"""
        # Obtener valores
        nombre = self.entries['nombre'].get().strip()
        correo = self.entries['correo'].get().strip()
        especialidad = self.entries['especialidad'].get().strip()
        cedula = self.entries['cedula'].get().strip()
        experiencia = self.entries['experiencia'].get('1.0', tk.END).strip()
        
        # Validar campos obligatorios
        if not all([nombre, correo, especialidad, cedula]):
            messagebox.showwarning("Campos Requeridos", "Por favor completa todos los campos obligatorios")
            return
        
        if not self.psicologo:
            password = self.entries['password'].get()
            if not password or len(password) < 6:
                messagebox.showwarning("Contraseña", "La contraseña debe tener al menos 6 caracteres")
                return
        
        try:
            if self.psicologo:  # Editar
                self.psicologo.especialidad = especialidad
                self.psicologo.experiencia = experiencia if experiencia else None
                self.psicologo.cedula = cedula
                
                exito, mensaje = self.controller.actualizar_psicologo(self.psicologo)
                
                # También actualizar usuario
                usuario = self.usuario_controller.obtener_usuario_por_id(self.psicologo.id_usuario)
                if usuario:
                    usuario.nombre = nombre
                    usuario.correo = correo
                    self.usuario_controller.actualizar_usuario(usuario)
            
            else:  # Nuevo
                # Primero crear el usuario
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    correo=correo,
                    contraseña=password,
                    rol='psicologo'
                )
                
                exito_usuario, mensaje_usuario, id_usuario = self.usuario_controller.crear_usuario(nuevo_usuario)
                
                if not exito_usuario:
                    messagebox.showerror("Error", f"Error al crear usuario:\n{mensaje_usuario}")
                    return
                
                # Luego crear el psicólogo
                nuevo_psicologo = Psicologo(
                    id_usuario=id_usuario,
                    especialidad=especialidad,
                    experiencia=experiencia if experiencia else None,
                    cedula=cedula
                )
                
                exito, mensaje, id_psicologo = self.controller.crear_psicologo(nuevo_psicologo)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                if self.callback:
                    self.callback()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")