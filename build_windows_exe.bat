@echo off
REM Build Windows .exe for desktop security app using PyInstaller
REM Run this script from the project root

REM Ensure PyInstaller is installed
pip install pyinstaller

REM Build the executable
pyinstaller --noconfirm --onefile --windowed --icon=windows/app_icon.ico --name windows_locker main.py

REM Output will be in the dist/ folder as windows_locker.exe
ECHO Build complete. Find windows_locker.exe in the dist/ folder.