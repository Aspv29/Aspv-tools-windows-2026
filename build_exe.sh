#!/bin/bash
# ASPV Tools - Build Script for Linux/Unix
# This script builds the executable using PyInstaller

echo "=========================================="
echo "ASPV Tools - Build Script (Linux/Unix)"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

echo "✓ Python detectado: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 no está instalado"
    exit 1
fi

echo "✓ pip3 detectado"
echo ""

# Install dependencies
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo ""
echo "✓ Dependencias instaladas correctamente"
echo ""

# Build executable
echo "🔨 Construyendo ejecutable con PyInstaller..."
echo ""

pyinstaller ASPVTools.spec --clean --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ BUILD EXITOSO"
    echo "=========================================="
    echo ""
    echo "El ejecutable se encuentra en: ./dist/ASPVTools"
    echo ""
    echo "Para ejecutar:"
    echo "  ./dist/ASPVTools"
    echo ""
    echo "Nota: Este programa está diseñado para Windows."
    echo "En Linux, muchas funciones no estarán disponibles."
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ ERROR EN EL BUILD"
    echo "=========================================="
    echo ""
    echo "Revisa los errores anteriores para más detalles."
    exit 1
fi
