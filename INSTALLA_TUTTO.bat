@echo off
cd /d "%~dp0"
echo.
echo ============================================================
echo   RIS NAPOLI - INSTALLAZIONE COMPLETA
echo ============================================================
echo.

echo [1/6] storage.js + rimozione file vecchi...
python file_01_setup.py
if errorlevel 1 ( echo ERRORE 01 & pause & exit /b )

echo [2/6] App.jsx...
python file_02_app.py
if errorlevel 1 ( echo ERRORE 02 & pause & exit /b )

echo [3/6] Dashboard.jsx...
python file_03_dashboard.py
if errorlevel 1 ( echo ERRORE 03 & pause & exit /b )

echo [4/6] Rapporto.jsx...
python file_04_rapporto.py
if errorlevel 1 ( echo ERRORE 04 & pause & exit /b )

echo [5/6] Anteprima.jsx...
python file_05_anteprima.py
if errorlevel 1 ( echo ERRORE 05 & pause & exit /b )

echo [6/6] Sicurezza .gitignore...
python file_06_gitignore.py
if errorlevel 1 ( echo ERRORE 06 & pause & exit /b )

echo.
echo ============================================================
echo   FILE PRONTI - Git commit e push
echo ============================================================
echo.
set /p COMMIT_MSG="Messaggio commit: "
echo.
git add .
git commit -m "%COMMIT_MSG%"
git push
echo.
echo ============================================================
echo   PUSH COMPLETATO - Vercel si aggiorna automaticamente
echo ============================================================
echo.
pause
