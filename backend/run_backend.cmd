@echo off
cd /d "%~dp0"
set "PYTHONPATH=%cd%"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port %PORT% --app-dir .

rem If PORT is not provided by the environment, default to 8002
if "%PORT%"=="" (
	set "PORT=8002"
)
