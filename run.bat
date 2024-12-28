@echo off
set VENV_PATH=.\.venv\Scripts\Activate.ps1

if exist "%VENV_PATH%" (
    powershell.exe -ExecutionPolicy Bypass -File "%VENV_PATH%"
    powershell -Command "&{python main.py;}"
) else (
    powershell -Command "&{python -m venv .venv;}"
    powershell.exe -ExecutionPolicy Bypass -File "%VENV_PATH%"
    powershell -Command "&{pip install -r requirements.txt;}"
    powershell -Command "&{python main.py;}"
)

pause