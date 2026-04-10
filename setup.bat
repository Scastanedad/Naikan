@echo off
echo Instalando proyecto Naikan...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta instalado. Descargandolo...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo Instalando Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    timeout /t 3
)

python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install --only-binary=pygame pygame
pip install -r requirements.txt --only-binary=:all: --ignore-requires-python

echo.
echo Listo! Corre el juego con: python main.py
pause
