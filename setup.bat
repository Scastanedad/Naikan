@echo off
echo Instalando proyecto Naikan...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta instalado. Descargandolo...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo Instalando Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python instalado! Cierra esta ventana, abre el setup.bat de nuevo y listo.
    pause
    exit
)

if exist venv (
    echo Borrando venv anterior...
    rmdir /s /q venv
)

if exist .venv (
    echo Borrando .venv anterior...
    rmdir /s /q .venv
)

python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install --only-binary=pygame pygame==2.5.2

echo.
echo Listo! Corre el juego con: python main.py
pause
