@echo off
echo Instalando proyecto Naikan...

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Listo! Corre el juego con: python main.py
pause
