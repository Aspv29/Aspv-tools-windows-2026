/**
 * ASPV Tools Premium v3.0 - Renderer Process
 * ===========================================
 * Main UI logic and section management
 */

// ═══════════════════════════════════════════════════════════
// NAVIGATION CONFIGURATION
// ═══════════════════════════════════════════════════════════

const NAVIGATION = [
  { id: 'home', icon: '🏠', label: 'Inicio' },
  { id: 'android-drivers', icon: '📱', label: 'Drivers Android' },
  { id: 'win-controllers', icon: '🖥️', label: 'Controladores Windows' },
  { id: 'optimization', icon: '⚡', label: 'Optimización Win11' },
  { id: 'cmd-tools', icon: '💻', label: 'Comandos CMD' },
  { id: 'adb-fastboot', icon: '🔧', label: 'ADB & Fastboot' },
  { id: 'usb-debug', icon: '🔓', label: 'USB Debugging / FRP' },
  { id: 'usb-devices', icon: '📡', label: 'Dispositivos USB' },
  { id: 'disk-tools', icon: '💾', label: 'Herramientas Disco' },
  { id: 'system-icons', icon: '🖼️', label: 'Íconos del Sistema' },
  { id: 'anti-spyware', icon: '🛡️', label: 'Anti-Spyware' },
  { id: 'usb-repair', icon: '🔌', label: 'Reparar USB' },
  { id: 'security', icon: '🔒', label: 'Seguridad Windows' },
  { id: 'network', icon: '🌐', label: 'Red & WiFi' },
  { id: 'audio', icon: '🔊', label: 'Audio' },
  { id: 'printers', icon: '🖨️', label: 'Impresoras' },
  { id: 'sysinfo', icon: 'ℹ️', label: 'Info del Sistema' },
  { id: 'bootable', icon: '💿', label: 'USB Booteable' },
  { id: 'developer', icon: '👨‍💻', label: 'Herramientas Dev' }
];

// ═══════════════════════════════════════════════════════════
// STATE MANAGEMENT
// ═══════════════════════════════════════════════════════════

let currentSection = 'home';
let systemInfo = null;

// ═══════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', async () => {
  initTitleBar();
  initNavigation();
  await loadSystemInfo();
  showSection('home');
  setupTerminalControls();
});

// ═══════════════════════════════════════════════════════════
// TITLE BAR
// ═══════════════════════════════════════════════════════════

function initTitleBar() {
  document.getElementById('minimize-btn').addEventListener('click', () => {
    window.aspv.minimize();
  });

  document.getElementById('maximize-btn').addEventListener('click', () => {
    window.aspv.maximize();
  });

  document.getElementById('close-btn').addEventListener('click', () => {
    window.aspv.close();
  });
}

// ═══════════════════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════════════════

function initNavigation() {
  const nav = document.getElementById('sidebar-nav');
  
  NAVIGATION.forEach(item => {
    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.section = item.id;
    btn.innerHTML = `
      <span class="nav-item-icon">${item.icon}</span>
      <span class="nav-item-text">${item.label}</span>
    `;
    btn.addEventListener('click', () => showSection(item.id));
    nav.appendChild(btn);
  });
}

function showSection(sectionId) {
  currentSection = sectionId;
  
  // Update navigation
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.section === sectionId);
  });
  
  // Get section config
  const section = SECTIONS[sectionId] || SECTIONS.home;
  
  // Update header
  document.getElementById('content-title').textContent = section.title;
  document.getElementById('content-subtitle').textContent = section.subtitle;
  
  // Render content
  const contentBody = document.getElementById('content-body');
  contentBody.innerHTML = '';
  section.render(contentBody);
  
  updateStatus('Listo');
}

// ═══════════════════════════════════════════════════════════
// SYSTEM INFO
// ═══════════════════════════════════════════════════════════

async function loadSystemInfo() {
  try {
    systemInfo = await window.aspv.getSystemInfo();
    const appInfo = await window.aspv.getAppInfo();
    
    // Update status bar
    const statusInfo = `${appInfo.platform} | Node ${appInfo.nodeVersion} | Electron ${appInfo.electronVersion}`;
    document.getElementById('system-info').textContent = statusInfo;
    
    // Check admin status (Windows only)
    if (appInfo.platform === 'win32') {
      try {
        const result = await executeCommand('net session', false);
        const isAdmin = result.success && !result.stderr.includes('Access is denied');
        updateAdminBadge(isAdmin);
      } catch {
        updateAdminBadge(false);
      }
    }
  } catch (err) {
    console.error('Error loading system info:', err);
  }
}

