# ASPV Tools - Windows Premium v2.0

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Descripción

**ASPV Tools** es una suite completa de administración y optimización para Windows que integra múltiples herramientas en una interfaz gráfica moderna y fácil de usar.

### ✨ Características Principales

- 📱 **Drivers Android**: Instalación automática de drivers USB para todas las marcas principales
- 🖥️ **Controladores Windows**: Gestión y actualización de drivers del sistema
- ⚡ **Optimización Win11**: Mejora el rendimiento y limpia el sistema
- 💻 **Comandos CMD**: Diagnóstico avanzado del sistema
- 🔧 **ADB & Fastboot**: Herramientas de depuración Android integradas
- 🔓 **USB Debugging**: Métodos de depuración y recuperación
- 💾 **Herramientas Disco**: Gestión de almacenamiento y cifrado BitLocker
- 🛡️ **Anti-Spyware**: Protección de privacidad y eliminación de telemetría
- 🌐 **Red & WiFi**: Diagnóstico y configuración de red
- 🔒 **Seguridad**: Firewall, usuarios y políticas de seguridad

## 🎯 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10 (64-bit) o Windows 11
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Espacio en Disco**: 500 MB libres
- **Python**: 3.8 o superior (solo para desarrollo)
- **Privilegios**: Administrador (requerido para la mayoría de funciones)

### Dependencias
- Python 3.8+
- tkinter (incluido con Python)
- PyInstaller 6.0+ (solo para compilar)

## 🚀 Instalación

### Opción 1: Ejecutable Pre-compilado (Recomendado)

1. Descarga el archivo `ASPVTools.exe` desde la carpeta `dist/`
2. Haz clic derecho → "Ejecutar como administrador"
3. ¡Listo! La aplicación se iniciará automáticamente

### Opción 2: Desde el Código Fuente

#### En Windows:

```batch
# 1. Clonar o descargar el repositorio
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar directamente
python aspv_tools.py

# O compilar a ejecutable
build_exe.bat
```

#### En Linux/Unix (Modo Demostración):

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# 2. Instalar dependencias
pip3 install -r requirements.txt

# 3. Ejecutar (modo demostración)
python3 aspv_tools.py

# O compilar
chmod +x build_exe.sh
./build_exe.sh
```

**⚠️ Nota**: En Linux, la aplicación se ejecutará en modo demostración. La mayoría de funciones requieren Windows.

## 📦 Compilar Ejecutable

### Windows (PowerShell):

```powershell
# Método 1: Script PowerShell
.\build_exe.ps1

# Método 2: Script Batch
.\build_exe.bat

# Método 3: Manual
pip install pyinstaller
pyinstaller ASPVTools.spec --clean --noconfirm
```

### Linux/Unix:

```bash
# Dar permisos de ejecución
chmod +x build_exe.sh

