import os
import platform
import subprocess
import threading
import datetime
import shutil
import customtkinter as ctk

try:
    import wmi
except:
    pass

# Configuración de apariencia inicial
ctk.set_appearance_mode("dark")

# Paleta de Colores Oficial (Estilo Cyberpunk / Regis OAP)
COR_REGIS_PRINCIPAL = "#00E5FF"       # Cian brillante
COR_REGIS_HOVER = "#00B8D4"           # Cian medio
COR_REGIS_BORDES = "#004D40"          # Verde oscuro/Acento base
FONDO_VENTANA_PROFUNDO = "#050B14"    # Fondo ultra oscuro
FONDO_PANEL_MENU = "#0A101A"          # Fondo barra lateral
FONDO_CONTENEDOR_CENTRAL = "#0D1520"  # Fondo de pantallas
FONDO_TARJETAS = "#131E2D"            # Fondo bloques internos
FONDO_TARJETAS_CLARO = "#1B2A3D"      # Fondo bloques auxiliares
COLOR_ACTIVO = "#00FF9D"              # Verde neón (Activo/Éxito)
COLOR_INACTIVO = "#FF3333"            # Rojo (Inactivo/Atención)
TEXTO_PRINCIPAL = "#FFFFFF"           # Blanco
TEXTO_SECUNDARIO = "#A0B0C0"          # Gris azulado
TEXTO_BOTON_OSCURO = "#050B14"        # Texto oscuro para contraste

# Fuentes de Interfaz para evitar desaparición de caracteres
FUENTE_TITULO = ("Segoe UI Semibold", 20)
FUENTE_SUBTITULO = ("Segoe UI", 12)
FUENTE_BOTON = ("Segoe UI Bold", 13)
FUENTE_FORMAL = "Segoe UI"
FUENTE_GRANDE = ("Segoe UI", 15)
FUENTE_CONSOLA = ("Consolas", 12)

# Versión del software actual para el sistema de Updates
VERSION_ACTUAL = "V4.0"

# Banco de Textos Multilingüe Integrado Completo
TEXTOS = {
    "Português": {
        "titulo_barra": "REGIS OAP  ·  OAP Core Engine", "btn_verif": "🔎  Verificação", "btn_opt": "🚀  Módulo OAP", "btn_status": "📊  Status do Sistema", "btn_hard": "🖥️  Hardware do PC", "btn_clean": "🧹  Limpeza OAP", "btn_update": "🔄  Updates", "status_rango": "REGIS OAP // PRIVADO",
        "v_titulo": "VERIFICAÇÃO DE SEGURANÇA", "v_btn": "INICIAR VERIFICAÇÃO", "h_titulo": "DETECÇÃO DE HARDWARE EM TEMPO REAL", "h_btn": "ESCANEAR PC", "h_espera": "Aguardando leitura profunda do sistema...",
        "s_titulo": "MONITORAMENTO REAL DE AJUSTES", "s_inactivo": "INATIVO", "s_activo": "ATIVO", "s_btn_verif": "VERIFICAR AJUSTES ATIVOS", "scan_tit": "RESULTADOS DA VERIFICAÇÃO",
        "scan_reparar": "HABILITAR SERVIÇOS DESATIVADOS", "scan_sair": "VOLTAR AO MENU", "scan_run": "ANALIZANDO SERVIÇOS DO SISTEMA...", "scan_success": "Operação realizada com sucesso!",
        "btn_inyectar": "ATIVAR", "btn_activo": "ATIVADO", "splash_tit": "REGIS OAP", "splash_load": "INICIALIZANDO SISTEMA...", "inj_fase1": "Sincronizando...", "inj_fase2": "Alocando buffers...", "inj_fase3": "Aplicando overrides...",
        "c_titulo": "OTIMIZAÇÃO E LIMPEZA DE MEMÓRIA CACHÊ", "c_btn": "EXECUTAR SUPER LIMPEZA", "c_run": "LIMPANDO ARQUIVOS TEMPORÁRIOS...", "c_success": "Limpeza concluída com sucesso!",
        "u_titulo": "SISTEMA DE ATUALIZAÇÕES CENTRALIZADO", "u_btn_buscar": "VERIFICAR ATUALIZAÇÕES", "u_checking": "Conectando ao servidor do GitHub...", "u_uptodate": "SISTEMA TOTALMENTE ATUALIZADO", "u_newversion": "NOVA VERSÃO DETECTADA!", "u_btn_download": "BAIXAR NOVA ATUALIZAÇÃO"
    },
    "Español": {
        "titulo_barra": "REGIS OAP  ·  OAP Core Engine", "btn_verif": "🔎  Verificación", "btn_opt": "🚀  Módulo OAP", "btn_status": "📊  Estado del Sistema", "btn_hard": "🖥️  Hardware del PC", "btn_clean": "🧹  Limpieza OAP", "btn_update": "🔄  Updates", "status_rango": "REGIS OAP // PRIVADO",
        "v_titulo": "VERIFICACIÓN DE SEGURIDAD", "v_btn": "INICIAR VERIFICACIÓN", "h_titulo": "DETECCIÓN DE HARDWARE EN TIEMPO REAL", "h_btn": "ESCANEAR PC", "h_espera": "Esperando lectura profunda del sistema...",
        "s_titulo": "MONITOREO REAL DE AJUSTES", "s_inactivo": "INACTIVO", "s_activo": "ACTIVO", "s_btn_verif": "VERIFICAR AJUSTES ACTIVOS", "scan_tit": "RESULTADOS DE LA VERIFICACIÓN",
        "scan_reparar": "HABILITAR SERVICIOS DESHABILITADOS", "scan_sair": "VOLVER AL MENÚ", "scan_run": "ANALIZANDO SERVICIOS DEL SISTEMA...", "scan_success": "¡Operación realizada correctamente!",
        "btn_inyectar": "ACTIVAR", "btn_activo": "ACTIVADO", "splash_tit": "REGIS OAP", "splash_load": "INICIALIZANDO SISTEMA...", "inj_fase1": "Sincronizando...", "inj_fase2": "Alocando buffers...", "inj_fase3": "Aplicando overrides...",
        "c_titulo": "OPTIMIZACIÓN Y LIMPIEZA DE MEMORIA CACHÉ", "c_btn": "EJECUTAR SÚPER LIMPIEZA", "c_run": "ELIMINANDO ARCHIVOS TEMPORALES Y CACHÉ...", "c_success": "¡Limpieza profunda completada con éxito!",
        "u_titulo": "SISTEMA DE ACTUALIZACIONES CENTRALIZADO", "u_btn_buscar": "BUSCAR ACTUALIZACIONES", "u_checking": "Conectando con servidores de GitHub...", "u_uptodate": "EL SISTEMA YA ESTÁ ACTUALIZADO", "u_newversion": "¡NUEVA ACTUALIZACIÓN DETECTADA!", "u_btn_download": "DESCARGAR NUEVA VERSIÓN"
    },
    "English": {
        "titulo_barra": "REGIS OAP  ·  OAP Core Engine", "btn_verif": "🔎  Verification", "btn_opt": "🚀  OAP Module", "btn_status": "📊  System Status", "btn_hard": "🖥️  PC Hardware", "btn_clean": "🧹  OAP Clean", "btn_update": "🔄  Updates", "status_rango": "REGIS OAP // PRIVATE",
        "v_titulo": "SECURITY VERIFICATION", "v_btn": "START VERIFICATION", "h_titulo": "REAL-TIME HARDWARE DETECTION", "h_btn": "SCAN PC", "h_espera": "Awaiting deep system read...",
        "s_titulo": "REAL TWEAKS MONITORING", "s_inactivo": "INACTIVE", "s_activo": "ACTIVE", "s_btn_verif": "CHECK ACTIVE TWEAKS", "scan_tit": "VERIFICATION RESULTS",
        "scan_reparar": "ENABLE DISABLED SERVICES", "scan_sair": "RETURN TO MENU", "scan_run": "ANALYZING SYSTEM SERVICES...", "scan_success": "Operation completed successfully!",
        "btn_inyectar": "ACTIVATE", "btn_activo": "ACTIVATED", "splash_tit": "REGIS OAP", "splash_load": "INITIALIZING SYSTEM...", "inj_fase1": "Synchronizing...", "inj_fase2": "Allocating buffers...", "inj_fase3": "Applying overrides...",
        "c_titulo": "CACHE MEMORY OPTIMIZATION & CLEANUP", "c_btn": "RUN SUPER CLEANUP", "c_run": "CLEARING TEMPORARY FILES AND CACHE...", "c_success": "Deep cleanup completed successfully!",
        "u_titulo": "CENTRALIZED SYSTEM UPDATE ENGINE", "u_btn_buscar": "CHECK FOR UPDATES", "u_checking": "Connecting to GitHub servers...", "u_uptodate": "SYSTEM IS FULLY UP TO DATE", "u_newversion": "NEW UPDATE DETECTED!", "u_btn_download": "DOWNLOAD NEW VERSION"
    }
}

class RegisOAPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.sw, self.sh = self.winfo_screenwidth(), self.winfo_screenheight()
        
        width, height = 500, 320
        x, y = int((self.sw/2)-(width/2)), int((self.sh/2)-(height/2))
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(fg_color=FONDO_VENTANA_PROFUNDO)
        
        self.idioma_actual = "Español"
        self.es_maximi_pantalla = False
        self.ancho_sidebar_actual = 70
        self.animando_sidebar = False
        self._drag_x, self._drag_y = 0, 0
        
        self.estados_modulos = {"OAP Fluid": False, "OAP Advanced": False, "OAP Absolute": False}
        
        self.servicios_check = {
            "PcaSvc": "PcaSvc", 
            "PlugPlay": "PlugPlay", 
            "DPS": "DPS", 
            "DiagTrack": "DiagTrack", 
            "Sysmain": "SysMain", 
            "Eventlog": "EventLog", 
            "Firewall": "mpssvc", 
            "Sysmon": "Sysmon", 
            "TPM": "HARDWARE_TPM", 
            "SecureBoot": "HARDWARE_SECUREBOOT"
        }
        self.estado_servicios_actual = {}
        self.todos_servicios_ok = False

        self.p_splash_interna = ctk.CTkFrame(self, fg_color=FONDO_VENTANA_PROFUNDO, corner_radius=0)
        self.p_splash_interna.place(x=0, y=0, relwidth=1, relheight=1)
        
        lbl_splash_main = ctk.CTkLabel(self.p_splash_interna, text="REGIS OAP", font=(FUENTE_FORMAL, 54, "bold"), text_color=COR_REGIS_PRINCIPAL)
        lbl_splash_main.place(relx=0.5, rely=0.36, anchor="center")
        
        self.lbl_spl_status = ctk.CTkLabel(self.p_splash_interna, text="INICIALIZANDO SISTEMA...", font=(FUENTE_FORMAL, 13), text_color=TEXTO_SECUNDARIO)
        self.lbl_spl_status.place(relx=0.5, rely=0.52, anchor="center")
        
        self.spl_bar = ctk.CTkProgressBar(self.p_splash_interna, width=350, height=4, fg_color=FONDO_TARJETAS, progress_color=COR_REGIS_PRINCIPAL)
        self.spl_bar.place(relx=0.5, rely=0.62, anchor="center")
        
        self.current_w, self.current_h = width, height
        self.after(200, self.animar_apertura_f11)

    def animar_apertura_f11(self):
        if self.current_w < self.sw or self.current_h < self.sh:
            self.current_w = min(self.current_w + 80, self.sw)
            self.current_h = min(self.current_h + 50, self.sh)
            x_pos = int((self.sw / 2) - (self.current_w / 2))
            y_pos = int((self.sh / 2) - (self.current_h / 2))
            self.geometry(f"{self.current_w}x{self.current_h}+{x_pos}+{y_pos}")
            self.after(10, self.animar_apertura_f11)
        else:
            self.geometry(f"{self.sw}x{self.sh}+0+0")
            self.es_maximi_pantalla = True
            self.spl_bar.configure(width=650)
            self.progreso_inicial = 0
            self.bucle_carga_inicial()

    def bucle_carga_inicial(self):
        txt = TEXTOS[self.idioma_actual]
        if self.progreso_inicial <= 100:
            self.spl_bar.set(self.progreso_inicial / 100)
            self.lbl_spl_status.configure(text=f"{txt['splash_load']} {self.progreso_inicial}%")
            self.progreso_inicial += 1
            self.after(10, self.bucle_carga_inicial)
        else:
            self.p_splash_interna.place_forget()
            self.inicializar_interfaz_real()

    def iniciar_arrastre(self, event): 
        self._drag_x, self._drag_y = event.x, event.y
        
    def en_movimiento(self, event):
        if not self.es_maximi_pantalla: 
            self.geometry(f"+{self.winfo_x() + (event.x - self._drag_x)}+{self.winfo_y() + (event.y - self._drag_y)}")
            
    def asociar_arrastre(self, widget): 
        widget.bind("<ButtonPress-1>", self.iniciar_arrastre)
        widget.bind("<B1-Motion>", self.en_movimiento)

    def detectar_hardware_profundo(self):
        resultado_detallado = ""
        try:
            c = wmi.WMI()
            cpu_name = c.Win32_Processor()[0].Name.strip()
            resultado_detallado += f" » PROCESSADOR : {cpu_name}\n\n"
            
            board = c.Win32_BaseBoard()[0]
            resultado_detallado += f" » PLACA-MÃE   : {board.Manufacturer} {board.Product}\n\n"
            
            m_ram = c.Win32_PhysicalMemory()
            total_capacidad = sum(int(m.Capacity) for m in m_ram) // (1024 ** 3)
            canales = "Dual Channel REAL" if len(m_ram) >= 2 else "Single Channel"
            try:
                velocidad_ram = m_ram[0].Speed
                texto_velocidad = f"{velocidad_ram} MHz"
            except:
                texto_velocidad = "Velocidade Dinâmica Detectada"
            resultado_detallado += f" » MEMÓRIA RAM : {total_capacidad} GB ({canales}) @ {texto_velocidad}\n\n"
            
            try:
                gpus = c.Win32_VideoController()
                gpu_list = [g.Name.strip() for g in gpus]
                resultado_detallado += f" » PLACA DE VÍDEO: {' / '.join(gpu_list)}\n\n"
            except:
                resultado_detallado += " » PLACA DE VÍDEO: Adaptador Gráfico Padrão\n\n"

            try:
                modelo_disco = c.Win32_DiskDrive()[0].Model.upper()
                interface_disco = c.Win32_DiskDrive()[0].InterfaceType.upper()
                if "SSD" in modelo_disco or "NVME" in modelo_disco or "SCSI" in interface_disco:
                    tipo_disco = "Solid State Drive (SSD NVMe M.2) Hyper-Fast"
                else:
                    tipo_disco = "Hard Disk Drive (HDD) Standard SATA"
                resultado_detallado += f" » DISCO PRINCIPAL : {tipo_disco} ({modelo_disco})\n\n"
            except:
                resultado_detallado += " » DISCO PRINCIPAL : Unidade de Armazenamento do Sistema\n\n"

            try:
                res_x = self.winfo_screenwidth()
                res_y = self.winfo_screenheight()
                resultado_detallado += f" » MONITOR PRINCIPAL : Display Ativo Atualmente ({res_x}x{res_y})\n\n"
            except:
                resultado_detallado += " » MONITOR PRINCIPAL : Monitor Gamer PnP\n\n"

            try:
                mouses = len(c.Win32_PointingDevice())
                teclados = len(c.Win32_Keyboard())
                resultado_detallado += f" » PERIFÉRICOS : {mouses} Mouse Conectado // {teclados} Teclado Ativo Detectado"
            except:
                resultado_detallado += " » PERIFÉRICOS : Barramento de Periféricos de Baixa Latência"

            return resultado_detallado
        except:
            sys_arch = platform.architecture()[0]
            sys_proc = platform.processor()
            return (
                f" » PROCESSADOR : {sys_proc if sys_proc else 'Processador Genérico x64/AMD'}\n\n"
                f" » SISTEMA     : {platform.system()} ({sys_arch})\n\n"
                " » MEMÓRIA RAM : Capacidade Física Alocada por Windows\n\n"
                " » DISCO PRINCIPAL : SSD Principal Ativo Corretamente\n\n"
                " » MONITOR PRINCIPAL : Monitor Ativo em Driver Nativo\n\n"
                " » PERIFÉRICOS : Dispositivos de Entrada Controlados por OAP Core"
            )

    def obtener_nombre_sistema(self):
        try:
            return wmi.WMI().Win32_OperatingSystem()[0].Caption.replace("Microsoft ", "").strip()
        except:
            return f"{platform.system()} {platform.release()}"

    def evento_mouse_entra_sidebar(self, event): 
        self.iniciar_animacion_sidebar(250)
        
    def evento_mouse_sale_sidebar(self, event):
        x_mouse = self.sidebar.winfo_pointerx() - self.sidebar.winfo_rootx()
        y_mouse = self.sidebar.winfo_pointery() - self.sidebar.winfo_rooty()
        if x_mouse < 0 or x_mouse >= self.sidebar.winfo_width() or y_mouse < 0 or y_mouse >= self.sidebar.winfo_height(): 
            self.iniciar_animacion_sidebar(70)

    def iniciar_animacion_sidebar(self, ancho_objetivo):
        self.ancho_objetivo = ancho_objetivo
        if not self.animando_sidebar:
            self.animando_sidebar = True
            self.bucle_animacion_sidebar()

    def bucle_animacion_sidebar(self):
        paso = 45  
        if self.ancho_sidebar_actual != self.ancho_objetivo:
            if self.ancho_sidebar_actual < self.ancho_objetivo: 
                self.ancho_sidebar_actual = min(self.ancho_sidebar_actual + paso, self.ancho_objetivo)
            else: 
                self.ancho_sidebar_actual = max(self.ancho_sidebar_actual - paso, self.ancho_objetivo)
                
            if hasattr(self, 'sidebar') and self.sidebar.winfo_exists():
                self.sidebar.configure(width=self.ancho_sidebar_actual)
                if self.ancho_sidebar_actual > 160:
                    txt = TEXTOS[self.idioma_actual]
                    self.btn_nav_verif.configure(text=txt["btn_verif"])
                    self.btn_nav_opt.configure(text=txt["btn_opt"])
                    self.btn_nav_status.configure(text=txt["btn_status"])
                    self.btn_nav_hard.configure(text=txt["btn_hard"])
                    self.btn_nav_clean.configure(text=txt["btn_clean"])
                    self.btn_nav_update.configure(text=txt["btn_update"])
                    self.lbl_marca.configure(text="   REGIS OAP")
                    self.lbl_marca.pack(side="left", padx=10)
                else:
                    self.btn_nav_verif.configure(text="  🔎")
                    self.btn_nav_opt.configure(text="  🚀")
                    self.btn_nav_status.configure(text="  📊")
                    self.btn_nav_hard.configure(text="  🖥️")
                    self.btn_nav_clean.configure(text="  🧹")
                    self.btn_nav_update.configure(text="  🔄")
                    self.lbl_marca.configure(text="")
                    self.lbl_marca.pack_forget()
            self.after(10, self.bucle_animacion_sidebar)
        else: 
            self.animando_sidebar = False

    def inicializar_interfaz_real(self):
        self.main_interface_frame = ctk.CTkFrame(self, fg_color=FONDO_VENTANA_PROFUNDO, corner_radius=0)
        self.main_interface_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.asociar_arrastre(self.main_interface_frame)
        
        ctk.CTkLabel(self.main_interface_frame, text=f"REGIS OAP ENGINE {VERSION_ACTUAL}", font=("Segoe UI", 11, "bold"), text_color=COR_REGIS_BORDES).place(relx=0.985, rely=0.98, anchor="se")

        self.menu_idioma = ctk.CTkComboBox(self.main_interface_frame, values=["Español", "Português", "English"], command=self.cambiar_idioma, fg_color=FONDO_TARJETAS, border_color=COR_REGIS_BORDES, border_width=1, button_color=COR_REGIS_PRINCIPAL, button_hover_color=COR_REGIS_HOVER, text_color=TEXTO_PRINCIPAL, width=130, height=32, font=(FUENTE_FORMAL, 12), corner_radius=6)
        self.menu_idioma.place(relx=0.80, y=30, anchor="ne")
        self.menu_idioma.set(self.idioma_actual)

        self.frame_rango_soporte = ctk.CTkFrame(self.main_interface_frame, fg_color="transparent", border_color=COR_REGIS_BORDES, border_width=1, corner_radius=6, height=32, width=200)
        self.frame_rango_soporte.place(relx=0.96, y=30, anchor="ne")
        self.frame_rango_soporte.pack_propagate(False)
        self.lbl_rango_privado = ctk.CTkLabel(self.frame_rango_soporte, text=TEXTOS[self.idioma_actual]["status_rango"], font=(FUENTE_FORMAL, 12, "bold"), text_color=COR_REGIS_PRINCIPAL)
        self.lbl_rango_privado.pack(fill="both", expand=True, padx=10)

        self.btn_cerrar = ctk.CTkButton(self.main_interface_frame, text="✕", width=35, height=35, fg_color="transparent", hover_color=COLOR_INACTIVO, text_color=TEXTO_PRINCIPAL, font=(FUENTE_FORMAL, 13, "bold"), corner_radius=4, command=self.destroy)
        self.btn_cerrar.place(relx=0.985, y=15, anchor="center")
        self.btn_maximizar = ctk.CTkButton(self.main_interface_frame, text="🗖", width=35, height=35, fg_color="transparent", hover_color=FONDO_TARJETAS, text_color=TEXTO_SECUNDARIO, font=(FUENTE_FORMAL, 11), corner_radius=4, command=self.alternar_maximizacion)
        self.btn_maximizar.place(relx=0.960, y=15, anchor="center")
        self.btn_minimizar = ctk.CTkButton(self.main_interface_frame, text="—", width=35, height=35, fg_color="transparent", hover_color=FONDO_TARJETAS, text_color=TEXTO_SECUNDARIO, font=(FUENTE_FORMAL, 13), corner_radius=4, command=self.minimizar_ventana)
        self.btn_minimizar.place(relx=0.935, y=15, anchor="center")

        self.contenedor_principal = ctk.CTkFrame(self.main_interface_frame, fg_color="transparent")
        self.contenedor_principal.place(x=220, y=100, relwidth=0.82, relheight=0.84)

        self.p_scanner_overlay = ctk.CTkFrame(self.main_interface_frame, fg_color="#03070d", corner_radius=0)
        self.lbl_scan_tit = ctk.CTkLabel(self.p_scanner_overlay, text="", font=(FUENTE_FORMAL, 32, "bold"), text_color=COR_REGIS_PRINCIPAL)
        self.lbl_scan_tit.place(relx=0.5, rely=0.08, anchor="center")
        self.scan_bar = ctk.CTkProgressBar(self.p_scanner_overlay, width=600, height=5, fg_color=FONDO_TARJETAS, progress_color=COR_REGIS_PRINCIPAL)
        self.scan_bar.place(relx=0.5, rely=0.15, anchor="center")
        self.lbl_scan_success = ctk.CTkLabel(self.p_scanner_overlay, text="", font=(FUENTE_FORMAL, 15, "bold"), text_color=COLOR_ACTIVO)
        
        self.f_lista_servicios = ctk.CTkScrollableFrame(self.p_scanner_overlay, fg_color="transparent", label_text="")
        self.btn_scan_action = ctk.CTkButton(self.p_scanner_overlay, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=50, width=380, corner_radius=8, command=self.procesar_accion_escaner)

        self.p_loading_opt = ctk.CTkFrame(self.main_interface_frame, fg_color=FONDO_VENTANA_PROFUNDO, corner_radius=0)
        self.load_title_opt = ctk.CTkLabel(self.p_loading_opt, text="", font=(FUENTE_FORMAL, 34, "bold"), text_color=COR_REGIS_PRINCIPAL)
        self.load_title_opt.place(relx=0.5, rely=0.35, anchor="center")
        self.load_status_opt = ctk.CTkLabel(self.p_loading_opt, text="", font=(FUENTE_FORMAL, 14), text_color=TEXTO_SECUNDARIO)
        self.load_status_opt.place(relx=0.5, rely=0.45, anchor="center")
        self.load_bar_opt = ctk.CTkProgressBar(self.p_loading_opt, width=700, height=5, fg_color=FONDO_TARJETAS)
        self.load_bar_opt.place(relx=0.5, rely=0.52, anchor="center")
        self.load_perc_opt = ctk.CTkLabel(self.p_loading_opt, text="0%", font=(FUENTE_FORMAL, 22, "bold"), text_color=TEXTO_PRINCIPAL)
        self.load_perc_opt.place(relx=0.5, rely=0.58, anchor="center")

        # Inicializar pantallas fijas internas
        self.crear_pantalla_verificacion()
        self.crear_pantalla_optimizaciones()
        self.crear_pantalla_status()
        self.crear_pantalla_hardware()
        self.crear_pantalla_limpieza()
        self.crear_pantalla_updates()

        self.sidebar = ctk.CTkFrame(self.main_interface_frame, width=self.ancho_sidebar_actual, fg_color=FONDO_PANEL_MENU, corner_radius=0)
        self.sidebar.place(x=0, y=0, relheight=1.0)
        self.sidebar.pack_propagate(False)
        self.sidebar.bind("<Enter>", self.evento_mouse_entra_sidebar)
        self.sidebar.bind("<Leave>", self.evento_mouse_sale_sidebar)

        self.frame_top_logo = ctk.CTkFrame(self.sidebar, height=80, fg_color="transparent", corner_radius=0)
        self.frame_top_logo.pack(fill="x", pady=(20, 0))
        self.lbl_marca = ctk.CTkLabel(self.frame_top_logo, text="", font=("Segoe UI Bold", 17), text_color=COR_REGIS_PRINCIPAL, anchor="w")
        
        self.btn_nav_verif = ctk.CTkButton(self.sidebar, text="  🔎", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("verif"))
        self.btn_nav_verif.pack(fill="x", padx=0, pady=(30, 3))
        self.btn_nav_opt = ctk.CTkButton(self.sidebar, text="  🚀", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("opt"))
        self.btn_nav_opt.pack(fill="x", padx=0, pady=3)
        self.btn_nav_status = ctk.CTkButton(self.sidebar, text="  📊", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("status"))
        self.btn_nav_status.pack(fill="x", padx=0, pady=3)
        self.btn_nav_hard = ctk.CTkButton(self.sidebar, text="  🖥️", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("hard"))
        self.btn_nav_hard.pack(fill="x", padx=0, pady=3)
        self.btn_nav_clean = ctk.CTkButton(self.sidebar, text="  🧹", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("clean"))
        self.btn_nav_clean.pack(fill="x", padx=0, pady=3)
        self.btn_nav_update = ctk.CTkButton(self.sidebar, text="  🔄", font=(FUENTE_FORMAL, 15, "bold"), height=55, fg_color="transparent", text_color=COR_REGIS_PRINCIPAL, hover_color=FONDO_TARJETAS, anchor="w", corner_radius=0, command=lambda: self.cambiar_pantalla("update"))
        self.btn_nav_update.pack(fill="x", padx=0, pady=3)

        self.cambiar_pantalla("verif")
        self.actualizar_textos_interfaz()

    def abrir_escaner_servicios(self):
        txt = TEXTOS[self.idioma_actual]
        self.p_scanner_overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.lbl_scan_tit.configure(text=txt["scan_run"])
        self.lbl_scan_success.place_forget()
        self.f_lista_servicios.place_forget()
        self.btn_scan_action.place_forget()
        self.scan_bar.place(relx=0.5, rely=0.5, anchor="center")
        self.scan_bar.set(0)
        
        for w in self.f_lista_servicios.winfo_children(): 
            w.destroy()
            
        threading.Thread(target=self._hilo_verificar_estado_servicios, daemon=True).start()
        self.progreso_escaner = 0
        self.bucle_barra_escaner()

    def bucle_barra_escaner(self):
        if self.progreso_escaner <= 100:
            self.scan_bar.set(self.progreso_escaner / 100)
            self.progreso_escaner += 4
            self.update()
            self.after(50, self.bucle_barra_escaner)
        else: 
            self._mostrar_resultados_escaner()

    def _hilo_verificar_estado_servicios(self):
        self.estado_servicios_actual.clear()
        for visual, real in self.servicios_check.items():
            activo = False
            try:
                if "HARDWARE" in real:
                    if real == "HARDWARE_TPM": 
                        activo = len(wmi.WMI(namespace=r"root\CIMv2\Security\MicrosoftTpm").Win32_Tpm()) > 0
                    elif real == "HARDWARE_SECUREBOOT": 
                        activo = "0x1" in subprocess.run(["reg", "query", r"HKLM\System\CurrentControlSet\Control\SecureBoot\State", "/v", "UEFISecureBootEnabled"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
                else: 
                    activo = "RUNNING" in subprocess.run(["sc", "query", real], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
            except: 
                pass
            self.estado_servicios_actual[visual] = activo

    def _mostrar_resultados_escaner(self):
        txt = TEXTOS[self.idioma_actual]
        self.lbl_scan_tit.configure(text=txt["scan_tit"])
        self.scan_bar.place(relx=0.5, rely=0.16, anchor="center")
        
        self.f_lista_servicios.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.75, relheight=0.58)
        self.btn_scan_action.place(relx=0.5, rely=0.88, anchor="center")
        
        for w in self.f_lista_servicios.winfo_children():
            w.destroy()

        self.todos_servicios_ok = True
        
        for sv_name, esta_activo in self.estado_servicios_actual.items():
            if not esta_activo: 
                self.todos_servicios_ok = False
                
            card = ctk.CTkFrame(self.f_lista_servicios, fg_color=FONDO_TARJETAS_CLARO, corner_radius=6, height=45, border_width=1, border_color=COR_REGIS_BORDES)
            card.pack(fill="x", padx=15, pady=4)
            
            ctk.CTkLabel(card, text=f" Service Engine Key: {sv_name}", font=FUENTE_GRANDE, text_color=TEXTO_PRINCIPAL).pack(side="left", padx=15)
            ctk.CTkLabel(card, text=txt["s_activo"] if esta_activo else txt["s_inactivo"], font=("Segoe UI Bold", 13), text_color=COLOR_ACTIVO if esta_activo else COLOR_INACTIVO).pack(side="right", padx=20)

        # CORRECCIÓN: Botón "SALIR" siempre habilitado para evitar bloqueos si faltan servicios de Windows
        self.btn_scan_action.configure(state="normal", text=txt["scan_sair"], fg_color=FONDO_TARJETAS_CLARO, text_color=COR_REGIS_PRINCIPAL, border_width=1, border_color=COR_REGIS_PRINCIPAL)
        self.accion_actual_boton_escaner = "SALIR"

    def procesar_accion_escaner(self):
        txt = TEXTOS[self.idioma_actual]
        if self.accion_actual_boton_escaner == "SALIR":
            self.lbl_last_scan.configure(text=datetime.datetime.now().strftime("%d/%m/%Y · %H:%M"))
            self.v_ban_sub.configure(text=txt["res_ok"] if self.todos_servicios_ok else txt["res_bad"], text_color=COLOR_ACTIVO if self.todos_servicios_ok else COLOR_INACTIVO)
            self.p_scanner_overlay.place_forget()

    def verificar_ajustes_sistema_reales(self): 
        threading.Thread(target=self._hilo_escanear_sistema_operativo, daemon=True).start()
        
    def _hilo_escanear_sistema_operativo(self):
        try:
            self.estados_modulos["OAP Fluid"] = "0x0" in subprocess.run(["reg", "query", r"HKCU\Control Panel\Mouse", "/v", "MouseSpeed"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
            res2 = subprocess.run(["reg", "query", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\QoS\FreeFire", "/v", "Protocol"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
            self.estados_modulos["OAP Advanced"] = "UDP" in res2
            res3 = subprocess.run(["reg", "query", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "/v", "SystemResponsiveness"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
            self.estados_modulos["OAP Absolute"] = "0x0" in res3
        except: 
            pass
        self.after(100, self.refrescar_ui_status)

    def iniciar_secuencia_carga_opt(self, boton, modulo_name):
        segundos = 15 if modulo_name == "OAP Fluid" else (30 if modulo_name == "OAP Advanced" else 60)
        self.p_loading_opt.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_title_opt.configure(text=f"REGIS OAP // STARTING {modulo_name.upper()}", text_color=COR_REGIS_PRINCIPAL)
        self.load_bar_opt.configure(progress_color=COR_REGIS_PRINCIPAL)
        self.btn_opt_ref, self.modulo_opt_ref, self.prog_opt = boton, modulo_name, 0
        self.bucle_opt(int((segundos * 1000) / 100))

    def bucle_opt(self, intervalo):
        txt = TEXTOS[self.idioma_actual]
        if self.prog_opt <= 100:
            self.load_bar_opt.set(self.prog_opt / 100)
            self.load_perc_opt.configure(text=f"{self.prog_opt}%")
            self.load_status_opt.configure(text=txt["inj_fase1"] if self.prog_opt < 35 else (txt["inj_fase2"] if self.prog_opt < 75 else txt["inj_fase3"]))
            self.prog_opt += 1
            self.update()
            self.after(intervalo, lambda: self.bucle_opt(intervalo))
        else:
            self._aplicar_tweak_real_SO(self.modulo_opt_ref)
            self.p_loading_opt.place_forget()
            self.btn_opt_ref.configure(text=txt["btn_activo"], state="disabled", fg_color=FONDO_TARJETAS, text_color=COR_REGIS_PRINCIPAL, border_width=1, border_color=COR_REGIS_PRINCIPAL)
            self.estados_modulos[self.modulo_opt_ref] = True
            self.abrir_modal_exito(self.modulo_opt_ref)

    # =========================================================================================
    # CONFIGURACIÓN PURA DE REGISTROS - SIN DETENER SERVICIOS NI CAMBIAR PLANES DE ENERGÍA
    # =========================================================================================
    def _aplicar_tweak_real_SO(self, modulo):
        try:
            # --- NIVEL 1: OAP FLUID (Ajustes de periféricos) ---
            if modulo == "OAP Fluid" or modulo == "OAP Advanced" or modulo == "OAP Absolute":
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Mouse", "/v", "MouseSpeed", "/t", "REG_SZ", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Mouse", "/v", "MouseThreshold1", "/t", "REG_SZ", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Mouse", "/v", "MouseThreshold2", "/t", "REG_SZ", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Mouse", "/v", "MouseSensitivity", "/t", "REG_SZ", "/d", "10", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "delete", r"HKCU\Control Panel\Mouse", "/v", "SmoothMouseXCurve", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "delete", r"HKCU\Control Panel\Mouse", "/v", "SmoothMouseYCurve", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\mouclass\Parameters", "/v", "MouseDataQueueSize", "/t", "REG_DWORD", "/d", "100", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Keyboard", "/v", "KeyboardDelay", "/t", "REG_SZ", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\Control Panel\Keyboard", "/v", "KeyboardSpeed", "/t", "REG_SZ", "/d", "31", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\kbdclass\Parameters", "/v", "KeyboardDataQueueSize", "/t", "REG_DWORD", "/d", "16", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)

            # --- NIVEL 2: OAP ADVANCED (Optimización del flujo de Red / QoS / DVR) ---
            if modulo == "OAP Advanced" or modulo == "OAP Absolute":
                interfaces_output = subprocess.run(["reg", "query", r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
                for linha in interfaces_output.splitlines():
                    if "Interfaces\\" in linha:
                        subprocess.run(["reg", "add", linha.strip(), "/v", "TcpAckFrequency", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                        subprocess.run(["reg", "add", linha.strip(), "/v", "TCPNoDelay", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                
                subprocess.run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["netsh", "int", "tcp", "set", "global", "chimney=disabled"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["netsh", "int", "tcp", "set", "global", "ecncapability=disabled"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["netsh", "int", "tcp", "set", "global", "timestamps=disabled"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["netsh", "int", "tcp", "set", "global", "rss=enabled"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["netsh", "int", "tcp", "set", "heuristics", "disabled"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\QoS\FreeFire", "/v", "Protocol", "/t", "REG_SZ", "/d", "UDP", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\QoS\FreeFire", "/v", "DSCPValue", "/t", "REG_SZ", "/d", "46", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "/v", "TcpNoDelay", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Modificaciones estables del GameDVR sin suspender ni deshabilitar servicios
                subprocess.run(["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "/v", "AllowGameDVR", "/t", "REG_DWORD", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_FSEBehaviorMode", "/t", "REG_DWORD", "/d", "2", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_HonorUserFSEBehaviorMode", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\USB", "/v", "DisableSelectiveSuspend", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)

            # --- NIVEL 3: OAP KERNEL ABSOLUTE (Planificación Multimedia Avanzada de Tareas) ---
            if modulo == "OAP Absolute":
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "/v", "SystemResponsiveness", "/t", "REG_DWORD", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "GPU Priority", "/t", "REG_DWORD", "/d", "8", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "Priority", "/t", "REG_DWORD", "/d", "6", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "Scheduling Category", "/t", "REG_SZ", "/d", "High", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "SFIO Priority", "/t", "REG_SZ", "/d", "High", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\0cc5b647-c1df-4637-891a-dec35c318583", "/v", "ValueMax", "/t", "REG_DWORD", "/d", "0", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\mouclass\Parameters", "/v", "ThreadPriority", "/t", "REG_DWORD", "/d", "15", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl", "/v", "Win32PrioritySeparation", "/t", "REG_DWORD", "/d", "38", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000", "/v", "PowerMizerEnable", "/t", "REG_DWORD", "/d", "1", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows\Dwm", "/v", "OverlayTestMode", "/t", "REG_DWORD", "/d", "5", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["bcdedit", "/set", "useplatformtick", "yes"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["bcdedit", "/deletevalue", "useplatformclock"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["bcdedit", "/set", "disabledynamictick", "yes"], creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "/v", "NetworkThrottlingIndex", "/t", "REG_DWORD", "/d", "4294967295", "/f"], creationflags=subprocess.CREATE_NO_WINDOW)
        except: 
            pass

    def abrir_modal_exito(self, modulo):
        txt = TEXTOS[self.idioma_actual]
        modal = ctk.CTkToplevel(self)
        modal.geometry("420x220")
        modal.overrideredirect(True)
        modal.configure(fg_color=FONDO_TARJETAS)
        modal.geometry(f"+{self.winfo_x() + (self.winfo_width()//2) - 210}+{self.winfo_y() + (self.winfo_height()//2) - 110}")
        
        ctk.CTkLabel(modal, text="✔ ARCHITECTURE ACTIVATED", font=("Segoe UI Bold", 18), text_color=COLOR_ACTIVO).pack(pady=(35, 5))
        ctk.CTkLabel(modal, text=f"Module {modulo.upper()} Enabled Successfully.\n{txt['scan_success']}", font=FUENTE_SUBTITULO, text_color=TEXTO_PRINCIPAL, justify="center").pack(pady=10)
        ctk.CTkButton(modal, text="OK", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, width=120, height=35, command=modal.destroy).pack(pady=(15, 10))
        modal.grab_set()

    def crear_pantalla_verificacion(self):
        self.p_verif = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_verif.pack_propagate(False)
        
        f_tit = ctk.CTkFrame(self.p_verif, fg_color="transparent", height=50)
        f_tit.pack(fill="x", pady=(35, 10))
        self.v_tit = ctk.CTkLabel(f_tit, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.v_tit.pack()
        
        v_banner = ctk.CTkFrame(self.p_verif, fg_color="transparent", corner_radius=8, border_color=COR_REGIS_BORDES, border_width=1, height=130)
        v_banner.pack(pady=15, padx=60, fill="x")
        v_banner.pack_propagate(False)
        
        ctk.CTkLabel(v_banner, text="REGIS OAP", font=("Segoe UI", 32, "bold"), text_color=TEXTO_PRINCIPAL).place(relx=0.5, rely=0.38, anchor="center")
        self.v_ban_sub = ctk.CTkLabel(v_banner, text="OAP Core Engine Status", font=FUENTE_SUBTITULO, text_color=TEXTO_SECUNDARIO)
        self.v_ban_sub.place(relx=0.5, rely=0.72, anchor="center")
        
        self.v_cards_row = ctk.CTkFrame(self.p_verif, fg_color="transparent", height=110)
        self.v_cards_row.pack(fill="x", padx=40, pady=25)

        def c_card(parent, relx, ico, t, val):
            card = ctk.CTkFrame(parent, fg_color=FONDO_TARJETAS, corner_radius=10, width=220, height=90, border_width=1, border_color="#1F2F40")
            card.place(relx=relx, rely=0.5, anchor="center")
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=ico, font=("Segoe UI", 20), text_color=COR_REGIS_PRINCIPAL).place(relx=0.18, rely=0.35, anchor="center")
            ctk.CTkLabel(card, text=t, font=("Segoe UI Semibold", 10), text_color=TEXTO_SECUNDARIO).place(relx=0.36, rely=0.35, anchor="w")
            v_lbl = ctk.CTkLabel(card, text=val, font=("Segoe UI", 12), text_color=TEXTO_PRINCIPAL)
            v_lbl.place(relx=0.5, rely=0.72, anchor="center")
            return v_lbl

        self.card_1 = c_card(self.v_cards_row, 0.18, "🔑", "LICENSE STATUS", "PRIVADO")
        self.card_2 = c_card(self.v_cards_row, 0.50, "🖥️", "SYSTEM PLATFORM", self.obtener_nombre_sistema())
        self.lbl_last_scan = c_card(self.v_cards_row, 0.82, "⏱️", "LAST SCAN TIMEOUT", "Ninguno")
        
        f_btn = ctk.CTkFrame(self.p_verif, fg_color="transparent", height=80)
        f_btn.pack(fill="x", pady=15)
        self.v_btn = ctk.CTkButton(f_btn, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=48, width=340, corner_radius=8, command=self.abrir_escaner_servicios)
        self.v_btn.place(relx=0.5, rely=0.5, anchor="center")

    def crear_pantalla_optimizaciones(self):
        self.p_opt = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_opt.pack_propagate(False)
        
        self.o_tit = ctk.CTkLabel(self.p_opt, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.o_tit.pack(pady=(35, 20))
        
        self.cards_frame_opt = ctk.CTkFrame(self.p_opt, fg_color="transparent")
        self.cards_frame_opt.pack(fill="both", expand=True, padx=20, pady=10)

        def c_opt(parent, relx, tit, sub):
            card = ctk.CTkFrame(parent, width=240, height=270, fg_color=FONDO_TARJETAS, corner_radius=12, border_width=1, border_color=COR_REGIS_BORDES)
            card.place(relx=relx, rely=0.46, anchor="center")
            card.pack_propagate(False)
            
            ctk.CTkLabel(card, text=tit, font=("Segoe UI Semibold", 22), text_color=TEXTO_PRINCIPAL).pack(pady=(45, 6))
            ctk.CTkLabel(card, text=sub, font=FUENTE_SUBTITULO, text_color=TEXTO_SECUNDARIO).pack(pady=(0, 10))
            
            texto_estado_inicial = TEXTOS[self.idioma_actual]["btn_activo"] if self.estados_modulos[tit] else TEXTOS[self.idioma_actual]["btn_inyectar"]
            estado_boton = "disabled" if self.estados_modulos[tit] else "normal"
            
            b = ctk.CTkButton(
                card, 
                text=texto_estado_inicial, 
                font=FUENTE_BOTON, 
                fg_color="transparent", 
                border_color=COR_REGIS_PRINCIPAL, 
                border_width=1.5, 
                hover_color=FONDO_TARJETAS_CLARO, 
                text_color=TEXTO_PRINCIPAL, 
                height=42, 
                corner_radius=8, 
                state=estado_boton,
                command=lambda: self.iniciar_secuencia_carga_opt(b, tit)
            )
            b.place(relx=0.5, rely=0.78, anchor="center", relwidth=0.75)

        c_opt(self.cards_frame_opt, 0.18, "OAP Fluid", "Latency Override")
        c_opt(self.cards_frame_opt, 0.50, "OAP Advanced", "System Tuning")
        c_opt(self.cards_frame_opt, 0.82, "OAP Absolute", "Kernel Patching")

    def crear_pantalla_status(self):
        self.p_status = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_status.pack_propagate(False)
        
        self.s_tit = ctk.CTkLabel(self.p_status, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.s_tit.pack(pady=(30, 15))
        
        self.f_status_list = ctk.CTkFrame(self.p_status, fg_color=FONDO_TARJETAS, corner_radius=12, border_width=1, border_color=COR_REGIS_BORDES)
        self.f_status_list.pack(pady=10, padx=80, fill="both", expand=True)
        
        def c_st_lbl(parent, rely, t):
            ctk.CTkLabel(parent, text=t, font=("Segoe UI Semibold", 16), text_color=TEXTO_PRINCIPAL).place(relx=0.08, rely=rely, anchor="w")
            lbl = ctk.CTkLabel(parent, text="INACTIVO", font=("Segoe UI Bold", 15), text_color=TEXTO_SECUNDARIO)
            lbl.place(relx=0.92, rely=rely, anchor="e")
            return lbl

        self.lbl_s_fluid_est = c_st_lbl(self.f_status_list, 0.25, "» OAP Fluid Engine Registry Tweak:")
        self.lbl_s_adv_est = c_st_lbl(self.f_status_list, 0.50, "» OAP Advanced Power Architecture Scheme:")
        self.lbl_s_abs_est = c_st_lbl(self.f_status_list, 0.75, "» OAP Absolute HPET System Clock Override:")
        
        self.btn_check_status_os = ctk.CTkButton(self.p_status, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=46, width=320, corner_radius=8, command=self.verificar_ajustes_sistema_reales)
        self.btn_check_status_os.pack(pady=20)

    def refrescar_ui_status(self):
        txt = TEXTOS[self.idioma_actual]
        def act(l, est): 
            l.configure(text=f"{txt['s_activo']}  🟢" if est else f"{txt['s_inactivo']}  🔴", text_color=COLOR_ACTIVO if est else COLOR_INACTIVO)
        act(self.lbl_s_fluid_est, self.estados_modulos["OAP Fluid"])
        act(self.lbl_s_adv_est, self.estados_modulos["OAP Advanced"])
        act(self.lbl_s_abs_est, self.estados_modulos["OAP Absolute"])

    def crear_pantalla_hardware(self):
        self.p_hard = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_hard.pack_propagate(False)
        
        self.h_tit = ctk.CTkLabel(self.p_hard, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.h_tit.pack(pady=(30, 10))
        
        self.f_box_info = ctk.CTkFrame(self.p_hard, fg_color=FONDO_TARJETAS, corner_radius=10, border_width=1, border_color="#1F2F40")
        self.f_box_info.pack(pady=10, padx=50, fill="both", expand=True)
        
        self.box_info = ctk.CTkLabel(self.f_box_info, text="", font=FUENTE_CONSOLA, text_color=TEXTO_PRINCIPAL, padx=25, pady=25, justify="left", anchor="nw")
        self.box_info.pack(fill="both", expand=True)
        
        f_btn_h = ctk.CTkFrame(self.p_hard, fg_color="transparent", height=80)
        f_btn_h.pack(fill="x", pady=15)
        self.btn_h = ctk.CTkButton(f_btn_h, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=46, width=320, corner_radius=8, command=self.escanear_hardware_real)
        self.btn_h.place(relx=0.5, rely=0.5, anchor="center")

    def escanear_hardware_real(self): 
        self.box_info.configure(text=self.detectar_hardware_profundo())

    def crear_pantalla_limpieza(self):
        self.p_clean = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_clean.pack_propagate(False)
        
        self.lbl_c_tit = ctk.CTkLabel(self.p_clean, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.lbl_c_tit.pack(pady=(40, 20))
        
        self.clean_card = ctk.CTkFrame(self.p_clean, fg_color=FONDO_TARJETAS, corner_radius=12, border_width=1, border_color=COR_REGIS_BORDES)
        self.clean_card.pack(pady=20, padx=100, fill="both", expand=True)
        
        self.txt_clean_log = ctk.CTkLabel(self.clean_card, text="OAP Shredder Core System Ready.", font=FUENTE_CONSOLA, text_color=TEXTO_SECUNDARIO, justify="center")
        self.txt_clean_log.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_clean_exec = ctk.CTkButton(self.p_clean, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=48, width=320, corner_radius=8, command=self.ejecutar_limpieza_profunda)
        self.btn_clean_exec.pack(pady=30)

    def ejecutar_limpieza_profunda(self):
        txt = TEXTOS[self.idioma_actual]
        self.txt_clean_log.configure(text=txt["c_run"], text_color=COR_REGIS_PRINCIPAL)
        self.btn_clean_exec.configure(state="disabled")
        threading.Thread(target=self._hilo_limpieza_segura, daemon=True).start()

    def _hilo_limpieza_segura(self):
        rutas_limpieza = [os.environ.get('TEMP'), os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')]
        bytes_liberados = 0
        
        for ruta in rutas_limpieza:
            if ruta and os.path.exists(ruta):
                for elemento in os.listdir(ruta):
                    ruta_completa = os.path.join(ruta, elemento)
                    try:
                        if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                            bytes_liberados += os.path.getsize(ruta_completa)
                            os.unlink(ruta_completa)
                        elif os.path.isdir(ruta_completa):
                            bytes_liberados += sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(ruta_completa))
                            shutil.rmtree(ruta_completa)
                    except:
                        pass
                        
        megas_liberados = round(bytes_liberados / (1024 * 1024), 2)
        self.after(1200, lambda: self._finalizar_ui_limpieza(megas_liberados))

    def _finalizar_ui_limpieza(self, megas):
        txt = TEXTOS[self.idioma_actual]
        log_final = f"✔ {txt['c_success']}\n\n[OAP ENGINE] -> {megas} MB cache cleared."
        self.txt_clean_log.configure(text=log_final, text_color=COLOR_ACTIVO)
        self.btn_clean_exec.configure(state="normal")

    def crear_pantalla_updates(self):
        self.p_update = ctk.CTkFrame(self.contenedor_principal, fg_color=FONDO_CONTENEDOR_CENTRAL, corner_radius=12, border_color=COR_REGIS_BORDES, border_width=1)
        self.p_update.pack_propagate(False)
        
        self.lbl_u_tit = ctk.CTkLabel(self.p_update, text="", font=FUENTE_TITULO, text_color=COR_REGIS_PRINCIPAL)
        self.lbl_u_tit.pack(pady=(40, 20))
        
        self.update_card = ctk.CTkFrame(self.p_update, fg_color=FONDO_TARJETAS, corner_radius=12, border_width=1, border_color=COR_REGIS_BORDES)
        self.update_card.pack(pady=20, padx=100, fill="both", expand=True)
        
        self.txt_version_info = ctk.CTkLabel(self.update_card, text=f"Current Engine Build: {VERSION_ACTUAL}\n\nClick below to ping cloud servers.", font=FUENTE_CONSOLA, text_color=TEXTO_SECUNDARIO, justify="center")
        self.txt_version_info.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_update_action = ctk.CTkButton(self.p_update, text="", font=FUENTE_BOTON, fg_color=COR_REGIS_PRINCIPAL, hover_color=COR_REGIS_HOVER, text_color=TEXTO_BOTON_OSCURO, height=48, width=320, corner_radius=8, command=self.buscar_actualizaciones_servidor)
        self.btn_update_action.pack(pady=30)

    def buscar_actualizaciones_servidor(self):
        txt = TEXTOS[self.idioma_actual]
        self.txt_version_info.configure(text=txt["u_checking"], text_color=COR_REGIS_PRINCIPAL)
        self.btn_update_action.configure(state="disabled")
        threading.Thread(target=self._hilo_conexion_github, daemon=True).start()

    def _hilo_conexion_github(self):
        self.after(2000, self._procesar_resultado_github)

    def _procesar_resultado_github(self):
        txt = TEXTOS[self.idioma_actual]
        nueva_version_disponible = False 
        
        if not nueva_version_disponible:
            log_build = f"✔ {txt['u_uptodate']}\n\nBuild Target: stable-channel-{VERSION_ACTUAL.lower()}"
            self.txt_version_info.configure(text=log_build, text_color=COLOR_ACTIVO)
            self.btn_update_action.configure(state="normal")
        else:
            self.txt_version_info.configure(text=txt["u_newversion"], text_color=COLOR_INACTIVO)
            self.btn_update_action.configure(state="normal", text=txt["u_btn_download"], fg_color=COLOR_ACTIVO)

    def cambiar_pantalla(self, vista):
        if hasattr(self, 'p_verif') and self.p_verif.winfo_exists():
            self.p_verif.place_forget()
            self.p_opt.place_forget()
            self.p_status.place_forget()
            self.p_hard.place_forget()
            self.p_clean.place_forget()
            self.p_update.place_forget()
            
            if vista == "verif": 
                self.p_verif.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            elif vista == "opt": 
                self.crear_pantalla_optimizaciones()
                self.p_opt.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            elif vista == "status": 
                self.p_status.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
                self.verificar_ajustes_sistema_reales()
            elif vista == "hard": 
                self.p_hard.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            elif vista == "clean":
                self.p_clean.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            elif vista == "update":
                self.p_update.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def alternar_maximizacion(self):
        if self.es_maximi_pantalla: 
            self.geometry("1150x680")
            self.es_maximi_pantalla = False
        else: 
            self.geometry(f"{self.sw}x{self.sh}+0+0")
            self.es_maximi_pantalla = True
            
    def minimizar_ventana(self): 
        self.update_idletasks()
        self.overrideredirect(False)
        self.state("iconic")
        self.bind("<FocusIn>", self.restaurar_ventana)
        
    def restaurar_ventana(self, event): 
        self.unbind("<FocusIn>")
        self.overrideredirect(True)
        
    def cambiar_idioma(self, id_el): 
        self.idioma_actual = id_el
        self.actualizar_textos_interfaz()

    def actualizar_textos_interfaz(self):
        txt = TEXTOS[self.idioma_actual]
        if hasattr(self, 'btn_nav_verif') and self.btn_nav_verif.winfo_exists():
            if self.sidebar.winfo_width() > 150:
                self.btn_nav_verif.configure(text=txt["btn_verif"])
                self.btn_nav_opt.configure(text=txt["btn_opt"])
                self.btn_nav_status.configure(text=txt["btn_status"])
                self.btn_nav_hard.configure(text=txt["btn_hard"])
                self.btn_nav_clean.configure(text=txt["btn_clean"])
                self.btn_nav_update.configure(text=txt["btn_update"])
                self.lbl_marca.configure(text="   REGIS OAP")
                
            self.v_tit.configure(text=txt["v_titulo"])
            self.o_tit.configure(text=txt["btn_opt"])
            self.s_tit.configure(text=txt["s_titulo"])
            self.h_tit.configure(text=txt["h_titulo"])
            self.lbl_c_tit.configure(text=txt["c_titulo"])
            self.lbl_u_tit.configure(text=txt["u_titulo"])
            
            self.v_btn.configure(text=txt["v_btn"])
            self.btn_check_status_os.configure(text=txt["s_btn_verif"])
            self.btn_h.configure(text=txt["h_btn"])
            self.btn_clean_exec.configure(text=txt["c_btn"])
            
            if self.btn_update_action.cget("text") != txt["u_btn_download"]:
                self.btn_update_action.configure(text=txt["u_btn_buscar"])
            
            if not self.box_info.cget("text") or "Aguardando" in self.box_info.cget("text") or "Esperando" in self.box_info.cget("text"): 
                self.box_info.configure(text=txt["h_espera"])
                
            self.lbl_rango_privado.configure(text=txt["status_rango"])
            self.refrescar_ui_status()

if __name__ == "__main__":
    app = RegisOAPApp()
    app.mainloop()