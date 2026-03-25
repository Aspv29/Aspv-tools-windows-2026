# Guía de Contribución - ASPV Tools

¡Gracias por tu interés en contribuir a ASPV Tools! 🎉

Esta guía te ayudará a entender cómo puedes contribuir al proyecto de manera efectiva.

---

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Proceso de Desarrollo](#proceso-de-desarrollo)
5. [Estándares de Código](#estándares-de-código)
6. [Proceso de Pull Request](#proceso-de-pull-request)
7. [Reportar Bugs](#reportar-bugs)
8. [Sugerir Mejoras](#sugerir-mejoras)

---

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de la participación en este proyecto una experiencia libre de acoso para todos, independientemente de:

- Edad
- Tamaño corporal
- Discapacidad
- Etnia
- Identidad y expresión de género
- Nivel de experiencia
- Nacionalidad
- Apariencia personal
- Raza
- Religión
- Identidad y orientación sexual

### Comportamiento Esperado

- Usar lenguaje acogedor e inclusivo
- Respetar diferentes puntos de vista y experiencias
- Aceptar críticas constructivas con gracia
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros

### Comportamiento Inaceptable

- Uso de lenguaje o imágenes sexualizadas
- Trolling, comentarios insultantes o despectivos
- Acoso público o privado
- Publicar información privada de otros sin permiso
- Conducta que razonablemente se considere inapropiada

---

## 🤝 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Los bugs se rastrean como [GitHub Issues](https://github.com/tu-usuario/aspv-tools/issues). Antes de crear un reporte:

1. **Verifica** que el bug no haya sido reportado ya
2. **Determina** en qué sección del código está el problema
3. **Recopila** información sobre el bug

**Crea un reporte detallado** incluyendo:

- **Título claro y descriptivo**
- **Pasos exactos para reproducir** el problema
- **Comportamiento esperado** vs **comportamiento actual**
- **Capturas de pantalla** si es aplicable
- **Información del sistema**:
  - Versión de ASPV Tools
  - Sistema operativo y versión
  - Versión de Python (si aplica)
- **Logs o mensajes de error** completos

### Sugerir Mejoras

Las sugerencias también se rastrean como GitHub Issues. Para sugerir una mejora:

1. **Usa un título claro y descriptivo**
2. **Describe el comportamiento actual** y **el comportamiento deseado**
3. **Explica por qué** esta mejora sería útil
4. **Proporciona ejemplos** de cómo funcionaría
5. **Lista alternativas** que hayas considerado

### Contribuir con Código

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcion`)
3. **Desarrolla** tu feature siguiendo los estándares de código
4. **Prueba** exhaustivamente tus cambios
5. **Commit** tus cambios (`git commit -am 'Agrega nueva función'`)
6. **Push** a la rama (`git push origin feature/nueva-funcion`)
7. **Abre** un Pull Request

### Mejorar Documentación

La documentación siempre puede mejorar:

- Corregir errores tipográficos o gramaticales
- Agregar ejemplos de uso
- Mejorar explicaciones existentes
- Traducir a otros idiomas
- Crear tutoriales o guías

---

## 🛠️ Configuración del Entorno

### Requisitos

- Python 3.8 o superior
- Git
- Editor de código (recomendado: VS Code, PyCharm)

### Instalación

```bash
# 1. Fork y clonar el repositorio
git clone https://github.com/tu-usuario/aspv-tools.git
cd aspv-tools

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar dependencias de desarrollo (opcional)
pip install pylint black flake8 pytest

# 5. Ejecutar el programa
python aspv_tools.py
```

### Estructura del Proyecto

```
aspv-tools/
├── aspv_tools.py          # Código principal
├── ASPVTools.spec         # Config PyInstaller
├── requirements.txt       # Dependencias
├── build_exe.bat          # Build Windows (CMD)
├── build_exe.ps1          # Build Windows (PowerShell)
├── build_exe.sh           # Build Linux
├── README.md              # Documentación principal
├── INSTALL.md             # Guía de instalación
├── CHANGELOG.md           # Historial de cambios
├── CONTRIBUTING.md        # Esta guía
├── LICENSE                # Licencia MIT
├── .gitignore             # Archivos ignorados
└── .blackbox/             # Configuración del proyecto
```

---

## 💻 Proceso de Desarrollo

### Flujo de Trabajo Git

1. **Mantén tu fork actualizado**
   ```bash
   git remote add upstream https://github.com/original/aspv-tools.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Crea una rama para cada feature**
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

3. **Haz commits pequeños y frecuentes**
   ```bash
   git add .
   git commit -m "Descripción clara del cambio"
   ```

4. **Escribe mensajes de commit descriptivos**
   - Usa presente imperativo ("Agrega" no "Agregado")
   - Primera línea: resumen breve (50 caracteres max)
   - Línea en blanco
   - Descripción detallada si es necesario

### Tipos de Ramas

- `main`: Código estable de producción
- `develop`: Desarrollo activo
- `feature/`: Nuevas funcionalidades
- `bugfix/`: Corrección de bugs
- `hotfix/`: Correcciones urgentes
- `docs/`: Mejoras de documentación

### Pruebas

Antes de enviar un PR, asegúrate de:

1. **Probar manualmente** todas las funciones afectadas
2. **Ejecutar en diferentes escenarios**:
   - Con y sin privilegios de administrador
   - En diferentes versiones de Windows (si es posible)
   - Con diferentes configuraciones del sistema

3. **Verificar que no hay errores** en la consola
4. **Compilar el ejecutable** y probarlo

---

## 📝 Estándares de Código

### Estilo Python (PEP 8)

```python
# Importaciones
import os
import sys
from tkinter import ttk

# Constantes en MAYÚSCULAS
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Clases en PascalCase
class CommandRunner:
    def __init__(self):
        pass

# Funciones y variables en snake_case
def execute_command(cmd_string):
    result = None
    return result

# Docstrings para funciones y clases
def my_function(param1, param2):
    """
    Descripción breve de la función.
    
    Args:
        param1 (str): Descripción del parámetro 1
        param2 (int): Descripción del parámetro 2
    
    Returns:
        bool: Descripción del valor de retorno
    """
    pass
```

### Convenciones del Proyecto

1. **Idioma**: Código y comentarios en español
2. **Indentación**: 4 espacios (no tabs)
3. **Longitud de línea**: Máximo 100 caracteres
4. **Encoding**: UTF-8 con BOM para compatibilidad Windows
5. **Nombres descriptivos**: Prefiere claridad sobre brevedad

### Comentarios

```python
# Comentarios de una línea para explicaciones breves

"""
Comentarios de múltiples líneas para:
- Explicaciones complejas
- Documentación de funciones
- Notas importantes
"""

# TODO: Tareas pendientes
# FIXME: Código que necesita corrección
# NOTE: Notas importantes
# HACK: Soluciones temporales
```

### Manejo de Errores

```python
try:
    # Código que puede fallar
    result = risky_operation()
except SpecificException as e:
    # Manejo específico
    logger.error(f"Error específico: {e}")
except Exception as e:
    # Manejo genérico
    logger.error(f"Error inesperado: {e}")
finally:
    # Limpieza
    cleanup()
```

---

## 🔄 Proceso de Pull Request

### Antes de Enviar

- [ ] El código sigue los estándares del proyecto
- [ ] Has probado los cambios exhaustivamente
- [ ] Has actualizado la documentación si es necesario
- [ ] Has agregado comentarios donde sea necesario
- [ ] El código compila sin errores ni warnings
- [ ] Has actualizado CHANGELOG.md

### Crear el Pull Request

1. **Título descriptivo**: `[Feature] Agrega soporte para X`
2. **Descripción detallada**:
   ```markdown
   ## Descripción
   Breve descripción de los cambios
   
   ## Tipo de cambio
   - [ ] Bug fix
   - [ ] Nueva feature
   - [ ] Breaking change
   - [ ] Documentación
   
   ## ¿Cómo se ha probado?
   Describe las pruebas realizadas
   
   ## Checklist
   - [ ] Mi código sigue los estándares del proyecto
   - [ ] He realizado una auto-revisión
   - [ ] He comentado código complejo
   - [ ] He actualizado la documentación
   - [ ] Mis cambios no generan nuevos warnings
   - [ ] He probado en Windows 10/11
   ```

3. **Asigna reviewers** si es posible
4. **Etiqueta apropiadamente**: bug, enhancement, documentation, etc.

### Proceso de Revisión

1. **Espera feedback** de los mantenedores
2. **Responde a comentarios** de manera constructiva
3. **Realiza cambios** solicitados
4. **Actualiza el PR** con nuevos commits
5. **Espera aprobación** final

### Después de la Aprobación

- Tu PR será merged por un mantenedor
- La rama será eliminada automáticamente
- Tus cambios aparecerán en la próxima release

---

## 🐛 Reportar Bugs

### Template de Reporte de Bug

```markdown
**Descripción del Bug**
Descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ve a '...'
2. Haz clic en '...'
3. Ejecuta '...'
4. Ver error

**Comportamiento Esperado**
Descripción de lo que esperabas que sucediera.

**Comportamiento Actual**
Descripción de lo que realmente sucedió.

**Capturas de Pantalla**
Si es aplicable, agrega capturas de pantalla.

**Información del Sistema**
- OS: [ej. Windows 11 Pro 23H2]
- Versión ASPV Tools: [ej. 2.0.0]
- Python: [ej. 3.9.7]

**Logs/Errores**
```
Pega aquí los logs o mensajes de error
```

**Contexto Adicional**
Cualquier otra información relevante.
```

---

## 💡 Sugerir Mejoras

### Template de Sugerencia

```markdown
**¿Tu sugerencia está relacionada con un problema?**
Descripción clara del problema. Ej: "Siempre me frustra cuando..."

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que suceda.

**Describe alternativas que has considerado**
Descripción de soluciones o features alternativas.

**Contexto Adicional**
Cualquier otra información, capturas, mockups, etc.

**¿Estarías dispuesto a implementarlo?**
- [ ] Sí, puedo trabajar en esto
- [ ] Necesitaría ayuda
- [ ] Solo estoy sugiriendo
```

---

## 🎯 Áreas de Contribución

### Prioridades Actuales

1. **Testing**: Pruebas en diferentes versiones de Windows
2. **Documentación**: Tutoriales y guías de uso
3. **Traducción**: Soporte multi-idioma
4. **Features**: Ver CHANGELOG.md para features planeadas
5. **Bug Fixes**: Ver Issues abiertos

### Habilidades Necesarias

- **Python**: Para desarrollo del core
- **Tkinter**: Para mejoras de UI
- **PowerShell/CMD**: Para nuevos comandos
- **Documentación**: Para mejorar guías
- **Testing**: Para QA y pruebas
- **Diseño**: Para mejorar UI/UX

---

## 📞 Contacto

- **GitHub Issues**: Para bugs y sugerencias
- **Email**: dev@aspvtools.com
- **Discord**: [Servidor de la comunidad](#)
- **Twitter**: [@aspvtools](#)

---

## 🙏 Reconocimientos

Todos los contribuidores serán reconocidos en:

- README.md (sección de contribuidores)
- CHANGELOG.md (en cada release)
- Página de About en la aplicación

---

## 📄 Licencia

Al contribuir a ASPV Tools, aceptas que tus contribuciones serán licenciadas bajo la Licencia MIT.

---

**¡Gracias por contribuir a ASPV Tools!** 🚀

Tu ayuda hace que este proyecto sea mejor para todos.

© 2026 ASPV Tools Team
