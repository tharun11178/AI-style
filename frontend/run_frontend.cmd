@echo off
cd /d "%~dp0"
python -m http.server 5175 --bind 127.0.0.1 -d dist
