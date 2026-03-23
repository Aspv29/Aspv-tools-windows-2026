@echo off
REM ============================================================
REM  ASPV Tools - Windows EXE Build Script
REM  Compila aspv_tools.py en un único ejecutable para Windows
REM ============================================================

echo [ASPV Tools] Instalando PyInstaller...
pip install pyinstaller --upgrade

echo.
echo [ASPV Tools] Compilando ejecutable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ASPVTools" ^
    --add-data "aspv_tools.py;." ^
    aspv_tools.py

echo.
echo [ASPV Tools] Listo! El ejecutable se encuentra en: dist\ASPVTools.exe
echo.
pause
