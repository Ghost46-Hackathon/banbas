@echo off
echo ============================================================
echo BANBAS RESORT - Django Development Server (Network Access)
echo ============================================================
echo Your IP Address: 10.10.152.117
echo Server Port: 8000
echo.
echo Access from any device on your network:
echo   Website: http://10.10.152.117:8000/
echo   Admin:   http://10.10.152.117:8000/admin/
echo.
echo IMPORTANT: If this is your first time running on network:
echo 1. Windows may ask to allow Python through firewall - CLICK ALLOW
echo 2. Or manually add firewall rule (Run as Admin):
echo    netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
echo.
echo Starting server...
echo Press Ctrl+C to stop
echo ============================================================
echo.

python manage.py runserver 0.0.0.0:8000

pause