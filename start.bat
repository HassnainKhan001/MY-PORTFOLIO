@echo off
title Muhammad Hasnain — Developer Portfolio
color 0B

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║       Muhammad Hasnain — Developer Portfolio         ║
echo  ║                 Portfolio Engine v4.1.0               ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

:: Check for virtual environment
if not exist "env\Scripts\python.exe" (
    echo  [!] Virtual environment NOT found in \env
    pause
    exit /b
)

echo  [*] Verifying dependencies...
env\Scripts\python.exe -m pip install -r requirements.txt --quiet

echo.
echo  [+] Environment synchronized.
echo  [+] Launching FastAPI server on http://127.0.0.1:8000
echo.
echo  [*] Available routes:
echo       http://127.0.0.1:8000              - Homepage
echo       http://127.0.0.1:8000/projects     - Projects
echo       http://127.0.0.1:8000/services     - Services
echo       http://127.0.0.1:8000/neural-net   - Architecture
echo       http://127.0.0.1:8000/diagnostic   - AI Assistant
echo       http://127.0.0.1:8000/contact      - Contact
echo       http://127.0.0.1:8000/api/docs     - API Docs
echo.
echo  [*] Press CTRL+C to stop the server.
echo.

:: Start server directly
echo  ======================================================
echo  [!] DO NOT CLOSE THIS WINDOW. THIS IS THE SERVER.
echo  [!] IF YOU CLOSE THIS, THE WEBSITE WILL STOP WORKING.
echo  ======================================================
echo.
env\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000

echo.
echo  [!] The server stopped unexpectedly.
pause
