#!/bin/bash
# Build Windows executable using PyInstaller
# Run this script on Windows after installing Python 3 and PyInstaller

pyinstaller --onefile --windowed --name FrameChanger --icon src/framechanger/icon.ico src/framechanger/app.py
