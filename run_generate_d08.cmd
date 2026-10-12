@echo off
cd /d "%~dp0"
python backend-engineering-knowledge-base\_generators\generate_d08_notes.py
if errorlevel 1 exit /b 1
echo Done. See FINISHED and FAILURES lines above.
