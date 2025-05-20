@echo off
setlocal enabledelayedexpansion

set "CONDA_CANDIDATES=%USERPROFILE%\Anaconda3;%USERPROFILE%\Miniconda3;C:\ProgramData\Anaconda3;C:\ProgramData\Miniconda3"
set "CONDA_BAT="
for %%D in (%CONDA_CANDIDATES%) do (
    if exist "%%D\condabin\conda.bat" (
        set "CONDA_BAT=%%D\condabin\conda.bat"
        goto :conda_found
    )
)

echo.
echo [ERREUR] Impossible de trouver Anaconda ou Miniconda.
echo Installez Anaconda depuis https://www.anaconda.com/products/distribution
echo ou vérifiez l'emplacement de votre installation.
pause
exit /b 1

:conda_found
echo [INFO] Conda détecté: %CONDA_BAT%
CALL "%CONDA_BAT%" activate base

set "ENV_NAME=quchemenv"

echo Suppression de l’environnement existant...
CALL "%CONDA_BAT%" env list | findstr /B /C:"%ENV_NAME%" >nul
IF %ERRORLEVEL% EQU 0 (
    echo Suppression de l’environnement existant: %ENV_NAME%
    CALL "%CONDA_BAT%" remove -n %ENV_NAME% --all -y
)

CALL "%CONDA_BAT%" config --add channels conda-forge
CALL "%CONDA_BAT%" config --set channel_priority strict

CALL "%CONDA_BAT%" create -n %ENV_NAME% ^
  python=3.8 ^
  numpy=1.21.6 ^
  scipy=1.9.3 ^
  scikit-learn=0.23.2 ^
  openbabel ^
  mayavi ^
  -c conda-forge -y

CALL "%CONDA_BAT%" activate %ENV_NAME%

pip install ^
  requests==2.25.1 ^
  psutil==5.8.0 ^
  cclib==1.8.1 ^
  Pillow==10.4.0 ^
  pylatex==1.4.1 ^
  cython==0.29.21 ^
  python-dotenv==1.0.1 ^
  python-docx==1.1.2


cd /d "%~dp0"
rmdir /s /q orbkit >nul 2>&1
git clone https://github.com/orbkit/orbkit.git
cd orbkit
pip install .
cd ..
echo
echo Début
python main.py examples\H2O_TD.log examples\H2O_OPT.log

echo.
echo Terminé.
pause
