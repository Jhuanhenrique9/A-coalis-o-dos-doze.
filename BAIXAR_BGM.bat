@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
%PY% -m pip install pygame
if errorlevel 1 echo Nao foi possivel instalar pygame. Verifique a conexao e a versao do Python.
%PY% baixar_bgm.py
pause
