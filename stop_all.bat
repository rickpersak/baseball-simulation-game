@echo off
echo Stopping Baseball Sim - Server and Frontend
echo.

echo Stopping Python API Server...
taskkill /f /im python.exe >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ Python processes terminated
) else (
    echo - No Python processes found
)

echo Stopping Node.js Frontend...
taskkill /f /im node.exe >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ Node.js processes terminated
) else (
    echo - No Node.js processes found
)

echo Stopping any remaining npm processes...
taskkill /f /im npm.cmd >nul 2>&1
taskkill /f /im cmd.exe /fi "WINDOWTITLE eq Baseball Sim*" >nul 2>&1

echo.
echo All Baseball Sim processes have been stopped.
echo You can now safely restart the application.
pause
