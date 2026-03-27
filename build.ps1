# ASPV Tools Premium - Build Script for Windows (PowerShell)
# Compiles the Electron application into distributable executables

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ASPV Tools Premium v3.0 - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "[1/4] Node.js version: $nodeVersion" -ForegroundColor Green
    Write-Host "      npm version: $npmVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Node.js is not installed!" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Build application
Write-Host "[3/4] Building Electron application..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Success
Write-Host "[4/4] Build completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Executable files are in the 'dist' folder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# List generated files
if (Test-Path "dist") {
    Write-Host "Generated files:" -ForegroundColor Green
    Get-ChildItem -Path "dist" -Filter "*.exe" | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor White
    }
    Write-Host ""
}

Write-Host "Build process completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"
