@echo off
REM Setup script for Semantic Movie Recommender on Windows
REM Run this once to install all dependencies

title Movie Recommender - Setup
color 0A

echo.
echo ============================================================
echo    MOVIE RECOMMENDER - SETUP SCRIPT (Windows)
echo ============================================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.x from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo ✓ Python and Node.js found
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✓ Python dependencies installed
echo.

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo ✓ Frontend dependencies installed
echo.

echo ============================================================
echo ✓ SETUP COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: start_all.bat (to start both servers)
echo    OR manually start servers:
echo    - Terminal 1: cd scripts ^& python api_server.py
echo    - Terminal 2: cd frontend ^& npm run dev
echo.
echo 2. Open browser: http://localhost:5173
echo.
echo 3. Select an emotion to get movie recommendations!
echo.
echo ============================================================
echo.

pause
