
@echo off
title Communication AI Setup

echo =====================================
echo   COMMUNICATION AI - SETUP
echo =====================================

python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo =====================================
echo Setup completed!
echo Run Start_Communication_AI.bat
echo =====================================
pause
