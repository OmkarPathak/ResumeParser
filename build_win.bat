@echo off

:: Setup directories
set APP_DIR=%~dp0
cd "resume_parser"

echo Building Resume Parser on Windows...

:: 1. Setup Virtual Environment
if exist env (
    echo Using existing virtual environment...
) else (
    echo Creating virtual environment...
    python -m venv env
)

call env\Scripts\activate.bat

:: 2. Install Project Dependencies
echo Installing Project Dependencies...
pip install -r requirements.txt

:: 3. Create necessary directories
if not exist models mkdir models

:: 4. Cleanup previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: 5. Run PyInstaller
echo Running PyInstaller...
pyinstaller ResumeParser.spec --noconfirm

:: 6. Post-build Verification
if exist "dist\ResumeParser\ResumeParser.exe" (
    echo Build success! Executable is at resume_parser\dist\ResumeParser\ResumeParser.exe
) else (
    echo Build failed! Executable not found.
    exit /b 1
)

pause
