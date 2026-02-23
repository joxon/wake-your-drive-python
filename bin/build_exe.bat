@echo off
SET VENV_DIR="venv"

REM Create virtual environment if it doesn't exist
IF NOT EXIST %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

echo Activating virtual environment...
CALL %VENV_DIR%\Scripts\activate.bat

echo Installing Dependencies...
pip install -r requirements.txt

echo.
echo Building WakeTheDrive.exe...
pyinstaller --onefile --noconsole --name "WakeTheDrive" ../src/__main__.py

echo.
echo Done! Your executable is in the "dist" folder.

echo Deactivating virtual environment...
deactivate

pause
