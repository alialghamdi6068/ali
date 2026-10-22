@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher was not found. Install Python 3.11+ from https://www.python.org/downloads/
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -e ".[dev]"
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m ali
if errorlevel 1 goto :error
exit /b 0
:error
echo.
echo Ali could not start. Read the error above.
pause
exit /b 1
