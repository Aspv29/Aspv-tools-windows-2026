# ============================================================
#  ASPV Tools - PowerShell Build Script
#  Compila aspv_tools.py en un unico ejecutable para Windows
#  Requiere Python 3.8+ y pip instalado
# ============================================================

Write-Host "[ASPV Tools] Instalando PyInstaller..." -ForegroundColor Cyan
pip install pyinstaller --upgrade

Write-Host "`n[ASPV Tools] Compilando ejecutable..." -ForegroundColor Cyan
pyinstaller `
    --onefile `
    --windowed `
    --name "ASPVTools" `
    --hidden-import=tkinter `
    --hidden-import=tkinter.ttk `
    --hidden-import=tkinter.messagebox `
    --hidden-import=tkinter.scrolledtext `
    --hidden-import=tkinter.filedialog `
    aspv_tools.py

Write-Host "`n[ASPV Tools] Build completado!" -ForegroundColor Green
Write-Host "Ejecutable: dist\ASPVTools.exe" -ForegroundColor Yellow
