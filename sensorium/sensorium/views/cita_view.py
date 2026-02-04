"""
Ventana de gestión de citas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from tkcalendar import DateEntry
from controllers.cita_controller import CitaController
from controllers.paciente_controller import PacienteController
from controllers.psicologo_controller import PsicologoController
from models.cita import Cita

class CitaView:
    """Ventana para gestionar citas"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.controller = CitaController()
        self.paciente_controller = PacienteController()
        self.psicologo_controller = PsicologoController()
        
        # Variables
        self.cita_seleccionada = None
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar citas
        self.cargar_citas()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Limpiar frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # ===== TÍTULO =====
        titulo = tk.Label(
            self.parent_frame,
            text="Gestión de Citas",
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
            text="➕ Nueva Cita",
            font=('Arial', 10, 'bold'),
            bg='#8b5cf6',
            fg='white',
            activebackground='#7c3aed',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.nueva_cita
        )
        btn_nueva.pack(side=tk.LEFT, padx=(0, 10))
        
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
            command=self.editar_cita
        )
        btn_editar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_cancelar = tk.Button(
            toolbar,
            text="❌ Cancelar Cita",
            font=('Arial', 10, 'bold'),
            bg='#f59e0b',
            fg='white',
            activebackground='#d97706',
            cursor='hand2',
            padx=15,
            pady=8,
            bd=0,
            command=self.cancelar_cita
        )
        btn_cancelar.pack(side=tk.LEFT, padx=(0, 10))
        
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
            command=self.eliminar_cita
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Filtro por estado
        tk.Label(
            toolbar,
            text="Estado:",
            font=('Arial', 10),
            bg='#f8fafc'
        ).pack(side=tk.RIGHT, padx=(10, 5))
        
        self.filtro_var = tk.StringVar(value="Todas")
        filtro_combo = ttk.Combobox(
            toolbar,
            textvariable=self.filtro_var,
            font=('Arial', 10),
            values=['Todas', 'Programada', 'Completada', 'Cancelada'],
            width=15,
            state='readonly'
        )
        filtro_combo.pack(side=tk.RIGHT)
        filtro_combo.bind('<<ComboboxSelected>>', lambda e: self.filtrar_citas())
        
        # ===== TABLA DE CITAS =====
        table_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columnas = ('ID', 'Fecha', 'Hora', 'Paciente', 'Psicólogo', 'Especialidad', 'Modalidad', 'Estado')
        
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
        self.tree.heading('Hora', text='Hora')
        self.tree.heading('Paciente', text='Paciente')
        self.tree.heading('Psicólogo', text='Psicólogo')
        self.tree.heading('Especialidad', text='Especialidad')
        self.tree.heading('Modalidad', text='Modalidad')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Fecha', width=100, anchor='center')
        self.tree.column('Hora', width=80, anchor='center')
        self.tree.column('Paciente', width=180)
        self.tree.column('Psicólogo', width=180)
        self.tree.column('Especialidad', width=150)
        self.tree.column('Modalidad', width=100, anchor='center')
        self.tree.column('Estado', width=100, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Aplicar colores por estado
        self.tree.tag_configure('Programada', background='#dbeafe')
        self.tree.tag_configure('Completada', background='#d1fae5')
        self.tree.tag_configure('Cancelada', background='#fee2e2')
        
        # Bind eventos
        self.tree.bind('<Double-1>', lambda e: self.editar_cita())
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def cargar_citas(self):
        """Carga todas las citas en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            citas = self.controller.listar_citas()
            
            for cita in citas:
                tag = cita.estado
                self.tree.insert('', tk.END, values=(
                    cita.id_cita,
                    cita.fecha,
                    cita.hora,
                    cita.nombre_paciente or '',
                    cita.nombre_psicologo or '',
                    cita.especialidad or '',
                    cita.modalidad,
                    cita.estado
                ), tags=(tag,))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar citas:\n{str(e)}")
    
    def filtrar_citas(self):
        """Filtra citas por estado"""
        estado = self.filtro_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if estado == "Todas":
                citas = self.controller.listar_citas()
            else:
                citas = self.controller.listar_citas(estado=estado)
            
            for cita in citas:
                tag = cita.estado
                self.tree.insert('', tk.END, values=(
                    cita.id_cita,
                    cita.fecha,
                    cita.hora,
                    cita.nombre_paciente or '',
                    cita.nombre_psicologo or '',
                    cita.especialidad or '',
                    cita.modalidad,
                    cita.estado
                ), tags=(tag,))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def on_select(self, event):
        """Maneja la selección de una cita"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            id_cita = item['values'][0]
            self.cita_seleccionada = self.controller.obtener_cita_por_id(id_cita)
    
    def nueva_cita(self):
        """Abre ventana para crear nueva cita"""
        FormularioCita(self.parent_frame, self.controller, self.paciente_controller, 
                      self.psicologo_controller, None, self.cargar_citas)
    
    def editar_cita(self):
        """Abre ventana para editar cita seleccionada"""
        if not self.cita_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una cita")
            return
        
        FormularioCita(self.parent_frame, self.controller, self.paciente_controller,
                      self.psicologo_controller, self.cita_seleccionada, self.cargar_citas)
    
    def cancelar_cita(self):
        """Cancela la cita seleccionada"""
        if not self.cita_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una cita")
            return
        
        if self.cita_seleccionada.estado == "Cancelada":
            messagebox.showinfo("Información", "Esta cita ya está cancelada")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Cancelación",
            f"¿Estás seguro de cancelar la cita?\n\n"
            f"Paciente: {self.cita_seleccionada.nombre_paciente}\n"
            f"Fecha: {self.cita_seleccionada.fecha} {self.cita_seleccionada.hora}"
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.cancelar_cita(self.cita_seleccionada.id_cita)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_citas()
                else:
                    messagebox.showerror("Error", mensaje)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar:\n{str(e)}")
    
    def eliminar_cita(self):
        """Elimina la cita seleccionada"""
        if not self.cita_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una cita")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar permanentemente esta cita?\n\n"
            f"Paciente: {self.cita_seleccionada.nombre_paciente}\n"
            f"Fecha: {self.cita_seleccionada.fecha} {self.cita_seleccionada.hora}\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.eliminar_cita(self.cita_seleccionada.id_cita)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.cargar_citas()
                    self.cita_seleccionada = None
                else:
                    messagebox.showerror("Error", mensaje)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar:\n{str(e)}")


class FormularioCita:
    """Ventana de formulario para crear/editar cita"""
    
    def __init__(self, parent, controller, paciente_controller, psicologo_controller, 
                 cita=None, callback=None):
        self.controller = controller
        self.paciente_controller = paciente_controller
        self.psicologo_controller = psicologo_controller
        self.cita = cita
        self.callback = callback
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nueva Cita" if not cita else "Editar Cita")
        self.ventana.geometry("500x550")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Cargar datos para combos
        self.pacientes = self.paciente_controller.listar_pacientes()
        self.psicologos = self.psicologo_controller.listar_psicologos()
        
        # Crear formulario
        self.crear_formulario()
        
        # Si es edición, cargar datos
        if self.cita:
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
            text="Nueva Cita" if not self.cita else "Editar Cita",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        titulo.pack(pady=(0, 20))
        
        # Paciente
        tk.Label(main_frame, text="Paciente *", font=('Arial', 10, 'bold'), 
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.paciente_var = tk.StringVar()
        paciente_combo = ttk.Combobox(
            main_frame,
            textvariable=self.paciente_var,
            font=('Arial', 11),
            state='readonly'
        )
        paciente_combo['values'] = [f"{p.id_paciente} - {p.nombre}" for p in self.pacientes]
        paciente_combo.pack(fill=tk.X, ipady=6, pady=(5, 10))
        self.paciente_combo = paciente_combo
        
        # Psicólogo
        tk.Label(main_frame, text="Psicólogo *", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.psicologo_var = tk.StringVar()
        psicologo_combo = ttk.Combobox(
            main_frame,
            textvariable=self.psicologo_var,
            font=('Arial', 11),
            state='readonly'
        )
        psicologo_combo['values'] = [f"{p.id_psicologo} - {p.nombre} ({p.especialidad})" 
                                      for p in self.psicologos]
        psicologo_combo.pack(fill=tk.X, ipady=6, pady=(5, 10))
        self.psicologo_combo = psicologo_combo
        
        # Fecha
        tk.Label(main_frame, text="Fecha *", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        # Nota: tkcalendar requiere instalación: pip install tkcalendar
        # Si no está disponible, usar Entry normal
        try:
            from tkcalendar import DateEntry
            self.fecha_entry = DateEntry(
                main_frame,
                font=('Arial', 11),
                date_pattern='yyyy-mm-dd',
                mindate=date.today()
            )
        except:
            self.fecha_entry = ttk.Entry(main_frame, font=('Arial', 11))
            self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        self.fecha_entry.pack(fill=tk.X, ipady=6, pady=(5, 10))
        
        # Hora
        tk.Label(main_frame, text="Hora *", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        hora_frame = tk.Frame(main_frame, bg='white')
        hora_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.hora_var = tk.StringVar(value="09:00")
        hora_combo = ttk.Combobox(
            hora_frame,
            textvariable=self.hora_var,
            font=('Arial', 11),
            width=10,
            state='readonly'
        )
        horas = [f"{h:02d}:{m:02d}" for h in range(8, 20) for m in [0, 30]]
        hora_combo['values'] = horas
        hora_combo.pack(side=tk.LEFT)
        
        # Modalidad
        tk.Label(main_frame, text="Modalidad *", font=('Arial', 10, 'bold'),
                bg='white', fg='#1e293b').pack(anchor='w')
        
        self.modalidad_var = tk.StringVar(value="Presencial")
        modalidad_frame = tk.Frame(main_frame, bg='white')
        modalidad_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Radiobutton(modalidad_frame, text="Presencial", variable=self.modalidad_var,
                       value="Presencial").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(modalidad_frame, text="Virtual", variable=self.modalidad_var,
                       value="Virtual").pack(side=tk.LEFT)
        
        # Estado (solo en edición)
        if self.cita:
            tk.Label(main_frame, text="Estado *", font=('Arial', 10, 'bold'),
                    bg='white', fg='#1e293b').pack(anchor='w')
            
            self.estado_var = tk.StringVar(value=self.cita.estado)
            estado_combo = ttk.Combobox(
                main_frame,
                textvariable=self.estado_var,
                font=('Arial', 11),
                values=['Programada', 'Completada', 'Cancelada'],
                state='readonly'
            )
            estado_combo.pack(fill=tk.X, ipady=6, pady=(5, 10))
        
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
            bg='#8b5cf6',
            fg='white',
            cursor='hand2',
            padx=20,
            pady=10,
            bd=0,
            command=self.guardar
        ).pack(side=tk.RIGHT)
    
    def cargar_datos(self):
        """Carga los datos de la cita en el formulario"""
        # Buscar y seleccionar paciente
        for i, p in enumerate(self.pacientes):
            if p.id_paciente == self.cita.id_paciente:
                self.paciente_combo.current(i)
                break
        
        # Buscar y seleccionar psicólogo
        for i, p in enumerate(self.psicologos):
            if p.id_psicologo == self.cita.id_psicologo:
                self.psicologo_combo.current(i)
                break
        
        # Fecha y hora
        try:
            self.fecha_entry.set_date(self.cita.fecha)
        except:
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, str(self.cita.fecha))
        
        self.hora_var.set(str(self.cita.hora)[:5])
        self.modalidad_var.set(self.cita.modalidad)
    
    def guardar(self):
        """Guarda la cita"""
        # Validar selecciones
        if not self.paciente_var.get():
            messagebox.showwarning("Campo Requerido", "Selecciona un paciente")
            return
        
        if not self.psicologo_var.get():
            messagebox.showwarning("Campo Requerido", "Selecciona un psicólogo")
            return
        
        # Obtener IDs
        id_paciente = int(self.paciente_var.get().split(' - ')[0])
        id_psicologo = int(self.psicologo_var.get().split(' - ')[0])
        
        # Obtener fecha
        try:
            fecha_cita = self.fecha_entry.get_date() if hasattr(self.fecha_entry, 'get_date') else date.fromisoformat(self.fecha_entry.get())
        except:
            messagebox.showerror("Error", "Formato de fecha inválido")
            return
        
        hora = self.hora_var.get()
        modalidad = self.modalidad_var.get()
        estado = self.estado_var.get() if self.cita else "Programada"
        
        try:
            if self.cita:  # Editar
                self.cita.id_paciente = id_paciente
                self.cita.id_psicologo = id_psicologo
                self.cita.fecha = fecha_cita
                self.cita.hora = hora
                self.cita.modalidad = modalidad
                self.cita.estado = estado
                
                exito, mensaje = self.controller.actualizar_cita(self.cita)
            else:  # Nueva
                nueva_cita = Cita(
                    id_paciente=id_paciente,
                    id_psicologo=id_psicologo,
                    fecha=fecha_cita,
                    hora=hora,
                    modalidad=modalidad,
                    estado="Programada"
                )
                
                exito, mensaje, id_cita = self.controller.crear_cita(nueva_cita)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                if self.callback:
                    self.callback()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")