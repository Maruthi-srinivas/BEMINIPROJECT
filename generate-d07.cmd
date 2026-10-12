@echo off
cd /d "%~dp0backend-engineering-knowledge-base\_generators"
python d07_all_topics.py
if errorlevel 1 exit /b 1
echo Done. See FINISHED line above.
