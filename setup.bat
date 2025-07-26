@echo off
echo 🚀 MXTSessions Generator Setup Script
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Install required packages
echo 📦 Installing required packages...
pip install cryptography pandas openpyxl flask flask-cors

if %errorlevel% equ 0 (
    echo ✅ All packages installed successfully!
) else (
    echo ❌ Failed to install packages. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Usage examples:
echo   python encrypt_tool.py encrypt "password123" "my_key"
echo   python encrypt_tool.py batch-encrypt input.xlsx output.xlsx "my_key"
echo   python app.py  # Run the backend server locally
echo.
pause
