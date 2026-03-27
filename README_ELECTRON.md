# ASPV Tools Premium v3.0 - Electron Edition

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Electron](https://img.shields.io/badge/electron-28.0.0-green)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Descripción

**ASPV Tools Premium** es una suite completa de administración y optimización para Windows construida con Electron. Integra más de 200 herramientas y comandos en una interfaz gráfica moderna, elegante y fácil de usar.

### ✨ Características Principales

- 🎨 **Interfaz Moderna**: Diseño premium con tema oscuro y animaciones fluidas
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
- 💿 **USB Booteable**: Integración con Rufus para crear USB de arranque
- 👨‍💻 **Herramientas Dev**: Instalación de Python, Node.js, Git, VS Code y más

## 🎯 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10 (64-bit) o Windows 11
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Espacio en Disco**: 200 MB para la aplicación
- **Privilegios**: Administrador (requerido para la mayoría de funciones)

### Dependencias de Desarrollo
- Node.js 18+ (para desarrollo)
- npm o yarn
- Electron 28+

## 🚀 Instalación

### Opción 1: Ejecutable Pre-compilado (Recomendado)

1. Descarga el instalador desde la carpeta `dist/`
2. Ejecuta `ASPV-Tools-Premium-Setup-3.0.0.exe`
3. Sigue el asistente de instalación
4. Ejecuta la aplicación desde el menú de inicio o escritorio

### Opción 2: Ejecutable Portable

1. Descarga `ASPV-Tools-Premium-3.0.0-portable.exe`
2. Ejecuta directamente sin instalación
3. ¡Listo para usar!

### Opción 3: Desde el Código Fuente

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/aspv-tools-premium.git
cd aspv-tools-premium

# 2. Instalar dependencias
npm install

# 3. Ejecutar en modo desarrollo
npm start

# 4. Compilar para producción
npm run build
```

## 📦 Compilar la Aplicación

### Windows

```bash
# Compilar instalador NSIS
npm run dist

# Compilar versión portable
npm run pack

# Compilar sin empaquetar (para pruebas)
npm run build:dir
```

El ejecutable se generará en la carpeta `dist/`

## 🎮 Uso

### Inicio Rápido

1. **Ejecutar la Aplicación**: Doble clic en el ejecutable o acceso directo
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

#### 💿 USB Booteable
- Integración con Rufus
- Descarga directa de Rufus
- Gestión de unidades USB
- Creación de USB de arranque

#### 👨‍💻 Herramientas de Desarrollo
- Instalación de Python
- Instalación de Node.js
- Instalación de Git
- Instalación de VS Code
- Package managers (Chocolatey, winget)

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
2. Comprueba que tienes Windows 10/11 de 64 bits
3. Reinstala la aplicación

### Los comandos no funcionan

1. Asegúrate de tener privilegios de administrador
2. Verifica que PowerShell esté habilitado
3. Comprueba que los comandos existan en tu versión de Windows

### Error de compilación

1. Actualiza Node.js a la última versión LTS
2. Limpia node_modules: `rm -rf node_modules && npm install`
3. Limpia caché de Electron: `npm run clean`
4. Vuelve a compilar: `npm run build`

## 📝 Estructura del Proyecto

```
aspv-tools-premium/
├── src/
│   ├── main.js              # Proceso principal de Electron
│   ├── preload.js           # Script de precarga (bridge seguro)
│   ├── renderer.js          # Lógica de la interfaz
│   ├── index.html           # Estructura HTML
│   └── styles.css           # Estilos CSS
├── assets/
│   ├── icon.ico             # Icono de la aplicación
│   └── ...
├── tools/                   # Herramientas adicionales
├── installer/               # Configuración del instalador
├── dist/                    # Ejecutables compilados
├── package.json             # Configuración del proyecto
├── README.md                # Este archivo
└── LICENSE                  # Licencia MIT
```

## 🛠️ Desarrollo

### Requisitos de Desarrollo

```bash
npm install
```

### Ejecutar en Modo Desarrollo

```bash
npm start
# o
npm run dev
```

### Agregar Nuevas Funciones

1. Edita `src/renderer.js`
2. Agrega tu sección en el objeto `SECTIONS`
3. Registra la sección en el array `NAVIGATION`
4. Implementa la función `render()` para tu sección

### Estilo de Código

- Usa ES6+ JavaScript moderno
- Sigue las convenciones de Electron
- Documenta funciones con JSDoc
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

### Seguridad de Electron

- **Context Isolation**: Habilitado para seguridad
- **Node Integration**: Deshabilitado en renderer
- **Preload Script**: Bridge seguro entre procesos
- **CSP**: Content Security Policy implementado

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

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/aspv-tools-premium/issues)
- **Email**: soporte@aspvtools.com
- **Documentación**: [Wiki del Proyecto](https://github.com/tu-usuario/aspv-tools-premium/wiki)

## 🙏 Agradecimientos

- Comunidad de Electron
- Desarrolladores de Node.js
- Usuarios beta testers
- Contribuidores del proyecto

## 📊 Changelog

### v3.0.0 (2026-03-27)
- ✨ Migración completa a Electron
- 🎨 Interfaz gráfica completamente rediseñada
- 🖼️ Tema oscuro premium moderno
- 📱 19 secciones de herramientas
- 🔧 Más de 200 comandos integrados
- 🛡️ Mejoras en seguridad y privacidad
- 🚀 Optimización de rendimiento
- 📦 Instalador NSIS y versión portable
- 💿 Integración con Rufus para USB booteable
- 👨‍💻 Sección de herramientas de desarrollo
- 🐛 Corrección de bugs críticos
- 📝 Documentación completa actualizada

### v2.0.0 (2026-03-25)
- 🎉 Versión Python con tkinter
- 📱 17 secciones funcionales
- 🖥️ Interfaz gráfica básica

---

**ASPV Tools Premium** - Suite Premium de Administración Windows
© 2026 ASPV Tools Team. Todos los derechos reservados.
