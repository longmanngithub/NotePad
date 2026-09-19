@echo off
setlocal enabledelayedexpansion

echo ====================================================
echo  Building NotePad for Windows (.exe)
echo ====================================================

:: Find Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo Error: Python is not installed or not in PATH.
        echo Please install Python 3.10, 3.11, or 3.12 from python.org.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py -3
    )
) else (
    set PYTHON_CMD=python
)

echo Using: %PYTHON_CMD%

:: Setup virtual environment if needed
if not exist "venv_build" (
    echo Creating virtual environment for clean build...
    %PYTHON_CMD% -m venv venv_build
)

call venv_build\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pyqt5 pyinstaller

echo Building NotePad.exe with PyInstaller...
python -m PyInstaller --clean --noconfirm NotePad.spec

if exist "dist\NotePad.exe" (
    echo.
    echo ====================================================
    echo  Build successful!
    echo  Executable: dist\NotePad.exe
    echo ====================================================
) else (
    echo.
    echo Error: dist\NotePad.exe was not created.
)

pause
