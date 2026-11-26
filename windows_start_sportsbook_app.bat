@echo off
setlocal

echo Starting backend...
start "Backend" /b cmd /c "uvicorn backend.main:app --reload"
set BACKEND_PID=%ERRORLEVEL%

echo Starting frontend...
start "Frontend" /b cmd /c "npm --prefix frontend run dev"

timeout /t 2 /nobreak >nul

start "" http://localhost:5173

echo.
echo Application started.
echo Press Ctrl+C to stop.

:wait
timeout /t 1 /nobreak >nul
goto wait