# Ejecutar script de compilación
./build_exe.sh
```

El ejecutable se generará en la carpeta `dist/ASPVTools` o `dist/ASPVTools.exe`

## 🎮 Uso

### Inicio Rápido

1. **Ejecutar como Administrador**: Haz clic derecho en `ASPVTools.exe` → "Ejecutar como administrador"
2. **Navegar**: Usa el menú lateral para acceder a las diferentes secciones
3. **Ejecutar Comandos**: Haz clic en cualquier botón para ejecutar la acción correspondiente
4. **Ver Resultados**: Los resultados se mostrarán en el terminal de salida en la parte inferior

### Secciones Principales

#### 📱 Drivers Android
Instala drivers USB para:
- Samsung (Smart Switch, Kies, USB Driver)
- Xiaomi/Redmi (Mi Flash Tool, USB Driver)
- Huawei/Honor (HiSuite)
- Motorola, LG, OnePlus, Google Pixel
- OPPO, Realme, Vivo, Sony

#### 🖥️ Controladores Windows
- Drivers de audio (Realtek)
- WiFi y Bluetooth
- GPU (NVIDIA, AMD, Intel Arc)
- USB y almacenamiento
- Seguridad (TPM, Secure Boot)

#### ⚡ Optimización
- Modos de rendimiento (Alto, Máximo, Equilibrado)
- Limpieza del sistema (temp, prefetch, papelera)
- Optimización gaming (Game Mode, prioridad CPU)
- Reparación del sistema (SFC, DISM, CHKDSK)

#### 🔧 ADB & Fastboot
- Instalación de Platform Tools
- Gestión de dispositivos Android
- Comandos Fastboot (unlock, flash, erase)
- Sideload de ROMs y APKs

#### 🛡️ Seguridad
- Configuración de Firewall
- Gestión de usuarios y grupos
- Políticas de seguridad
- Windows Defender

## ⚙️ Configuración

### Variables de Entorno

El programa utiliza las siguientes variables de entorno:

- `PATH`: Para acceder a comandos del sistema
- `TEMP`: Para archivos temporales
- `SYSTEMROOT`: Para acceder a archivos del sistema Windows

### Permisos de Administrador

**Importante**: La mayoría de funciones requieren privilegios de administrador:

- Instalación de drivers
- Modificación de servicios del sistema
- Cambios en el registro de Windows
- Gestión de firewall y seguridad
- Optimización del sistema

## 🔧 Solución de Problemas

### El programa no inicia

1. Verifica que estés ejecutando como administrador
2. Comprueba que tienes Python 3.8+ instalado
3. Reinstala las dependencias: `pip install -r requirements.txt`

### Los comandos no funcionan

1. Asegúrate de tener privilegios de administrador
2. Verifica que PowerShell esté habilitado
3. Comprueba que los comandos existan en tu versión de Windows

### Error de compilación

1. Actualiza PyInstaller: `pip install --upgrade pyinstaller`
2. Limpia archivos anteriores: `rmdir /s /q build dist`
3. Vuelve a compilar: `pyinstaller ASPVTools.spec --clean`

### Funciones no disponibles en Linux

El programa está diseñado específicamente para Windows. En Linux:
- La interfaz gráfica funcionará
- Los comandos de Windows no se ejecutarán
- Se mostrará un aviso al iniciar

## 📝 Estructura del Proyecto

```
aspv-tools/
├── aspv_tools.py          # Código fuente principal
├── ASPVTools.spec         # Configuración PyInstaller
├── requirements.txt       # Dependencias Python
├── build_exe.bat          # Script de compilación (Windows CMD)
├── build_exe.ps1          # Script de compilación (PowerShell)
├── build_exe.sh           # Script de compilación (Linux/Unix)
├── README.md              # Este archivo
├── .blackbox/             # Configuración del proyecto
│   └── project-context.md
├── dist/                  # Ejecutables compilados (generado)
│   └── ASPVTools.exe
└── build/                 # Archivos temporales (generado)
```

## 🛠️ Desarrollo

### Requisitos de Desarrollo

```bash
pip install -r requirements.txt
```

### Ejecutar en Modo Desarrollo

```bash
python aspv_tools.py
```

### Agregar Nuevas Funciones

1. Edita `aspv_tools.py`
2. Agrega tu sección en el método correspondiente (ej: `_section_nueva_funcion`)
3. Registra la sección en el diccionario `sections` del método `show_section`
4. Agrega el botón de navegación en `_build_sidebar`

### Estilo de Código

- Usa 4 espacios para indentación
- Sigue PEP 8
- Documenta funciones con docstrings
- Usa nombres descriptivos en español para UI

## 🔐 Seguridad y Privacidad

### Advertencias Importantes

⚠️ **Este programa ejecuta comandos del sistema con privilegios elevados**:

- Revisa el código antes de ejecutar
- No ejecutes comandos que no entiendas
- Haz copias de seguridad antes de modificaciones importantes
- Usa bajo tu propia responsabilidad

### Funciones de Privacidad

El programa incluye herramientas para:
- Deshabilitar telemetría de Windows
- Bloquear servidores de rastreo
- Limpiar historial y logs
- Proteger datos con BitLocker

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Contribuciones

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -am 'Agrega nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/aspv-tools/issues)
- **Email**: soporte@aspvtools.com
- **Documentación**: [Wiki del Proyecto](https://github.com/tu-usuario/aspv-tools/wiki)

## 🙏 Agradecimientos

- Comunidad de Python
- Desarrolladores de PyInstaller
- Usuarios beta testers
- Contribuidores del proyecto

## 📊 Changelog

### v2.0.0 (2026-03-25)
- ✨ Interfaz gráfica completamente rediseñada
- 🎨 Tema oscuro moderno
- 📱 17 secciones de herramientas
- 🔧 Más de 200 comandos integrados
- 🛡️ Mejoras en seguridad y privacidad
- 🚀 Optimización de rendimiento
- 📦 Compilación a ejecutable único
- 🌐 Soporte multi-idioma (preparado)
- 🐛 Corrección de bugs críticos
- 📝 Documentación completa

### v1.0.0 (2025-12-01)
- 🎉 Lanzamiento inicial
- 📱 Drivers Android básicos
- 🖥️ Comandos CMD esenciales
- ⚡ Optimización básica

---

**ASPV Tools** - Suite Premium de Administración Windows
© 2026 ASPV Tools Team. Todos los derechos reservados.