function updateAdminBadge(isAdmin) {
  const badge = document.getElementById('admin-badge');
  if (isAdmin) {
    badge.className = 'admin-badge is-admin';
    badge.innerHTML = '<span class="badge-icon">●</span><span class="badge-text">Admin</span>';
  } else {
    badge.className = 'admin-badge no-admin';
    badge.innerHTML = '<span class="badge-icon">○</span><span class="badge-text">Sin Admin</span>';
  }
}

// ═══════════════════════════════════════════════════════════
// COMMAND EXECUTION
// ═══════════════════════════════════════════════════════════

async function executeCommand(command, usePowerShell = false, admin = false) {
  showLoading(true);
  updateStatus('Ejecutando comando...');
  addTerminalLine(`> ${command}`, 'command');
  
  try {
    const result = await window.aspv.executeCommand({
      command,
      admin,
      shell: usePowerShell ? 'powershell' : 'cmd'
    });
    
    if (result.stdout) {
      addTerminalLine(result.stdout, 'output');
    }
    
    if (result.stderr) {
      addTerminalLine(result.stderr, 'error');
    }
    
    if (result.success) {
      addTerminalLine('[OK] Comando completado con éxito', 'success');
      updateStatus('Completado con éxito');
    } else {
      addTerminalLine(`[ERROR] ${result.error || 'Error desconocido'}`, 'error');
      updateStatus('Error al ejecutar comando');
    }
    
    return result;
  } catch (err) {
    addTerminalLine(`[ERROR] ${err.message}`, 'error');
    updateStatus('Error al ejecutar comando');
    return { success: false, error: err.message };
  } finally {
    showLoading(false);
  }
}

// ═══════════════════════════════════════════════════════════
// TERMINAL
// ═══════════════════════════════════════════════════════════

