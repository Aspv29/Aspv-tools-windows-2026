# Guía de Instalación - ASPV Tools v2.0

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux](#instalación-en-linux)
4. [Compilación desde Código Fuente](#compilación-desde-código-fuente)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

### Windows 10/11

- **Sistema Operativo**: Windows 10 (64-bit) o Windows 11
- **RAM**: Mínimo 4 GB (recomendado 8 GB)
- **Espacio en Disco**: 500 MB libres
- **Privilegios**: Cuenta de administrador
- **Python** (opcional, solo para desarrollo): 3.8 o superior

### Linux (Modo Demostración)

- **Distribución**: Ubuntu 20.04+, Debian 11+, Fedora 35+, o similar
- **Python**: 3.8 o superior
- **Tkinter**: python3-tk
- **Dependencias**: binutils, gcc

---

## 💻 Instalación en Windows

### Método 1: Ejecutable Pre-compilado (Más Fácil)

1. **Descargar el ejecutable**
   ```
   Descarga ASPVTools.exe desde la carpeta dist/
   ```

2. **Ejecutar como Administrador**
   - Haz clic derecho en `ASPVTools.exe`
   - Selecciona "Ejecutar como administrador"
   - Si aparece el Control de Cuentas de Usuario (UAC), haz clic en "Sí"

3. **Primera Ejecución**
   - El programa solicitará privilegios de administrador
   - Acepta para acceder a todas las funciones
   - La interfaz gráfica se abrirá automáticamente

### Método 2: Desde Código Fuente

#### Paso 1: Instalar Python

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marca "Add Python to PATH"
3. Verifica la instalación:
   ```cmd
   python --version
   ```

#### Paso 2: Descargar el Proyecto

```cmd
# Opción A: Con Git
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# Opción B: Descarga manual
# Descarga el ZIP y extrae en una carpeta
cd ruta\a\aspv-tools
```

#### Paso 3: Instalar Dependencias

```cmd
pip install -r requirements.txt
```

#### Paso 4: Ejecutar

```cmd
# Ejecutar directamente
python aspv_tools.py

# O compilar a ejecutable
build_exe.bat
```

---

## 🐧 Instalación en Linux

**⚠️ Advertencia**: ASPV Tools está diseñado para Windows. En Linux funcionará en modo demostración con funcionalidad limitada.

### Ubuntu/Debian

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias
sudo apt install -y python3 python3-pip python3-tk binutils

# 3. Clonar repositorio
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# 4. Instalar dependencias Python
pip3 install -r requirements.txt

# 5. Ejecutar
python3 aspv_tools.py
```

### Fedora/RHEL/Amazon Linux

```bash
# 1. Actualizar sistema
sudo dnf update -y

# 2. Instalar dependencias
sudo dnf install -y python3 python3-pip python3-tkinter binutils

# 3. Clonar repositorio
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# 4. Instalar dependencias Python
pip3 install -r requirements.txt

# 5. Ejecutar
python3 aspv_tools.py
```

### Arch Linux

```bash
# 1. Instalar dependencias
sudo pacman -S python python-pip tk binutils

# 2. Clonar y ejecutar
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools
pip3 install -r requirements.txt
python3 aspv_tools.py
```

---

## 🔨 Compilación desde Código Fuente

### Windows

#### Usando PowerShell (Recomendado)

```powershell
# 1. Abrir PowerShell como Administrador
# 2. Navegar al directorio del proyecto
cd C:\ruta\a\aspv-tools

# 3. Ejecutar script de compilación
.\build_exe.ps1

# El ejecutable estará en: dist\ASPVTools.exe
```

#### Usando CMD

```cmd
# 1. Abrir CMD como Administrador
# 2. Navegar al directorio
cd C:\ruta\a\aspv-tools

# 3. Ejecutar script
build_exe.bat

# El ejecutable estará en: dist\ASPVTools.exe
```

#### Manual

```cmd
# 1. Instalar PyInstaller
pip install pyinstaller>=6.0.0

# 2. Limpiar builds anteriores (opcional)
rmdir /s /q build dist

# 3. Compilar
pyinstaller ASPVTools.spec --clean --noconfirm

# 4. El ejecutable estará en: dist\ASPVTools.exe
```

### Linux

```bash
# 1. Dar permisos al script
chmod +x build_exe.sh

# 2. Ejecutar compilación
./build_exe.sh

# 3. El ejecutable estará en: dist/ASPVTools
```

---

## ✅ Verificación de Instalación

### Verificar Ejecutable

#### Windows

```cmd
# Verificar que el archivo existe
dir dist\ASPVTools.exe

# Ver tamaño del archivo
dir dist\ASPVTools.exe | findstr ASPVTools

# Ejecutar
dist\ASPVTools.exe
```

#### Linux

```bash
# Verificar que el archivo existe
ls -lh dist/ASPVTools

# Ejecutar
./dist/ASPVTools
```

### Verificar Instalación de Python

```bash
# Versión de Python
python --version  # Windows
python3 --version # Linux

# Verificar pip
pip --version     # Windows
pip3 --version    # Linux

# Verificar PyInstaller
pyinstaller --version
```

### Verificar Dependencias

```bash
# Listar paquetes instalados
pip list | findstr pyinstaller  # Windows
pip3 list | grep pyinstaller    # Linux
```

---

## 🔧 Solución de Problemas

### Problema: "Python no se reconoce como comando"

**Solución Windows**:
```cmd
# Agregar Python al PATH manualmente
setx PATH "%PATH%;C:\Python39;C:\Python39\Scripts"
```

**Solución Linux**:
```bash
# Instalar Python
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora/RHEL
```

### Problema: "No se puede ejecutar como administrador"

**Solución**:
1. Haz clic derecho en el ejecutable
2. Propiedades → Compatibilidad
3. Marca "Ejecutar este programa como administrador"
4. Aplicar → Aceptar

### Problema: "tkinter no está instalado"

**Solución Windows**:
- Reinstala Python marcando "tcl/tk and IDLE"

**Solución Linux**:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Problema: "PyInstaller falla al compilar"

**Solución**:
```bash
# 1. Actualizar PyInstaller
pip install --upgrade pyinstaller

# 2. Limpiar caché
pip cache purge

# 3. Reinstalar
pip uninstall pyinstaller
pip install pyinstaller>=6.0.0

# 4. Limpiar builds anteriores
rm -rf build dist __pycache__  # Linux
rmdir /s /q build dist         # Windows

# 5. Compilar de nuevo
pyinstaller ASPVTools.spec --clean --noconfirm
```

### Problema: "El ejecutable no inicia"

**Diagnóstico**:
```bash
# Ejecutar desde terminal para ver errores
./dist/ASPVTools  # Linux
dist\ASPVTools.exe  # Windows
```

**Soluciones comunes**:
1. Verifica que tienes privilegios de administrador
2. Desactiva temporalmente el antivirus
3. Ejecuta desde la terminal para ver errores
4. Verifica que todas las dependencias estén instaladas

### Problema: "Comandos no funcionan en Linux"

**Explicación**:
- ASPV Tools está diseñado para Windows
- Los comandos de PowerShell y CMD no existen en Linux
- La interfaz funcionará pero los comandos no se ejecutarán

**Solución**:
- Usa el programa en Windows para funcionalidad completa
- O adapta los comandos para Linux (requiere modificar el código)

### Problema: "Error de permisos en Linux"

**Solución**:
```bash
# Dar permisos de ejecución
chmod +x dist/ASPVTools
chmod +x build_exe.sh

# Ejecutar con sudo si es necesario
sudo ./dist/ASPVTools
```

### Problema: "Falta binutils en Linux"

**Solución**:
```bash
# Ubuntu/Debian
sudo apt install binutils

# Fedora/RHEL/Amazon Linux
sudo dnf install binutils

# Arch
sudo pacman -S binutils
```

---

## 📞 Soporte Adicional

Si los problemas persisten:

1. **Revisa los logs**: Busca archivos `.log` en la carpeta del programa
2. **Consulta la documentación**: Lee `README.md` para más detalles
3. **Reporta el problema**: Abre un issue en GitHub con:
   - Sistema operativo y versión
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir el problema

---

## 🎯 Próximos Pasos

Una vez instalado correctamente:

1. Lee el `README.md` para conocer todas las funciones
2. Explora las diferentes secciones del programa
3. Ejecuta comandos de diagnóstico primero
4. Haz copias de seguridad antes de modificaciones importantes
5. Usa con precaución los comandos de optimización

---

**¡Disfruta de ASPV Tools!** 🚀

© 2026 ASPV Tools Team
