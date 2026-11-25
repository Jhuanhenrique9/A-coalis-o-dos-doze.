@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
%PY% -m pip install pyinstaller pygame
if errorlevel 1 goto erro
%PY% -m PyInstaller --noconfirm --clean main.spec
if errorlevel 1 goto erro
echo Executavel criado em dist\The Battle.exe
pause
exit /b 0
:erro
echo Nao foi possivel compilar. Verifique a instalacao do Python e a conexao.
pause
exit /b 1
