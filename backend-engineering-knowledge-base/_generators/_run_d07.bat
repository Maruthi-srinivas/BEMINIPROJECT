@echo off
cd /d "%~dp0"
python d07_all_topics.py > d07_run_log.txt 2>&1
type d07_run_log.txt
