@echo off
REM ASPV Tools Premium - Build Script for Windows
REM Compiles the Electron application into distributable executables

echo ========================================
echo ASPV Tools Premium v3.0 - Build Script
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Checking Node.js version...
node --version
npm --version
echo.

echo [2/4] Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/4] Building Electron application...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.

echo [4/4] Build completed successfully!
echo.
echo ========================================
echo Executable files are in the 'dist' folder
echo ========================================
echo.

REM List generated files
if exist dist (
    echo Generated files:
    dir /b dist\*.exe
    echo.
)

echo Build process completed!
pause
