# ============================================================
#  ASPV Tools - PowerShell Build Script
#  Compila aspv_tools.py en un unico ejecutable para Windows
# ============================================================

Write-Host "[ASPV Tools] Instalando PyInstaller..." -ForegroundColor Cyan
pip install pyinstaller --upgrade

Write-Host "`n[ASPV Tools] Compilando ejecutable..." -ForegroundColor Cyan
pyinstaller `
    --onefile `
    --windowed `
    --name "ASPVTools" `
    aspv_tools.py

Write-Host "`n[ASPV Tools] Build completado!" -ForegroundColor Green
Write-Host "Ejecutable: dist\ASPVTools.exe" -ForegroundColor Yellow
