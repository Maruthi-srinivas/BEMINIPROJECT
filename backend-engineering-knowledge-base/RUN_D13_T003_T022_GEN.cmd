@echo off
cd /d "%~dp0"
python _gen_d13_t003_t022.py
if errorlevel 1 exit /b 1
echo Done. See FINISHED / FAILURES lines above.
