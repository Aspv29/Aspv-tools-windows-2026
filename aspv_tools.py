# -*- coding: utf-8 -*-
"""
ASPV Tools - Windows Premium
============================
Comprehensive Windows system administration tool.
Features: Android Drivers, Windows Controllers, Optimization,
CMD Tools, ADB/Fastboot, USB Debugging, Disk Tools, Security, Network, and more.

Author: ASPV Tools Team
Version: 2.0.0
Requires: Python 3.8+, Windows OS, Administrator Privileges
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import sys
import os
import ctypes
import platform
import json
import time
try:
    import winreg
except ImportError:
    winreg = None

# ─────────────────────── ADMIN CHECK ───────────────────────

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def request_admin():
    """Re-launch with admin privileges."""
    if sys.platform == "win32" and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

# ─────────────────────── COLORS & FONTS ────────────────────

C = {
    "bg_main":    "#0A0E1A",
    "bg_card":    "#0D1B2A",
    "bg_sidebar": "#070B14",
    "bg_btn":     "#1E40AF",
    "bg_btn_h":   "#2563EB",
    "bg_btn_act": "#3B82F6",
    "bg_purple":  "#7C3AED",
    "bg_purp_h":  "#9333EA",
    "accent":     "#3B82F6",
    "text":       "#E2E8F0",
    "text_dim":   "#94A3B8",
    "text_head":  "#FFFFFF",
    "border":     "#1E293B",
    "success":    "#10B981",
    "warning":    "#F59E0B",
    "danger":     "#EF4444",
    "output_bg":  "#0F172A",
}

FONT = {
    "title":   ("Segoe UI", 18, "bold"),
    "section": ("Segoe UI", 13, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "mono":    ("Consolas", 9),
    "btn":     ("Segoe UI", 10, "bold"),
}

# ─────────────────────── COMMAND RUNNER ─────────────────────

class CommandRunner:
    """Runs shell commands in a background thread and streams output."""

    def __init__(self, output_widget: scrolledtext.ScrolledText, status_var: tk.StringVar):
        self.out = output_widget
        self.status = status_var

    def _write(self, text: str, tag: str = "normal"):
        self.out.configure(state="normal")
        self.out.insert(tk.END, text + "\n", tag)
        self.out.see(tk.END)
        self.out.configure(state="disabled")

    def run(self, cmd: str, shell: bool = True, use_powershell: bool = False):
        self.out.configure(state="normal")
        self.out.delete(1.0, tk.END)
        self.out.configure(state="disabled")
        self.status.set("Ejecutando comando...")
        t = threading.Thread(target=self._execute, args=(cmd, shell, use_powershell), daemon=True)
        t.start()

    def _execute(self, cmd, shell, use_powershell):
        try:
            if use_powershell:
                full_cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd]
                proc = subprocess.Popen(
                    full_cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace"
                )
            else:
                proc = subprocess.Popen(
                    cmd, shell=shell,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace"
                )
            for line in proc.stdout:
                self._write(line.rstrip(), "output")
            proc.wait()
            rc = proc.returncode
            if rc == 0:
                self._write("\n[OK] Proceso completado con éxito.", "success")
                self.status.set("Completado con éxito")
            else:
                self._write(f"\n[WARN] Proceso terminó con código: {rc}", "warning")
                self.status.set(f"Terminado (código {rc})")
        except FileNotFoundError as e:
            self._write(f"[ERROR] Comando no encontrado: {e}", "error")
            self.status.set("Error: comando no encontrado")
        except Exception as e:
            self._write(f"[ERROR] {e}", "error")
            self.status.set(f"Error: {e}")

# ─────────────────────── MAIN APP ───────────────────────────

class ASPVTools(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASPV Tools - Windows Premium v2.0")
        self.geometry("1280x800")
        self.minsize(900, 600)
        self.configure(bg=C["bg_main"])
        self.resizable(True, True)

        # State
        self.status_var = tk.StringVar(value="Listo")
        self.current_section = tk.StringVar(value="home")

        # Build UI
        self._build_header()
        self._build_layout()
        self._build_sidebar()
        self._build_content_area()
        self._build_status_bar()

        # Default view
        self.show_section("home")

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    # ── LAYOUT BUILDERS ──────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self, bg="#050810", height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        logo = tk.Label(header, text="⚡ ASPV Tools", font=("Segoe UI", 16, "bold"),
                        bg="#050810", fg="#3B82F6")
        logo.pack(side="left", padx=20, pady=10)

        subtitle = tk.Label(header, text="Windows Premium Suite v2.0",
                            font=("Segoe UI", 10), bg="#050810", fg="#64748B")
        subtitle.pack(side="left", padx=0, pady=14)

        # Admin badge
        admin_txt = "● Admin" if is_admin() else "○ Sin Admin"
        admin_fg  = C["success"] if is_admin() else C["danger"]
        tk.Label(header, text=admin_txt, font=FONT["small"],
                 bg="#050810", fg=admin_fg).pack(side="right", padx=20)

    def _build_layout(self):
        self.main_frame = tk.Frame(self, bg=C["bg_main"])
        self.main_frame.pack(fill="both", expand=True)

    def _build_sidebar(self):
        # Scrollable sidebar
        sidebar_container = tk.Frame(self.main_frame, bg=C["bg_sidebar"], width=220)
        sidebar_container.pack(fill="y", side="left")
        sidebar_container.pack_propagate(False)

        canvas = tk.Canvas(sidebar_container, bg=C["bg_sidebar"],
                           highlightthickness=0, width=218)
        scrollbar = ttk.Scrollbar(sidebar_container, orient="vertical",
                                  command=canvas.yview)
        self.sidebar = tk.Frame(canvas, bg=C["bg_sidebar"])

        self.sidebar.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.sidebar, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Navigation items: (icon, label, section_key)
        nav_items = [
            ("🏠", "Inicio",               "home"),
            ("📱", "Drivers Android",       "android_drivers"),
            ("🖥️", "Controladores Windows", "win_controllers"),
            ("⚡", "Optimización Win11",    "optimization"),
            ("💻", "Comandos CMD",          "cmd_tools"),
            ("🔧", "ADB & Fastboot",        "adb_fastboot"),
            ("🔓", "USB Debugging / FRP",   "usb_debug"),
            ("📡", "Dispositivos USB",      "usb_devices"),
            ("💾", "Herramientas Disco",    "disk_tools"),
            ("🖼️", "Íconos del Sistema",   "system_icons"),
            ("🛡️", "Anti-Spyware",         "anti_spyware"),
            ("🔌", "Reparar USB",           "usb_repair"),
            ("🔒", "Seguridad Windows",     "security"),
            ("🌐", "Red & WiFi",            "network"),
            ("🔊", "Audio",                 "audio"),
            ("🖨️", "Impresoras",           "printers"),
            ("ℹ️", "Info del Sistema",      "sysinfo"),
        ]

        tk.Label(self.sidebar, text="NAVEGACIÓN", font=("Segoe UI", 8, "bold"),
                 bg=C["bg_sidebar"], fg="#475569").pack(pady=(16, 4), padx=12, anchor="w")

        self.nav_buttons = {}
        for icon, label, key in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}  {label}",
                font=FONT["body"],
                bg=C["bg_sidebar"],
                fg=C["text_dim"],
                activebackground=C["bg_btn"],
                activeforeground=C["text_head"],
                relief="flat",
                anchor="w",
                cursor="hand2",
                command=lambda k=key: self.show_section(k),
            )
            btn.pack(fill="x", padx=6, pady=1, ipady=6)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=C["bg_btn"], fg=C["text"]))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.configure(
                bg=C["bg_btn_act"] if self.current_section.get() == k else C["bg_sidebar"],
                fg=C["text_head"] if self.current_section.get() == k else C["text_dim"]
            ))
            self.nav_buttons[key] = btn

    def _build_content_area(self):
        self.content_frame = tk.Frame(self.main_frame, bg=C["bg_main"])
        self.content_frame.pack(fill="both", expand=True, side="left")

        # Output terminal at bottom
        terminal_frame = tk.LabelFrame(self.content_frame, text=" Terminal de Salida ",
                                       font=FONT["small"], bg=C["bg_main"],
                                       fg=C["text_dim"], bd=1, relief="flat",
                                       highlightbackground=C["border"],
                                       highlightthickness=1)
        terminal_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 8))

        self.output_box = scrolledtext.ScrolledText(
            terminal_frame, height=10,
            bg=C["output_bg"], fg=C["text"],
            font=FONT["mono"], relief="flat",
            insertbackground=C["accent"],
            state="disabled"
        )
        self.output_box.pack(fill="x", padx=4, pady=4)
        self.output_box.tag_configure("output",  foreground=C["text"])
        self.output_box.tag_configure("success", foreground=C["success"])
        self.output_box.tag_configure("warning", foreground=C["warning"])
        self.output_box.tag_configure("error",   foreground=C["danger"])
        self.output_box.tag_configure("normal",  foreground=C["text_dim"])

        self.runner = CommandRunner(self.output_box, self.status_var)

        # Scrollable main panel
        scroll_canvas = tk.Canvas(self.content_frame, bg=C["bg_main"], highlightthickness=0)
        vscroll = ttk.Scrollbar(self.content_frame, orient="vertical",
                                command=scroll_canvas.yview)
        self.panel = tk.Frame(scroll_canvas, bg=C["bg_main"])
        self.panel.bind("<Configure>",
                        lambda e: scroll_canvas.configure(
                            scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=self.panel, anchor="nw")
        scroll_canvas.configure(yscrollcommand=vscroll.set)

        scroll_canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")
        scroll_canvas.bind_all("<MouseWheel>",
                               lambda e: scroll_canvas.yview_scroll(
                                   -1 * (e.delta // 120), "units"))

    def _build_status_bar(self):
        bar = tk.Frame(self, bg="#070B14", height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self.status_var, font=FONT["small"],
                 bg="#070B14", fg=C["text_dim"]).pack(side="left", padx=12)
        tk.Label(bar, text=f"Python {sys.version.split()[0]} | {platform.system()} {platform.release()}",
                 font=FONT["small"], bg="#070B14", fg="#334155").pack(side="right", padx=12)

    # ── SECTION ROUTER ────────────────────────────────────────

    def show_section(self, key: str):
        # Reset all buttons
        self.current_section.set(key)
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=C["bg_btn_act"], fg=C["text_head"])
            else:
                btn.configure(bg=C["bg_sidebar"], fg=C["text_dim"])

        # Clear panel
        for w in self.panel.winfo_children():
            w.destroy()

        sections = {
            "home":           self._section_home,
            "android_drivers":self._section_android_drivers,
            "win_controllers":self._section_win_controllers,
            "optimization":   self._section_optimization,
            "cmd_tools":      self._section_cmd_tools,
            "adb_fastboot":   self._section_adb_fastboot,
            "usb_debug":      self._section_usb_debug,
            "usb_devices":    self._section_usb_devices,
            "disk_tools":     self._section_disk_tools,
            "system_icons":   self._section_system_icons,
            "anti_spyware":   self._section_anti_spyware,
            "usb_repair":     self._section_usb_repair,
            "security":       self._section_security,
            "network":        self._section_network,
            "audio":          self._section_audio,
            "printers":       self._section_printers,
            "sysinfo":        self._section_sysinfo,
        }
        fn = sections.get(key, self._section_home)
        fn()

    # ── UI HELPERS ────────────────────────────────────────────

    def _section_header(self, title: str, subtitle: str = ""):
        frm = tk.Frame(self.panel, bg=C["bg_main"])
        frm.pack(fill="x", padx=20, pady=(20, 4))
        tk.Label(frm, text=title, font=FONT["title"],
                 bg=C["bg_main"], fg=C["text_head"]).pack(anchor="w")
        if subtitle:
            tk.Label(frm, text=subtitle, font=FONT["body"],
                     bg=C["bg_main"], fg=C["text_dim"]).pack(anchor="w")
        sep = tk.Frame(self.panel, bg=C["border"], height=1)
        sep.pack(fill="x", padx=20, pady=(4, 12))

    def _card(self, parent=None, title: str = "", cols: int = 3):
        parent = parent or self.panel
        card = tk.LabelFrame(parent, text=f"  {title}  " if title else "",
                             font=FONT["small"], bg=C["bg_card"],
                             fg=C["accent"], bd=1, relief="flat",
                             highlightbackground=C["border"], highlightthickness=1)
        card.pack(fill="x", padx=20, pady=6)
        grid = tk.Frame(card, bg=C["bg_card"])
        grid.pack(fill="x", padx=8, pady=8)
        return grid, cols

    def _btn(self, parent, text: str, cmd, color=None, width=28):
        color = color or C["bg_btn"]
        b = tk.Button(parent, text=text, font=FONT["btn"], width=width,
                      bg=color, fg=C["text_head"], activebackground=C["bg_btn_h"],
                      activeforeground="white", relief="flat", cursor="hand2",
                      command=cmd, pady=6)
        b.bind("<Enter>", lambda e: b.configure(bg=C["bg_btn_h"]))
        b.bind("<Leave>", lambda e: b.configure(bg=color))
        return b

    def _grid_buttons(self, items, cols=3, color=None):
        """items: list of (label, command_string_or_callable)"""
        grid, _ = self._card(cols=cols)
        for i, (label, action) in enumerate(items):
            if callable(action):
                cmd = action
            else:
                cmd = lambda a=action, ps=action.startswith("Get-") or action.startswith("Set-"): \
                      self.runner.run(a, use_powershell=ps)
            btn = self._btn(grid, label, cmd, color=color)
            btn.grid(row=i // cols, column=i % cols, padx=6, pady=4, sticky="ew")
        for c in range(cols):
            grid.columnconfigure(c, weight=1)

    def _run_ps(self, cmd: str):
        self.runner.run(cmd, use_powershell=True)

    def _run_cmd(self, cmd: str):
        self.runner.run(cmd, use_powershell=False)

    # ─────────────────── SECTIONS ────────────────────────────

    def _section_home(self):
        self._section_header("⚡ ASPV Tools - Windows Premium",
                             "Suite completa de administración y optimización del sistema")

        # Info cards
        info = [
            ("📱 Drivers Android",   "Instala drivers USB para Samsung, Xiaomi, Huawei y más"),
            ("🖥️ Controladores",     "Actualiza y gestiona controladores de Windows"),
            ("⚡ Optimización",      "Mejora el rendimiento de Windows 11"),
            ("💻 Comandos CMD",      "Diagnóstico avanzado del sistema"),
            ("🔧 ADB & Fastboot",    "Herramientas de depuración Android"),
            ("🔓 FRP / MDM Bypass",  "Métodos de desbloqueo USB"),
            ("💾 Disco & Seguridad", "Gestión y protección de almacenamiento"),
            ("🌐 Red & WiFi",        "Diagnóstico y configuración de red"),
            ("🛡️ Anti-Spyware",     "Protección y limpieza del sistema"),
            ("ℹ️ Info del Sistema",  "Información detallada de hardware"),
        ]
        grid = tk.Frame(self.panel, bg=C["bg_main"])
        grid.pack(fill="x", padx=20, pady=8)
        for i, (title, desc) in enumerate(info):
            card = tk.Frame(grid, bg=C["bg_card"], relief="flat",
                            highlightbackground=C["border"], highlightthickness=1)
            card.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="ew")
            tk.Label(card, text=title, font=FONT["section"],
                     bg=C["bg_card"], fg=C["accent"]).pack(anchor="w", padx=12, pady=(10, 2))
            tk.Label(card, text=desc, font=FONT["small"],
                     bg=C["bg_card"], fg=C["text_dim"]).pack(anchor="w", padx=12, pady=(0, 10))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # System quick-info
        g2, _ = self._card(title="Información Rápida del Sistema")
        info_lines = [
            f"Sistema Operativo: {platform.system()} {platform.release()} ({platform.version()})",
            f"Arquitectura:      {platform.machine()}",
            f"Procesador:        {platform.processor() or 'N/A'}",
            f"Nombre del equipo: {platform.node()}",
            f"Python:            {sys.version}",
            f"Privilegios Admin: {'SÍ ✓' if is_admin() else 'NO ✗ (algunas funciones requieren admin)'}",
        ]
        for line in info_lines:
            tk.Label(g2, text=line, font=FONT["mono"],
                     bg=C["bg_card"], fg=C["text"]).pack(anchor="w", padx=4, pady=1)

    # ── ANDROID DRIVERS ──────────────────────────────────────

    def _section_android_drivers(self):
        self._section_header("📱 Drivers Android por Marca",
                             "Instala los drivers USB para depuración y gestión de dispositivos")

        brands = {
            "Samsung": [
                ("Samsung USB Driver (winget)", "winget install Samsung.USB.Driver"),
                ("Samsung Smart Switch",         "winget install Samsung.SmartSwitch"),
                ("Samsung Kies",                 "winget install Samsung.Kies3"),
            ],
            "Xiaomi / Redmi": [
                ("Xiaomi USB Driver",    "winget install Xiaomi.USBDriver"),
                ("Mi Flash Tool",        "winget install Xiaomi.MiFlash"),
                ("MIUI ADB Drivers",     'pnputil /add-driver "%SYSTEMROOT%\\INF\\wpdmtp.inf" /install'),
            ],
            "Huawei / Honor": [
                ("HiSuite (Huawei)",   "winget install Huawei.HiSuite"),
                ("Huawei USB Driver",  'pnputil /scan-devices'),
                ("HiLink Driver",      'devmgmt.msc'),
            ],
            "Motorola": [
                ("Motorola Device Manager", "winget install Motorola.DeviceManager"),
                ("Moto USB Driver",         'pnputil /add-driver "%SYSTEMROOT%\\INF\\wpdmtp.inf" /install'),
            ],
            "LG": [
                ("LG USB Driver",    "winget install LG.Mobile.Support.Tool"),
                ("LG Bridge",        "winget install LG.Bridge"),
            ],
            "OnePlus": [
                ("OnePlus USB Driver", "winget install OnePlus.USBDriver"),
                ("MTP Driver",         'pnputil /scan-devices'),
            ],
            "Google Pixel": [
                ("Google USB Driver",   "winget install Google.AndroidStudio"),
                ("ADB Interface Driver",'winget install Google.PlatformTools'),
            ],
            "OPPO / Realme": [
                ("OPPO USB Driver",  "winget install OPPO.USBDriver"),
                ("Realme Driver",    'pnputil /scan-devices'),
            ],
            "Vivo": [
                ("Vivo USB Driver",  "winget install Vivo.PCManager"),
            ],
            "Sony": [
                ("Sony Xperia Companion", "winget install Sony.XperiaCompanion"),
                ("PC Companion",          "winget install Sony.PCCompanion"),
            ],
        }

        for brand, actions in brands.items():
            grid, cols = self._card(title=brand)
            for i, (label, cmd) in enumerate(actions):
                btn = self._btn(grid, label,
                                lambda c=cmd: self._run_cmd(c),
                                color=C["bg_purple"])
                btn.grid(row=0, column=i, padx=6, pady=4, sticky="ew")
            for c in range(len(actions)):
                grid.columnconfigure(c, weight=1)

    # ── WINDOWS CONTROLLERS ──────────────────────────────────

    def _section_win_controllers(self):
        self._section_header("🖥️ Controladores de Windows",
                             "Gestiona y actualiza controladores del sistema")

        categories = {
            "Audio (Realtek)": [
                ("Instalar Realtek HD Audio",  "winget install RealtekSemiconductor.RealtekAudioDriver"),
                ("Actualizar Audio (Windows)", "Get-PnpDevice -Class Media | Update-PnpDeviceDriver"),
                ("Abrir Administrador Devices", "devmgmt.msc"),
            ],
            "WiFi & Bluetooth": [
                ("Buscar driver WiFi",      "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*Wireless*'}"),
                ("Actualizar driver WiFi",  "Get-PnpDevice -Class Net | Update-PnpDeviceDriver"),
                ("Estado Bluetooth",        "Get-PnpDevice -Class Bluetooth"),
            ],
            "Display / GPU": [
                ("Información GPU",         "Get-PnpDevice -Class Display"),
                ("Instalar NVIDIA (winget)", "winget install Nvidia.GeForceExperience"),
                ("Instalar AMD drivers",    "winget install AMD.AdrenalinEdition"),
                ("Instalar Intel Arc",      "winget install Intel.ArcControl"),
            ],
            "USB & Almacenamiento": [
                ("Ver dispositivos USB",    "Get-PnpDevice -Class USB"),
                ("Actualizar drivers USB",  "Get-PnpDevice -Class USB | Update-PnpDeviceDriver"),
                ("Estado discos",           "Get-Disk"),
            ],
            "Seguridad & TPM": [
                ("Estado TPM",             "Get-Tpm"),
                ("Info Secure Boot",       "Confirm-SecureBootUEFI"),
                ("Estado BitLocker",       "Get-BitLockerVolume"),
            ],
            "Red & Adaptadores": [
                ("Ver adaptadores red",    "Get-NetAdapter"),
                ("Estadísticas red",       "Get-NetAdapterStatistics"),
                ("Reset TCP/IP",           "netsh int ip reset"),
            ],
            "Cámara & Cast": [
                ("Ver cámaras",            "Get-PnpDevice -Class Camera"),
                ("Miracast info",          "netsh wlan show wirelesscapabilities"),
            ],
            "Lectores SD / USB": [
                ("Ver lectores SD",        "Get-PnpDevice -FriendlyName '*SD*'"),
                ("Escanear nuevos HW",     "pnputil /scan-devices"),
            ],
        }

        for cat, actions in categories.items():
            grid, cols = self._card(title=cat)
            for i, (label, cmd) in enumerate(actions):
                btn = self._btn(grid, label,
                                lambda c=cmd: self._run_ps(c))
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── OPTIMIZATION ─────────────────────────────────────────

    def _section_optimization(self):
        self._section_header("⚡ Optimización Windows 11",
                             "Mejora el rendimiento, limpia y repara el sistema")

        opts = {
            "Modo de Rendimiento": [
                ("Alto Rendimiento",        "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"),
                ("Máximo Rendimiento",      "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"),
                ("Equilibrado (default)",   "powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e"),
            ],
            "Limpieza del Sistema": [
                ("Limpiar archivos temp",   "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue"),
                ("Limpiar Prefetch",        "Remove-Item -Path C:\\Windows\\Prefetch\\* -Recurse -Force -ErrorAction SilentlyContinue"),
                ("Disk Cleanup silencioso", "cleanmgr /sagerun:1"),
                ("Vaciar papelera",         "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"),
            ],
            "Servicios del Sistema": [
                ("Deshabilitar SysMain",    "Stop-Service SysMain; Set-Service SysMain -StartupType Disabled"),
                ("Habilitar SysMain",       "Set-Service SysMain -StartupType Automatic; Start-Service SysMain"),
                ("Deshabilitar Xbox Live",  "Stop-Service XboxNetApiSvc; Set-Service XboxNetApiSvc -StartupType Disabled"),
                ("Ver servicios activos",   "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name, DisplayName"),
            ],
            "Optimización Gaming": [
                ("Game Mode ON",            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\GameBar' -Name 'AutoGameModeEnabled' -Value 1"),
                ("Deshabilitar Xbox Game Bar","Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR' -Name 'AppCaptureEnabled' -Value 0"),
                ("Prioridad CPU juegos",    "bcdedit /set useplatformtick yes"),
                ("Optimizar memoria RAM",   "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management' -Name 'ClearPageFileAtShutdown' -Value 0"),
            ],
            "Batería & Energía": [
                ("Informe batería",         "powercfg /batteryreport /output C:\\battery_report.html && start C:\\battery_report.html"),
                ("Diagnóstico energía",     "powercfg /energy /output C:\\energy_report.html && start C:\\energy_report.html"),
                ("Deshabilitar hibernación","powercfg /hibernate off"),
                ("Habilitar hibernación",   "powercfg /hibernate on"),
            ],
            "Reparación del Sistema": [
                ("SFC /scannow",            "sfc /scannow"),
                ("DISM RestoreHealth",      "DISM /Online /Cleanup-Image /RestoreHealth"),
                ("CHKDSK C:",               "echo Y | chkdsk C: /f /r /x"),
                ("Reiniciar Windows Update","Stop-Service wuauserv; Start-Service wuauserv"),
            ],
            "Visual & Animaciones": [
                ("Deshabilitar animaciones","Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects' -Name 'VisualFXSetting' -Value 2"),
                ("Activar modo oscuro",     "Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'AppsUseLightTheme' -Value 0"),
                ("Transparencia OFF",       "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'EnableTransparency' -Value 0"),
            ],
        }

        for cat, actions in opts.items():
            grid, cols = self._card(title=cat)
            for i, (label, cmd) in enumerate(actions):
                btn = self._btn(grid, label,
                                lambda c=cmd: self.runner.run(c, use_powershell=not c.startswith("sfc") and not c.startswith("DISM") and not c.startswith("echo") and not c.startswith("bcdedit") and not c.startswith("powercfg") and not c.startswith("cleanmgr")),
                                color=C["bg_btn"])
                btn.grid(row=i // 4, column=i % 4, padx=5, pady=4, sticky="ew")
            for c in range(4):
                grid.columnconfigure(c, weight=1)

    # ── CMD TOOLS ────────────────────────────────────────────

    def _section_cmd_tools(self):
        self._section_header("💻 Comandos CMD Avanzados",
                             "Diagnóstico del sistema, red, y comandos ocultos de Windows")

        cmds = {
            "Diagnóstico Sistema": [
                ("Información sistema (msinfo32)", "msinfo32"),
                ("Rendimiento CPU/RAM",            "wmic cpu get name,numberofcores,maxclockspeed && systeminfo | findstr /i 'memory'"),
                ("Procesos en ejecución",          "tasklist /v"),
                ("Variables de entorno",           "set"),
                ("Versión Windows",                "winver"),
            ],
            "Diagnóstico Red": [
                ("ipconfig /all",                  "ipconfig /all"),
                ("Ping Google",                    "ping -n 4 8.8.8.8"),
                ("Traceroute Google",              "tracert -d 8.8.8.8"),
                ("Puertos en uso (netstat)",       "netstat -ano"),
                ("DNS flush",                      "ipconfig /flushdns"),
                ("Limpiar caché ARP",              "arp -d"),
            ],
            "Disco & Archivos": [
                ("Listar discos (diskpart)",       "echo list disk | diskpart"),
                ("Directorios del sistema",        "dir C:\\ /a"),
                ("Atributos de archivos",          "attrib C:\\Windows\\System32\\*.dll | more"),
                ("Espacio en disco",               "wmic logicaldisk get name,size,freespace"),
            ],
            "Comandos Ocultos": [
                ("Calibrador pantalla",            "dccw"),
                ("Editor de directivas",           "gpedit.msc"),
                ("Administrador credenciales",     "control /name Microsoft.CredentialManager"),
                ("Fuentes del sistema",            "control fonts"),
                ("Administrador tareas (hidden)",  "resmon"),
                ("DirectX Diagnostic",             "dxdiag"),
                ("Opciones de accesibilidad",      "utilman"),
                ("Configurar arranque",            "msconfig"),
            ],
            "Seguridad & Registro": [
                ("Editor del registro",            "regedit"),
                ("Política de contraseñas",        "net accounts"),
                ("Usuarios del sistema",           "net user"),
                ("Grupos locales",                 "net localgroup"),
                ("Directivas seguridad local",     "secpol.msc"),
            ],
            "Personalizado": [],
        }

        for cat, actions in cmds.items():
            if cat == "Personalizado":
                grid, _ = self._card(title="Ejecutar Comando Personalizado")
                tk.Label(grid, text="Ingresa tu comando:", font=FONT["body"],
                         bg=C["bg_card"], fg=C["text"]).grid(row=0, column=0, padx=6, pady=4, sticky="w")
                entry = tk.Entry(grid, font=FONT["mono"], bg=C["output_bg"],
                                 fg=C["text"], insertbackground=C["accent"],
                                 relief="flat", width=50)
                entry.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
                tk.Button(grid, text="Ejecutar CMD", font=FONT["btn"],
                          bg=C["bg_btn"], fg="white", relief="flat", cursor="hand2",
                          command=lambda e=entry: self._run_cmd(e.get())).grid(
                    row=0, column=2, padx=6, pady=4)
                tk.Button(grid, text="Ejecutar PowerShell", font=FONT["btn"],
                          bg=C["bg_purple"], fg="white", relief="flat", cursor="hand2",
                          command=lambda e=entry: self._run_ps(e.get())).grid(
                    row=0, column=3, padx=6, pady=4)
                grid.columnconfigure(1, weight=1)
            else:
                grid, cols = self._card(title=cat)
                for i, (label, cmd) in enumerate(actions):
                    btn = self._btn(grid, label, lambda c=cmd: self._run_cmd(c))
                    btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
                for c in range(3):
                    grid.columnconfigure(c, weight=1)

    # ── ADB & FASTBOOT ───────────────────────────────────────

    def _section_adb_fastboot(self):
        self._section_header("🔧 ADB & Fastboot Setup",
                             "Instala y usa herramientas de depuración Android")

        setup = [
            ("Instalar Platform Tools (winget)", "winget install Google.PlatformTools"),
            ("Añadir ADB al PATH",               'setx PATH "%PATH%;%LOCALAPPDATA%\\Android\\Sdk\\platform-tools"'),
            ("Verificar ADB instalado",          "adb version"),
            ("Verificar Fastboot",               "fastboot --version"),
        ]

        devices = [
            ("Listar dispositivos ADB",   "adb devices"),
            ("Reboot to recovery",         "adb reboot recovery"),
            ("Reboot to bootloader",       "adb reboot bootloader"),
            ("ADB Shell",                  "adb shell"),
            ("ADB over WiFi (puerto 5555)","adb tcpip 5555"),
            ("Pull archivo del dispositivo","adb pull /sdcard/DCIM/Camera ."),
        ]

        fastboot_cmds = [
            ("Fastboot devices",          "fastboot devices"),
            ("Desbloquear bootloader",    "fastboot oem unlock"),
            ("Bloquear bootloader",       "fastboot oem lock"),
            ("Flash boot.img",            "fastboot flash boot boot.img"),
            ("Flash recovery.img",        "fastboot flash recovery recovery.img"),
            ("Borrar caché (fastboot)",   "fastboot erase cache"),
            ("Reiniciar desde fastboot",  "fastboot reboot"),
        ]

        sideload = [
            ("ADB Sideload ROM",          "adb sideload update.zip"),
            ("Instalar APK",              "adb install app.apk"),
            ("Instalar APK (degradar)",   "adb install -d app.apk"),
            ("Listar paquetes instalados","adb shell pm list packages"),
        ]

        for title, items in [("Instalación & Configuración", setup),
                              ("Gestión de Dispositivos", devices),
                              ("Comandos Fastboot", fastboot_cmds),
                              ("Sideload & APK", sideload)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                btn = self._btn(grid, label, lambda c=cmd: self._run_cmd(c),
                                color=C["bg_purple"])
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── USB DEBUGGING / FRP ──────────────────────────────────

    def _section_usb_debug(self):
        self._section_header("🔓 USB Debugging & FRP/MDM",
                             "Métodos de depuración USB y bypass de bloqueos para uso educativo/recuperación")

        tk.Label(self.panel, text="⚠️  AVISO: Estas herramientas son para uso educativo y recuperación de dispositivos propios únicamente.",
                 font=FONT["body"], bg=C["bg_main"], fg=C["warning"],
                 wraplength=800, justify="left").pack(padx=20, pady=(0, 8), anchor="w")

        usb_debug = [
            ("Habilitar USB Debugging (ADB)", "adb shell settings put global adb_enabled 1"),
            ("Verificar depuración USB",       "adb shell settings get global adb_enabled"),
            ("Ver info del dispositivo",       "adb shell getprop ro.product.model"),
            ("Ver versión Android",            "adb shell getprop ro.build.version.release"),
        ]

        frp = [
            ("Info FRP (ADB shell)",           "adb shell content query --uri content://settings/secure --projection name:value --where \"name='android_id'\""),
            ("Factory Reset (ADB)",            "adb shell recovery --wipe_data"),
            ("Limpiar datos app Settings",     "adb shell pm clear com.android.settings"),
            ("Abrir Ajustes de cuenta (ADB)",  "adb shell am start -n com.android.settings/.Settings"),
        ]

        mdm = [
            ("Listar admin activos",           "adb shell dpm list-owners"),
            ("Info MDM administrador",         "adb shell dumpsys device_policy"),
            ("Ver políticas activas",          "adb shell dumpsys devicepolicymanager"),
        ]

        for title, items in [("USB Debugging", usb_debug),
                              ("FRP (Factory Reset Protection)", frp),
                              ("MDM (Mobile Device Management)", mdm)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                btn = self._btn(grid, label, lambda c=cmd: self._run_cmd(c),
                                color=C["bg_btn"])
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── USB DEVICES ──────────────────────────────────────────

    def _section_usb_devices(self):
        self._section_header("📡 Dispositivos Conectados",
                             "Detecta y gestiona dispositivos conectados por USB")

        scan = [
            ("Escanear dispositivos USB",     "Get-PnpDevice -Class USB | Select-Object Status, Class, FriendlyName, InstanceId"),
            ("Ver puertos COM",               "Get-WMIObject Win32_SerialPort | Select-Object Name, DeviceID, Description"),
            ("Ver discos externos",           "Get-Disk | Where-Object {$_.BusType -eq 'USB'} | Select-Object FriendlyName, Size"),
            ("Dispositivos ADB conectados",   "adb devices"),
            ("Escanear nuevos HW (pnputil)",  "pnputil /scan-devices"),
            ("Árbol de dispositivos",         "devcon find *"),
            ("Ver info HID",                  "Get-PnpDevice -Class HIDClass | Select-Object Status, FriendlyName"),
            ("Eyectar disco USB seguro",      "([wmiclass]'Win32_Volume').GetInstances() | Where-Object {$_.DriveType -eq 2} | ForEach-Object {$_.Dismount($true, $false)}"),
        ]

        grid, cols = self._card(title="Escaneo y Gestión USB")
        for i, (label, cmd) in enumerate(scan):
            is_ps = not cmd.startswith("adb") and not cmd.startswith("pnputil") and not cmd.startswith("devcon")
            btn = self._btn(grid, label, lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

        # Live refresh button
        frm = tk.Frame(self.panel, bg=C["bg_main"])
        frm.pack(fill="x", padx=20, pady=4)
        self._btn(frm, "🔄 Actualizar lista de dispositivos USB",
                  lambda: self._run_ps("Get-PnpDevice | Where-Object {$_.Status -eq 'OK'} | Select-Object Class, FriendlyName, Status | Sort-Object Class"),
                  color=C["success"], width=40).pack(side="left", padx=4)

    # ── DISK TOOLS ───────────────────────────────────────────

    def _section_disk_tools(self):
        self._section_header("💾 Herramientas de Disco",
                             "Gestión de disco, cifrado, carpetas protegidas y más")

        disk_info = [
            ("Ver discos (Get-Disk)",          "Get-Disk | Select-Object Number, FriendlyName, Size, PartitionStyle"),
            ("Particiones",                    "Get-Partition | Select-Object DriveLetter, Size, Type"),
            ("Espacio libre",                  "Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free"),
            ("Discos físicos (WMIC)",          "wmic diskdrive get model,serialnumber,size"),
        ]

        disk_manage = [
            ("Abrir Administración de discos", "diskmgmt.msc"),
            ("Lanzar DiskPart",                "start cmd /k diskpart"),
            ("CHKDSK C: (reparar)",            "echo Y | chkdsk C: /f"),
            ("Desfragmentar C:",               "defrag C: /U /V"),
            ("Optimizar SSD C:",               "Optimize-Volume -DriveLetter C -ReTrim -Verbose"),
        ]

        protection = [
            ("Activar BitLocker C:",           "Enable-BitLocker -MountPoint 'C:' -EncryptionMethod XtsAes256 -UsedSpaceOnly"),
            ("Estado BitLocker",               "Get-BitLockerVolume"),
            ("Suspender BitLocker",            "Suspend-BitLocker -MountPoint 'C:'"),
            ("Desactivar BitLocker C:",        "Disable-BitLocker -MountPoint 'C:'"),
        ]

        folder_lock = [
            ("Crear carpeta oculta",           'attrib +h +s "C:\\CarpetaOculta"'),
            ("Mostrar carpeta oculta",         'attrib -h -s "C:\\CarpetaOculta"'),
            ("Ver archivos ocultos",           "Get-ChildItem -Force C:\\ | Where-Object {$_.Attributes -match 'Hidden'}"),
        ]

        for title, items in [("Información de Disco", disk_info),
                              ("Gestión de Disco", disk_manage),
                              ("Cifrado BitLocker", protection),
                              ("Carpetas y Archivos", folder_lock)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                is_ps = not any(cmd.startswith(x) for x in ["diskmgmt", "start", "echo", "attrib", "defrag", "wmic"])
                btn = self._btn(grid, label,
                                lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps))
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── SYSTEM ICONS ─────────────────────────────────────────

    def _section_system_icons(self):
        self._section_header("🖼️ Íconos del Sistema",
                             "Personaliza y restaura íconos de escritorio y sistema")

        icons = [
            ("Restaurar íconos de escritorio",   "$code='[DllImport(\\'Shell32.dll\\', CharSet = CharSet.Auto)][return: MarshalAs(UnmanagedType.Bool)]public static extern bool ShellExecuteEx(ref SHELLEXECUTEINFO lpExecInfo);'; Add-Type -MemberDefinition $code -Name Shell32 -Namespace Shell32; SHChangeNotify(0x8000000, 0, 0, 0)"),
            ("Actualizar caché de íconos",       "ie4uinit.exe -ClearIconCache"),
            ("Reconstruir caché íconos",         "taskkill /F /IM explorer.exe && del /F /Q %localappdata%\\IconCache.db && start explorer.exe"),
            ("Abrir Config. íconos escritorio",  "start ms-settings:themes"),
            ("Cambiar ícono carpeta",            "shell32.dll"),
            ("Resetear íconos por defecto",      "reg delete 'HKCU\\Software\\Classes\\CLSID' /f; reg delete 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3' /f"),
        ]

        grid, cols = self._card(title="Gestión de Íconos")
        for i, (label, cmd) in enumerate(icons):
            btn = self._btn(grid, label,
                            lambda c=cmd: self.runner.run(c, use_powershell=c.startswith("[") or c.startswith("reg")))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

    # ── ANTI-SPYWARE ─────────────────────────────────────────

    def _section_anti_spyware(self):
        self._section_header("🛡️ Anti-Spyware & Privacidad",
                             "Scripts para mejorar privacidad y eliminar telemetría de Windows")

        privacy = [
            ("Deshabilitar telemetría",          "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Value 0 -Force"),
            ("Deshabilitar DiagTrack",           "Stop-Service DiagTrack; Set-Service DiagTrack -StartupType Disabled"),
            ("Bloquear servidor telemetría",     'Add-Content -Path "C:\\Windows\\System32\\drivers\\etc\\hosts" -Value "0.0.0.0 vortex.data.microsoft.com"'),
            ("Deshabilitar publicidad dirigida", "Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo' -Name 'Enabled' -Value 0"),
            ("Deshabilitar Cortana",             "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search' -Name 'AllowCortana' -Value 0"),
            ("Deshabilitar rastreo ubicación",   "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Sensor\\Overrides\\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}' -Name 'SensorPermissionState' -Value 0"),
        ]

        defender = [
            ("Estado Windows Defender",          "Get-MpComputerStatus | Select-Object AMRunningMode, AntispywareEnabled, AntivirusEnabled"),
            ("Análisis rápido Defender",         "Start-MpScan -ScanType QuickScan"),
            ("Análisis completo Defender",       "Start-MpScan -ScanType FullScan"),
            ("Actualizar definiciones",          "Update-MpSignature"),
            ("Ver amenazas detectadas",          "Get-MpThreatDetection"),
            ("Limpiar amenazas",                 "Remove-MpThreat"),
        ]

        cleanup = [
            ("Limpiar prefetch",                 "Remove-Item -Path C:\\Windows\\Prefetch\\* -Force -ErrorAction SilentlyContinue"),
            ("Limpiar logs de eventos",          "Get-EventLog -LogName * | ForEach-Object {Clear-EventLog $_.Log}"),
            ("Limpiar historial DNS",            "ipconfig /flushdns"),
            ("Borrar historial PowerShell",      "Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue"),
            ("Limpiar historial Explorer",       "reg delete 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU' /va /f"),
        ]

        for title, items in [("Privacidad & Telemetría", privacy),
                              ("Windows Defender", defender),
                              ("Limpieza de Historial", cleanup)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                btn = self._btn(grid, label, lambda c=cmd: self._run_ps(c),
                                color=C["bg_purple"])
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── USB REPAIR ───────────────────────────────────────────

    def _section_usb_repair(self):
        self._section_header("🔌 Reparar USB",
                             "Soluciona problemas de dispositivos USB no detectados")

        repair = [
            ("Reiniciar servicio USB (UsbStor)",  "Stop-Service UsbStor; Start-Service UsbStor"),
            ("Reinstalar drivers USB HID",         "Get-PnpDevice -Class HIDClass | Disable-PnpDevice -Confirm:$false; Get-PnpDevice -Class HIDClass | Enable-PnpDevice -Confirm:$false"),
            ("Escanear cambios de HW",             "pnputil /scan-devices"),
            ("Limpiar controladores USB huérfanos","pnputil /enum-drivers | Select-String 'USB'"),
            ("Restablecer USB (devmgmt)",          "devmgmt.msc"),
            ("Desinstalar dispositivos USB",       "Get-PnpDevice -Class USB | Where-Object{$_.Status -ne 'OK'} | Disable-PnpDevice -Confirm:$false"),
            ("Habilitar todos los USB",            "Get-PnpDevice -Class USB | Enable-PnpDevice -Confirm:$false"),
            ("Ver log errores USB",                "Get-WinEvent -LogName System | Where-Object {$_.Message -like '*USB*'} | Select-Object TimeCreated, Message -First 20"),
            ("Reset Bus USB (Power Shell)",        "Restart-Service HidServ; Restart-Service UsbStor"),
        ]

        grid, cols = self._card(title="Herramientas de Reparación USB")
        for i, (label, cmd) in enumerate(repair):
            is_ps = not any(cmd.startswith(x) for x in ["pnputil", "devmgmt"])
            btn = self._btn(grid, label,
                            lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps),
                            color=C["warning"])
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

    # ── SECURITY ─────────────────────────────────────────────

    def _section_security(self):
        self._section_header("🔒 Seguridad Windows",
                             "Firewall, Windows Defender, usuarios y políticas de seguridad")

        firewall = [
            ("Estado del Firewall",           "Get-NetFirewallProfile | Select-Object Name, Enabled"),
            ("Activar Firewall (todos)",      "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"),
            ("Desactivar Firewall",           "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"),
            ("Ver reglas de entrada",         "Get-NetFirewallRule -Direction Inbound | Select-Object DisplayName, Enabled, Action | Format-Table -AutoSize"),
            ("Bloquear IP específica",        'New-NetFirewallRule -DisplayName "BlockIP" -Direction Inbound -LocalPort Any -Protocol TCP -Action Block -RemoteAddress 0.0.0.0'),
        ]

        users = [
            ("Listar usuarios locales",       "Get-LocalUser | Select-Object Name, Enabled, LastLogon"),
            ("Crear usuario local",           'New-LocalUser -Name "NuevoUsuario" -Password (ConvertTo-SecureString "Pass1234!" -AsPlainText -Force) -FullName "Nuevo Usuario"'),
            ("Eliminar usuario",              'Remove-LocalUser -Name "NuevoUsuario"'),
            ("Ver grupos locales",            "Get-LocalGroup"),
            ("Agregar usuario a admins",      'Add-LocalGroupMember -Group "Administrators" -Member "NuevoUsuario"'),
        ]

        policies = [
            ("Auditoría de inicio de sesión", "auditpol /set /category:'Logon/Logoff' /success:enable /failure:enable"),
            ("Ver política de contraseñas",   "net accounts"),
            ("Bloquear cuenta tras 5 fallos", "net accounts /lockoutthreshold:5"),
            ("Abrir secpol.msc",              "secpol.msc"),
            ("Abrir gpedit.msc",              "gpedit.msc"),
        ]

        for title, items in [("Firewall", firewall),
                              ("Usuarios y Grupos", users),
                              ("Políticas de Seguridad", policies)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                is_ps = not any(cmd.startswith(x) for x in ["auditpol", "net ", "secpol", "gpedit"])
                btn = self._btn(grid, label,
                                lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps),
                                color=C["danger"])
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── NETWORK ──────────────────────────────────────────────

    def _section_network(self):
        self._section_header("🌐 Red & WiFi",
                             "Diagnóstico, configuración y gestión de red")

        diag = [
            ("IP Config completo",           "ipconfig /all"),
            ("Ping Google",                  "ping -n 4 google.com"),
            ("Tracert Google",               "tracert -d google.com"),
            ("Estadísticas red",             "netstat -s"),
            ("Puertos abiertos",             "netstat -ano"),
            ("Tabla ARP",                    "arp -a"),
            ("Tabla de rutas",               "route print"),
        ]

        wifi = [
            ("Ver redes WiFi disponibles",   "netsh wlan show networks mode=bssid"),
            ("Perfil WiFi actual",           "netsh wlan show interfaces"),
            ("Mostrar perfiles guardados",   "netsh wlan show profiles"),
            ("Ver contraseña WiFi guardada", 'netsh wlan show profile name="MiRed" key=clear'),
            ("Desconectar WiFi",             "netsh wlan disconnect"),
            ("Activar WiFi (hostelería)",    "netsh wlan start hostednetwork"),
        ]

        reset = [
            ("Flush DNS",                    "ipconfig /flushdns"),
            ("Release & Renew IP",           "ipconfig /release && ipconfig /renew"),
            ("Reset TCP/IP",                 "netsh int ip reset"),
            ("Reset Winsock",                "netsh winsock reset"),
            ("Reset IPv6",                   "netsh int ipv6 reset"),
            ("Renovar DHCP",                 "ipconfig /renew"),
        ]

        for title, items in [("Diagnóstico", diag),
                              ("WiFi", wifi),
                              ("Reparación de Red", reset)]:
            grid, cols = self._card(title=title)
            for i, (label, cmd) in enumerate(items):
                btn = self._btn(grid, label, lambda c=cmd: self._run_cmd(c))
                btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
            for c in range(3):
                grid.columnconfigure(c, weight=1)

    # ── AUDIO ────────────────────────────────────────────────

    def _section_audio(self):
        self._section_header("🔊 Herramientas de Audio",
                             "Gestión y diagnóstico del sistema de sonido")

        audio = [
            ("Ver dispositivos de audio",       "Get-PnpDevice -Class Media | Select-Object Status, FriendlyName"),
            ("Reiniciar servicio de audio",     "Stop-Service Audiosrv; Start-Service Audiosrv"),
            ("Reiniciar AudioEndpointBuilder",  "Stop-Service AudioEndpointBuilder; Start-Service AudioEndpointBuilder"),
            ("Abrir mezclador de volumen",      "sndvol"),
            ("Abrir Config. de sonido",         "mmsys.cpl"),
            ("Abrir Config. sonido (Settings)", "start ms-settings:sound"),
            ("Instalar Realtek Audio",          "winget install RealtekSemiconductor.RealtekAudioDriver"),
            ("Ver controladores de audio",      "Get-WMIObject Win32_SoundDevice | Select-Object Name, Status, Manufacturer"),
            ("Test de sonido (Diagnostics)",    "msdt.exe /id AudioPlaybackDiagnostic"),
        ]

        grid, cols = self._card(title="Gestión de Audio")
        for i, (label, cmd) in enumerate(audio):
            is_ps = cmd.startswith("Get-") or cmd.startswith("Stop-") or cmd.startswith("Start-") or cmd.startswith("Restart-")
            btn = self._btn(grid, label,
                            lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

    # ── PRINTERS ─────────────────────────────────────────────

    def _section_printers(self):
        self._section_header("🖨️ Gestión de Impresoras",
                             "Administra impresoras y colas de impresión")

        printers = [
            ("Ver impresoras instaladas",     "Get-Printer | Select-Object Name, DriverName, PortName, PrinterStatus"),
            ("Ver cola de impresión",         "Get-PrintJob -PrinterName (Get-Printer | Select-Object -First 1).Name"),
            ("Cancelar todos los trabajos",   "Get-Printer | Get-PrintJob | Remove-PrintJob"),
            ("Reiniciar Spooler",             "Stop-Service Spooler; Start-Service Spooler"),
            ("Abrir Config. impresoras",      "control printers"),
            ("Abrir admin. impresoras",       "printmanagement.msc"),
            ("Ver drivers de impresora",      "Get-PrinterDriver | Select-Object Name, Manufacturer"),
            ("Limpiar cola atascada",         "Stop-Service Spooler; Remove-Item -Path C:\\Windows\\System32\\spool\\PRINTERS\\* -Force -ErrorAction SilentlyContinue; Start-Service Spooler"),
            ("Agregar impresora de red",      'Add-Printer -ConnectionName "\\\\servidor\\impresora"'),
        ]

        grid, cols = self._card(title="Gestión de Impresoras")
        for i, (label, cmd) in enumerate(printers):
            is_ps = not any(cmd.startswith(x) for x in ["control", "printmanagement"])
            btn = self._btn(grid, label,
                            lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)

    # ── SYSINFO ──────────────────────────────────────────────

    def _section_sysinfo(self):
        self._section_header("ℹ️ Información del Sistema",
                             "Información detallada de hardware y software")

        # Static info
        card_frm = tk.LabelFrame(self.panel, text="  Información del Equipo  ",
                                 font=FONT["small"], bg=C["bg_card"],
                                 fg=C["accent"], bd=1, relief="flat",
                                 highlightbackground=C["border"], highlightthickness=1)
        card_frm.pack(fill="x", padx=20, pady=6)

        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            hostname, local_ip = "N/A", "N/A"

        static_info = {
            "Sistema Operativo":    f"{platform.system()} {platform.release()} ({platform.version()})",
            "Arquitectura":         platform.machine(),
            "Procesador":           platform.processor() or "N/A",
            "Nodo (hostname)":      platform.node(),
            "IP Local":             local_ip,
            "Python":               sys.version,
            "Directorio Personal":  os.path.expanduser("~"),
            "Directorio Actual":    os.getcwd(),
            "Admin Activo":         "SÍ" if is_admin() else "NO",
        }

        for k, v in static_info.items():
            row = tk.Frame(card_frm, bg=C["bg_card"])
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text=f"{k}:", font=FONT["btn"], width=22,
                     bg=C["bg_card"], fg=C["accent"], anchor="w").pack(side="left")
            tk.Label(row, text=v, font=FONT["mono"],
                     bg=C["bg_card"], fg=C["text"], anchor="w").pack(side="left")

        # Dynamic queries
        queries = [
            ("CPU detallado",             "Get-WMIObject Win32_Processor | Select-Object Name, MaxClockSpeed, NumberOfCores, NumberOfLogicalProcessors"),
            ("RAM instalada",             "Get-WMIObject Win32_PhysicalMemory | Select-Object BankLabel, Capacity, Speed, Manufacturer"),
            ("Placa base",                "Get-WMIObject Win32_BaseBoard | Select-Object Manufacturer, Product, SerialNumber"),
            ("BIOS / UEFI",               "Get-WMIObject Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate"),
            ("GPU",                       "Get-WMIObject Win32_VideoController | Select-Object Name, AdapterRAM, CurrentRefreshRate"),
            ("Discos duros",              "Get-WMIObject Win32_DiskDrive | Select-Object Model, Size, MediaType, SerialNumber"),
            ("Red: IPs y MACs",           "Get-NetAdapter | Where-Object{$_.Status -eq 'Up'} | Select-Object Name, MacAddress, LinkSpeed"),
            ("Temperatura CPU (si disp.)","Get-WMIObject MSAcpi_ThermalZoneTemperature -Namespace 'root/wmi' | Select-Object InstanceName, CurrentTemperature"),
            ("Reporte completo (msinfo32)","msinfo32"),
        ]

        grid, cols = self._card(title="Consultas Detalladas de Hardware")
        for i, (label, cmd) in enumerate(queries):
            is_ps = not cmd.startswith("msinfo32")
            btn = self._btn(grid, label,
                            lambda c=cmd, ps=is_ps: self.runner.run(c, use_powershell=ps))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=4, sticky="ew")
        for c in range(3):
            grid.columnconfigure(c, weight=1)


# ─────────────────────── ENTRY POINT ────────────────────────

def main():
    # On Windows, request admin if not already elevated
    if sys.platform == "win32":
        if not is_admin():
            resp = ctypes.windll.user32.MessageBoxW(
                0,
                "ASPV Tools requiere privilegios de Administrador para todas sus funciones.\n\n"
                "¿Deseas reiniciar como Administrador?",
                "ASPV Tools - Privilegios Requeridos",
                0x24  # MB_YESNO | MB_ICONQUESTION
            )
            if resp == 6:  # IDYES
                request_admin()
            # Continue without admin if user says No

    app = ASPVTools()
    app.mainloop()


if __name__ == "__main__":
    main()
