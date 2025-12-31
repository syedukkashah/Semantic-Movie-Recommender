@echo off
REM Quick Start Script for Movie Recommender
REM Starts both Frontend and Backend servers in new windows

title Movie Recommender - Quick Start
color 0A
cls

echo.
echo ============================================================
echo    MOVIE RECOMMENDER - QUICK START
echo ============================================================
echo.

REM Check if we're in the right directory
if not exist "scripts\api_server.py" (
    echo ERROR: api_server.py not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ERROR: frontend\package.json not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✓ Project files found
echo.

echo Starting servers...
echo.

echo 1. Starting Backend API Server (Port 5000)...
echo    Location: scripts\api_server.py
echo.

REM Start backend in a new window
start "Movie Recommender - Backend API" cmd /k "cd scripts && python api_server.py"

timeout /t 3 /nobreak

echo 2. Starting Frontend Development Server (Port 5173)...
echo    Location: frontend\
echo.

REM Start frontend in a new window
start "Movie Recommender - Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 2 /nobreak

echo.
echo ============================================================
echo ✓ Both servers are starting!
echo.
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:5000
echo.
echo Check the console windows to see startup messages.
echo Press Ctrl+C in each window to stop the servers.
echo ============================================================
echo.
echo Opening browser...

REM Try to open in default browser
start http://localhost:5173

echo.
echo Done! Enjoy emotion-based movie recommendations! 🍿
echo.
pause
