@echo off
REM ============================================================
REM  ASPV Tools - Windows EXE Build Script
REM  Compila aspv_tools.py en un unico ejecutable para Windows
REM  Requiere Python 3.8+ y pip instalado
REM ============================================================

echo [ASPV Tools] Instalando PyInstaller...
pip install pyinstaller --upgrade

echo.
echo [ASPV Tools] Compilando ejecutable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ASPVTools" ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.filedialog ^
    aspv_tools.py

echo.
echo [ASPV Tools] Build completado!
echo Ejecutable: dist\ASPVTools.exe
echo.
pause
