@echo off
echo Starting Baseball Sim - Server and Frontend
echo.
echo Starting API Server in new window...
start "Baseball Sim API Server" cmd /k "cd backend && python api_server.py"

echo Waiting 3 seconds for server to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend in new window...
start "Baseball Sim Frontend" cmd /k "cd frontend && npm start"

echo.
echo Both services are starting in separate windows.
echo Close this window when done.
pause