function addTerminalLine(text, type = 'output') {
  const terminal = document.getElementById('terminal-output');
  const line = document.createElement('div');
  line.className = `terminal-line ${type}`;
  line.textContent = text;
  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

function clearTerminal() {
  const terminal = document.getElementById('terminal-output');
  terminal.innerHTML = '<div class="terminal-line welcome">Terminal limpiado - Listo para nuevos comandos</div>';
}

function copyTerminal() {
  const terminal = document.getElementById('terminal-output');
  const text = terminal.innerText;
  navigator.clipboard.writeText(text).then(() => {
    updateStatus('Contenido del terminal copiado al portapapeles');
  });
}

function setupTerminalControls() {
  document.getElementById('clear-terminal').addEventListener('click', clearTerminal);
  document.getElementById('copy-terminal').addEventListener('click', copyTerminal);
}

// ═══════════════════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════════════════

function updateStatus(text) {
  document.getElementById('status-text').textContent = text;
}

function showLoading(show) {
  const overlay = document.getElementById('loading-overlay');
  overlay.classList.toggle('active', show);
}

function createCard(title, icon = '') {
  const card = document.createElement('div');
  card.className = 'card';
  
  const header = document.createElement('div');
  header.className = 'card-header';
  header.innerHTML = `<span class="card-title">${icon} ${title}</span>`;
  
  const body = document.createElement('div');
  body.className = 'card-body';
  
  card.appendChild(header);
  card.appendChild(body);
  
  return { card, body };
}

function createButton(text, onClick, className = 'btn-primary') {
  const btn = document.createElement('button');
  btn.className = `btn ${className}`;
  btn.textContent = text;
  btn.addEventListener('click', onClick);
  return btn;
}

function createButtonGrid(buttons) {
  const grid = document.createElement('div');
  grid.className = 'btn-grid';
  buttons.forEach(btn => grid.appendChild(btn));
  return grid;
}

function createInfoCard(icon, title, description, onClick) {
  const card = document.createElement('div');
  card.className = 'info-card';
  card.innerHTML = `
    <div class="info-card-icon">${icon}</div>
    <div class="info-card-title">${title}</div>
    <div class="info-card-desc">${description}</div>
  `;
  if (onClick) {
    card.addEventListener('click', onClick);
  }
  return card;
}

// ═══════════════════════════════════════════════════════════
// SECTION DEFINITIONS
// ═══════════════════════════════════════════════════════════

const SECTIONS = {
  // ─────────────────────── HOME ───────────────────────
  home: {
    title: '⚡ ASPV Tools - Windows Premium',
    subtitle: 'Suite completa de administración y optimización del sistema',
    render: (container) => {
      const infoCards = [
        { icon: '📱', title: 'Drivers Android', desc: 'Instala drivers USB para Samsung, Xiaomi, Huawei y más', section: 'android-drivers' },
        { icon: '🖥️', title: 'Controladores', desc: 'Actualiza y gestiona controladores de Windows', section: 'win-controllers' },
        { icon: '⚡', title: 'Optimización', desc: 'Mejora el rendimiento de Windows 11', section: 'optimization' },
        { icon: '💻', title: 'Comandos CMD', desc: 'Diagnóstico avanzado del sistema', section: 'cmd-tools' },
        { icon: '🔧', title: 'ADB & Fastboot', desc: 'Herramientas de depuración Android', section: 'adb-fastboot' },
        { icon: '🔓', title: 'FRP / MDM Bypass', desc: 'Métodos de desbloqueo USB', section: 'usb-debug' },
        { icon: '💾', title: 'Disco & Seguridad', desc: 'Gestión y protección de almacenamiento', section: 'disk-tools' },
        { icon: '🌐', title: 'Red & WiFi', desc: 'Diagnóstico y configuración de red', section: 'network' },
        { icon: '🛡️', title: 'Anti-Spyware', desc: 'Protección y limpieza del sistema', section: 'anti-spyware' },
        { icon: 'ℹ️', title: 'Info del Sistema', desc: 'Información detallada de hardware', section: 'sysinfo' }
      ];
      
      const grid = document.createElement('div');
      grid.className = 'card-body';
      
      infoCards.forEach(item => {
        const card = createInfoCard(item.icon, item.title, item.desc, () => showSection(item.section));
        grid.appendChild(card);
      });
      
      container.appendChild(grid);
      
      // System quick info
      if (systemInfo) {
        const { card, body } = createCard('Información Rápida del Sistema', 'ℹ️');
        const info = [
          ['Sistema Operativo', `${systemInfo.osType} ${systemInfo.osRelease}`],
          ['Arquitectura', systemInfo.arch],
          ['Hostname', systemInfo.hostname],
          ['CPUs', `${systemInfo.cpus.length} cores - ${systemInfo.cpus[0]?.model || 'N/A'}`],
          ['RAM Total', `${(systemInfo.totalMemory / 1024 / 1024 / 1024).toFixed(2)} GB`],
          ['RAM Libre', `${(systemInfo.freeMemory / 1024 / 1024 / 1024).toFixed(2)} GB`],
          ['Uptime', `${Math.floor(systemInfo.uptime / 3600)} horas`]
        ];
        
        info.forEach(([label, value]) => {
          const row = document.createElement('div');
          row.className = 'info-row';
          row.innerHTML = `
            <div class="info-label">${label}:</div>
            <div class="info-value">${value}</div>
          `;
          body.appendChild(row);
        });
        
        container.appendChild(card);
      }
    }
  },

  // ─────────────────────── ANDROID DRIVERS ───────────────────────
  'android-drivers': {
    title: '📱 Drivers Android por Marca',
    subtitle: 'Instala los drivers USB para depuración y gestión de dispositivos',
    render: (container) => {
      const brands = {
        'Samsung': [
          ['Samsung USB Driver', 'winget install Samsung.USB.Driver'],
          ['Samsung Smart Switch', 'winget install Samsung.SmartSwitch'],
          ['Samsung Kies', 'winget install Samsung.Kies3']
        ],
        'Xiaomi / Redmi': [
          ['Xiaomi USB Driver', 'winget install Xiaomi.USBDriver'],
          ['Mi Flash Tool', 'winget install Xiaomi.MiFlash'],
          ['MIUI ADB Drivers', 'pnputil /add-driver "%SYSTEMROOT%\\INF\\wpdmtp.inf" /install']
        ],
        'Huawei / Honor': [
          ['HiSuite (Huawei)', 'winget install Huawei.HiSuite'],
          ['Huawei USB Driver', 'pnputil /scan-devices'],
          ['HiLink Driver', 'devmgmt.msc']
        ],
        'Motorola': [
          ['Motorola Device Manager', 'winget install Motorola.DeviceManager'],
          ['Moto USB Driver', 'pnputil /add-driver "%SYSTEMROOT%\\INF\\wpdmtp.inf" /install']
        ],
        'LG': [
          ['LG USB Driver', 'winget install LG.Mobile.Support.Tool'],
          ['LG Bridge', 'winget install LG.Bridge']
        ],
        'OnePlus': [
          ['OnePlus USB Driver', 'winget install OnePlus.USBDriver'],
          ['MTP Driver', 'pnputil /scan-devices']
        ],
        'Google Pixel': [
          ['Google USB Driver', 'winget install Google.AndroidStudio'],
          ['ADB Interface Driver', 'winget install Google.PlatformTools']
        ],
        'OPPO / Realme': [
          ['OPPO USB Driver', 'winget install OPPO.USBDriver'],
          ['Realme Driver', 'pnputil /scan-devices']
        ],
        'Vivo': [
          ['Vivo USB Driver', 'winget install Vivo.PCManager']
        ],
        'Sony': [
          ['Sony Xperia Companion', 'winget install Sony.XperiaCompanion'],
          ['PC Companion', 'winget install Sony.PCCompanion']
        ]
      };
      
      Object.entries(brands).forEach(([brand, commands]) => {
        const { card, body } = createCard(brand, '📱');
        const buttons = commands.map(([label, cmd]) => 
          createButton(label, () => executeCommand(cmd), 'btn-purple')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── WINDOWS CONTROLLERS ───────────────────────
  'win-controllers': {
    title: '🖥️ Controladores de Windows',
    subtitle: 'Gestiona y actualiza controladores del sistema',
    render: (container) => {
      const categories = {
        'Audio (Realtek)': [
          ['Instalar Realtek HD Audio', 'winget install RealtekSemiconductor.RealtekAudioDriver', false],
          ['Actualizar Audio (Windows)', 'Get-PnpDevice -Class Media | Update-PnpDeviceDriver', true],
          ['Abrir Administrador Devices', 'devmgmt.msc', false]
        ],
        'WiFi & Bluetooth': [
          ['Buscar driver WiFi', 'Get-NetAdapter | Where-Object {$_.InterfaceDescription -like \'*Wireless*\'}', true],
          ['Actualizar driver WiFi', 'Get-PnpDevice -Class Net | Update-PnpDeviceDriver', true],
          ['Estado Bluetooth', 'Get-PnpDevice -Class Bluetooth', true]
        ],
        'Display / GPU': [
          ['Información GPU', 'Get-PnpDevice -Class Display', true],
          ['Instalar NVIDIA', 'winget install Nvidia.GeForceExperience', false],
          ['Instalar AMD drivers', 'winget install AMD.AdrenalinEdition', false],
          ['Instalar Intel Arc', 'winget install Intel.ArcControl', false]
        ],
        'USB & Almacenamiento': [
          ['Ver dispositivos USB', 'Get-PnpDevice -Class USB', true],
          ['Actualizar drivers USB', 'Get-PnpDevice -Class USB | Update-PnpDeviceDriver', true],
          ['Estado discos', 'Get-Disk', true]
        ]
      };
      
      Object.entries(categories).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🖥️');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── OPTIMIZATION ───────────────────────
  'optimization': {
    title: '⚡ Optimización Windows 11',
    subtitle: 'Mejora el rendimiento, limpia y repara el sistema',
    render: (container) => {
      const opts = {
        'Modo de Rendimiento': [
          ['Alto Rendimiento', 'powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', false],
          ['Máximo Rendimiento', 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61', false],
          ['Equilibrado (default)', 'powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e', false]
        ],
        'Limpieza del Sistema': [
          ['Limpiar archivos temp', 'Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue', true],
          ['Limpiar Prefetch', 'Remove-Item -Path C:\\Windows\\Prefetch\\* -Recurse -Force -ErrorAction SilentlyContinue', true],
          ['Disk Cleanup', 'cleanmgr /sagerun:1', false],
          ['Vaciar papelera', 'Clear-RecycleBin -Force -ErrorAction SilentlyContinue', true]
        ],
        'Reparación del Sistema': [
          ['SFC /scannow', 'sfc /scannow', false],
          ['DISM RestoreHealth', 'DISM /Online /Cleanup-Image /RestoreHealth', false],
          ['CHKDSK C:', 'echo Y | chkdsk C: /f /r /x', false]
        ]
      };
      
      Object.entries(opts).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '⚡');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── CMD TOOLS ───────────────────────
  'cmd-tools': {
    title: '💻 Comandos CMD Avanzados',
    subtitle: 'Diagnóstico del sistema, red, y comandos ocultos de Windows',
    render: (container) => {
      const cmds = {
        'Diagnóstico Sistema': [
          ['Información sistema', 'msinfo32', false],
          ['Procesos en ejecución', 'tasklist /v', false],
          ['Variables de entorno', 'set', false]
        ],
        'Diagnóstico Red': [
          ['ipconfig /all', 'ipconfig /all', false],
          ['Ping Google', 'ping -n 4 8.8.8.8', false],
          ['Traceroute Google', 'tracert -d 8.8.8.8', false],
          ['Puertos en uso', 'netstat -ano', false],
          ['DNS flush', 'ipconfig /flushdns', false]
        ],
        'Comandos Ocultos': [
          ['Calibrador pantalla', 'dccw', false],
          ['Editor de directivas', 'gpedit.msc', false],
          ['DirectX Diagnostic', 'dxdiag', false],
          ['Configurar arranque', 'msconfig', false]
        ]
      };
      
      Object.entries(cmds).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '💻');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── ADB & FASTBOOT ───────────────────────
  'adb-fastboot': {
    title: '🔧 ADB & Fastboot Setup',
    subtitle: 'Instala y usa herramientas de depuración Android',
    render: (container) => {
      const sections = {
        'Instalación & Configuración': [
          ['Instalar Platform Tools', 'winget install Google.PlatformTools', false],
          ['Verificar ADB instalado', 'adb version', false],
          ['Verificar Fastboot', 'fastboot --version', false]
        ],
        'Gestión de Dispositivos': [
          ['Listar dispositivos ADB', 'adb devices', false],
          ['Reboot to recovery', 'adb reboot recovery', false],
          ['Reboot to bootloader', 'adb reboot bootloader', false],
          ['ADB Shell', 'start cmd /k adb shell', false]
        ],
        'Comandos Fastboot': [
          ['Fastboot devices', 'fastboot devices', false],
          ['Desbloquear bootloader', 'fastboot oem unlock', false],
          ['Bloquear bootloader', 'fastboot oem lock', false],
          ['Reiniciar desde fastboot', 'fastboot reboot', false]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🔧');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-purple')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── USB DEBUG ───────────────────────
  'usb-debug': {
    title: '🔓 USB Debugging & FRP/MDM',
    subtitle: 'Métodos de depuración USB y bypass de bloqueos para uso educativo/recuperación',
    render: (container) => {
      const warning = document.createElement('div');
      warning.className = 'warning-box';
      warning.innerHTML = '<strong>⚠️ AVISO:</strong> Estas herramientas son para uso educativo y recuperación de dispositivos propios únicamente.';
      container.appendChild(warning);
      
      const sections = {
        'USB Debugging': [
          ['Habilitar USB Debugging', 'adb shell settings put global adb_enabled 1', false],
          ['Verificar depuración USB', 'adb shell settings get global adb_enabled', false],
          ['Ver info del dispositivo', 'adb shell getprop ro.product.model', false]
        ],
        'FRP (Factory Reset Protection)': [
          ['Info FRP', 'adb shell content query --uri content://settings/secure --projection name:value', false],
          ['Factory Reset (ADB)', 'adb shell recovery --wipe_data', false]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🔓');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── USB DEVICES ───────────────────────
  'usb-devices': {
    title: '📡 Dispositivos Conectados',
    subtitle: 'Detecta y gestiona dispositivos conectados por USB',
    render: (container) => {
      const { card, body } = createCard('Escaneo y Gestión USB', '📡');
      const commands = [
        ['Escanear dispositivos USB', 'Get-PnpDevice -Class USB | Select-Object Status, Class, FriendlyName', true],
        ['Ver discos externos', 'Get-Disk | Where-Object {$_.BusType -eq \'USB\'} | Select-Object FriendlyName, Size', true],
        ['Dispositivos ADB conectados', 'adb devices', false],
        ['Escanear nuevos HW', 'pnputil /scan-devices', false]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
      );
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── DISK TOOLS ───────────────────────
  'disk-tools': {
    title: '💾 Herramientas de Disco',
    subtitle: 'Gestión de disco, cifrado, carpetas protegidas y más',
    render: (container) => {
      const sections = {
        'Información de Disco': [
          ['Ver discos', 'Get-Disk | Select-Object Number, FriendlyName, Size, PartitionStyle', true],
          ['Particiones', 'Get-Partition | Select-Object DriveLetter, Size, Type', true],
          ['Espacio libre', 'Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free', true]
        ],
        'Gestión de Disco': [
          ['Abrir Administración de discos', 'diskmgmt.msc', false],
          ['CHKDSK C:', 'echo Y | chkdsk C: /f', false],
          ['Desfragmentar C:', 'defrag C: /U /V', false]
        ],
        'Cifrado BitLocker': [
          ['Estado BitLocker', 'Get-BitLockerVolume', true],
          ['Suspender BitLocker', 'Suspend-BitLocker -MountPoint \'C:\'', true]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '💾');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── SYSTEM ICONS ───────────────────────
  'system-icons': {
    title: '🖼️ Íconos del Sistema',
    subtitle: 'Personaliza y restaura íconos de escritorio y sistema',
    render: (container) => {
      const { card, body } = createCard('Gestión de Íconos', '🖼️');
      const commands = [
        ['Actualizar caché de íconos', 'ie4uinit.exe -ClearIconCache', false],
        ['Reconstruir caché íconos', 'taskkill /F /IM explorer.exe && del /F /Q %localappdata%\\IconCache.db && start explorer.exe', false],
        ['Abrir Config. íconos', 'start ms-settings:themes', false]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
      );
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── ANTI-SPYWARE ───────────────────────
  'anti-spyware': {
    title: '🛡️ Anti-Spyware & Privacidad',
    subtitle: 'Scripts para mejorar privacidad y eliminar telemetría de Windows',
    render: (container) => {
      const sections = {
        'Privacidad & Telemetría': [
          ['Deshabilitar telemetría', 'Set-ItemProperty -Path \'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\' -Name \'AllowTelemetry\' -Value 0 -Force', true],
          ['Deshabilitar DiagTrack', 'Stop-Service DiagTrack; Set-Service DiagTrack -StartupType Disabled', true],
          ['Deshabilitar Cortana', 'Set-ItemProperty -Path \'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search\' -Name \'AllowCortana\' -Value 0', true]
        ],
        'Windows Defender': [
          ['Estado Windows Defender', 'Get-MpComputerStatus | Select-Object AMRunningMode, AntispywareEnabled', true],
          ['Análisis rápido', 'Start-MpScan -ScanType QuickScan', true],
          ['Actualizar definiciones', 'Update-MpSignature', true]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🛡️');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-purple')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── USB REPAIR ───────────────────────
  'usb-repair': {
    title: '🔌 Reparar USB',
    subtitle: 'Soluciona problemas de dispositivos USB no detectados',
    render: (container) => {
      const { card, body } = createCard('Herramientas de Reparación USB', '🔌');
      const commands = [
        ['Reiniciar servicio USB', 'Stop-Service UsbStor; Start-Service UsbStor', true],
        ['Escanear cambios de HW', 'pnputil /scan-devices', false],
        ['Restablecer USB', 'devmgmt.msc', false],
        ['Habilitar todos los USB', 'Get-PnpDevice -Class USB | Enable-PnpDevice -Confirm:$false', true]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-warning')
      );
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── SECURITY ───────────────────────
  'security': {
    title: '🔒 Seguridad Windows',
    subtitle: 'Firewall, Windows Defender, usuarios y políticas de seguridad',
    render: (container) => {
      const sections = {
        'Firewall': [
          ['Estado del Firewall', 'Get-NetFirewallProfile | Select-Object Name, Enabled', true],
          ['Activar Firewall', 'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True', true],
          ['Ver reglas de entrada', 'Get-NetFirewallRule -Direction Inbound | Select-Object DisplayName, Enabled', true]
        ],
        'Usuarios y Grupos': [
          ['Listar usuarios locales', 'Get-LocalUser | Select-Object Name, Enabled, LastLogon', true],
          ['Ver grupos locales', 'Get-LocalGroup', true]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🔒');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-danger')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── NETWORK ───────────────────────
  'network': {
    title: '🌐 Red & WiFi',
    subtitle: 'Diagnóstico, configuración y gestión de red',
    render: (container) => {
      const sections = {
        'Diagnóstico': [
          ['IP Config completo', 'ipconfig /all', false],
          ['Ping Google', 'ping -n 4 google.com', false],
          ['Tracert Google', 'tracert -d google.com', false],
          ['Puertos abiertos', 'netstat -ano', false]
        ],
        'WiFi': [
          ['Ver redes WiFi', 'netsh wlan show networks mode=bssid', false],
          ['Perfil WiFi actual', 'netsh wlan show interfaces', false],
          ['Mostrar perfiles guardados', 'netsh wlan show profiles', false]
        ],
        'Reparación de Red': [
          ['Flush DNS', 'ipconfig /flushdns', false],
          ['Release & Renew IP', 'ipconfig /release && ipconfig /renew', false],
          ['Reset TCP/IP', 'netsh int ip reset', false],
          ['Reset Winsock', 'netsh winsock reset', false]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '🌐');
        const buttons = commands.map(([label, cmd, ps]) => 
          createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
        );
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  },

  // ─────────────────────── AUDIO ───────────────────────
  'audio': {
    title: '🔊 Herramientas de Audio',
    subtitle: 'Gestión y diagnóstico del sistema de sonido',
    render: (container) => {
      const { card, body } = createCard('Gestión de Audio', '🔊');
      const commands = [
        ['Ver dispositivos de audio', 'Get-PnpDevice -Class Media | Select-Object Status, FriendlyName', true],
        ['Reiniciar servicio de audio', 'Stop-Service Audiosrv; Start-Service Audiosrv', true],
        ['Abrir mezclador de volumen', 'sndvol', false],
        ['Abrir Config. de sonido', 'mmsys.cpl', false],
        ['Instalar Realtek Audio', 'winget install RealtekSemiconductor.RealtekAudioDriver', false]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
      );
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── PRINTERS ───────────────────────
  'printers': {
    title: '🖨️ Gestión de Impresoras',
    subtitle: 'Administra impresoras y colas de impresión',
    render: (container) => {
      const { card, body } = createCard('Gestión de Impresoras', '🖨️');
      const commands = [
        ['Ver impresoras instaladas', 'Get-Printer | Select-Object Name, DriverName, PortName', true],
        ['Reiniciar Spooler', 'Stop-Service Spooler; Start-Service Spooler', true],
        ['Abrir Config. impresoras', 'control printers', false],
        ['Ver drivers de impresora', 'Get-PrinterDriver | Select-Object Name, Manufacturer', true]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
      );
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── SYSINFO ───────────────────────
  'sysinfo': {
    title: 'ℹ️ Información del Sistema',
    subtitle: 'Información detallada de hardware y software',
    render: async (container) => {
      if (systemInfo) {
        const { card, body } = createCard('Información del Equipo', 'ℹ️');
        
        const info = [
          ['Sistema Operativo', `${systemInfo.osType} ${systemInfo.osRelease}`],
          ['Arquitectura', systemInfo.arch],
          ['Hostname', systemInfo.hostname],
          ['Usuario', systemInfo.userInfo.username],
          ['Home Directory', systemInfo.homeDir],
          ['CPUs', `${systemInfo.cpus.length} cores`],
          ['Modelo CPU', systemInfo.cpus[0]?.model || 'N/A'],
          ['RAM Total', `${(systemInfo.totalMemory / 1024 / 1024 / 1024).toFixed(2)} GB`],
          ['RAM Libre', `${(systemInfo.freeMemory / 1024 / 1024 / 1024).toFixed(2)} GB`],
          ['RAM Usada', `${((systemInfo.totalMemory - systemInfo.freeMemory) / 1024 / 1024 / 1024).toFixed(2)} GB`],
          ['Uptime', `${Math.floor(systemInfo.uptime / 3600)} horas ${Math.floor((systemInfo.uptime % 3600) / 60)} minutos`]
        ];
        
        info.forEach(([label, value]) => {
          const row = document.createElement('div');
          row.className = 'info-row';
          row.innerHTML = `
            <div class="info-label">${label}:</div>
            <div class="info-value">${value}</div>
          `;
          body.appendChild(row);
        });
        
        container.appendChild(card);
      }
      
      const { card: card2, body: body2 } = createCard('Consultas Detalladas de Hardware', 'ℹ️');
      const commands = [
        ['CPU detallado', 'Get-WMIObject Win32_Processor | Select-Object Name, MaxClockSpeed, NumberOfCores', true],
        ['RAM instalada', 'Get-WMIObject Win32_PhysicalMemory | Select-Object BankLabel, Capacity, Speed', true],
        ['Placa base', 'Get-WMIObject Win32_BaseBoard | Select-Object Manufacturer, Product', true],
        ['GPU', 'Get-WMIObject Win32_VideoController | Select-Object Name, AdapterRAM', true],
        ['Discos duros', 'Get-WMIObject Win32_DiskDrive | Select-Object Model, Size', true],
        ['Reporte completo', 'msinfo32', false]
      ];
      
      const buttons = commands.map(([label, cmd, ps]) => 
        createButton(label, () => executeCommand(cmd, ps), 'btn-primary')
      );
      body2.appendChild(createButtonGrid(buttons));
      container.appendChild(card2);
    }
  },

  // ─────────────────────── BOOTABLE USB ───────────────────────
  'bootable': {
    title: '💿 Crear USB Booteable',
    subtitle: 'Herramientas para crear USB de arranque con ISO',
    render: (container) => {
      const { card, body } = createCard('Herramientas de USB Booteable', '💿');
      
      const info = document.createElement('div');
      info.className = 'warning-box';
      info.innerHTML = '<strong>ℹ️ Información:</strong> Para crear USB booteables, se recomienda usar Rufus, una herramienta gratuita y confiable.';
      container.appendChild(info);
      
      const buttons = [
        createButton('🌐 Descargar Rufus', async () => {
          await window.aspv.openExternal('https://rufus.ie/');
          addTerminalLine('Abriendo página de descarga de Rufus...', 'success');
        }, 'btn-primary'),
        createButton('🚀 Lanzar Rufus', async () => {
          const result = await window.aspv.launchRufus();
          if (result.success) {
            addTerminalLine('Rufus lanzado correctamente', 'success');
          } else {
            addTerminalLine(`Error: ${result.error}`, 'error');
          }
        }, 'btn-success'),
        createButton('📀 Ver Unidades USB', () => executeCommand('Get-Disk | Where-Object {$_.BusType -eq \'USB\'}', true), 'btn-purple')
      ];
      
      body.appendChild(createButtonGrid(buttons));
      container.appendChild(card);
    }
  },

  // ─────────────────────── DEVELOPER TOOLS ───────────────────────
  'developer': {
    title: '👨‍💻 Herramientas de Desarrollo',
    subtitle: 'Instala y gestiona herramientas para desarrolladores',
    render: (container) => {
      const sections = {
        'Lenguajes de Programación': [
          ['Instalar Python', async () => {
            const result = await window.aspv.installPython();
            addTerminalLine(result.message || 'Abriendo página de descarga...', 'success');
          }],
          ['Instalar Node.js', async () => {
            const result = await window.aspv.installNodejs();
            addTerminalLine(result.message || 'Abriendo página de descarga...', 'success');
          }],
          ['Verificar Python', () => executeCommand('python --version', false)],
          ['Verificar Node.js', () => executeCommand('node --version', false)],
          ['Verificar npm', () => executeCommand('npm --version', false)]
        ],
        'Control de Versiones': [
          ['Instalar Git', async () => {
            const result = await window.aspv.installGit();
            addTerminalLine(result.message || 'Abriendo página de descarga...', 'success');
          }],
          ['Verificar Git', () => executeCommand('git --version', false)],
          ['Configurar Git User', () => executeCommand('git config --global user.name "Tu Nombre"', false)],
          ['Configurar Git Email', () => executeCommand('git config --global user.email "tu@email.com"', false)]
        ],
        'Editores de Código': [
          ['Instalar VS Code', async () => {
            const result = await window.aspv.installVscode();
            addTerminalLine(result.message || 'Abriendo página de descarga...', 'success');
          }],
          ['Verificar VS Code', () => executeCommand('code --version', false)]
        ],
        'Package Managers': [
          ['Instalar Chocolatey', () => executeCommand('Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))', true)],
          ['Verificar Chocolatey', () => executeCommand('choco --version', false)],
          ['Verificar winget', () => executeCommand('winget --version', false)]
        ]
      };
      
      Object.entries(sections).forEach(([category, commands]) => {
        const { card, body } = createCard(category, '👨‍💻');
        const buttons = commands.map(([label, action]) => {
          if (typeof action === 'function') {
            return createButton(label, action, 'btn-primary');
          } else {
            return createButton(label, () => executeCommand(action, false), 'btn-primary');
          }
        });
        body.appendChild(createButtonGrid(buttons));
        container.appendChild(card);
      });
    }
  }
};
