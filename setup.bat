@echo off
echo Instalando proyecto Naikan...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta instalado. Descargandolo...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo Instalando Python, acepta los permisos que aparezcan...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Listo! Corre el juego con: python main.py
pause