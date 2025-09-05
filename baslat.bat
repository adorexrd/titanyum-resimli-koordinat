@echo off
title ADOREXRD BOT BASLIYOR...
:: Renk ayarla
color 0a

:: ASCII animasyon
cls
echo.
echo.
echo    █████╗ ██████╗  ██████╗ ██████╗ ███████╗██╗  ██╗██████╗ ██████╗ 
ping -n 1 >nul localhost
echo   ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔══██╗
ping -n 1 >nul localhost
echo   ███████║██████╔╝██║   ██║██████╔╝█████╗  ███████║██████╔╝██║  ██║
ping -n 1 >nul localhost
echo   ██╔══██║██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝  ██╔══██║██╔═══╝ ██║  ██║
ping -n 1 >nul localhost
echo   ██║  ██║██║     ╚██████╔╝██║     ███████╗██║  ██║██║     ██████╔╝
ping -n 1 >nul localhost
echo   ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═════╝ 
ping -n 2 >nul localhost

echo.
echo [1/3] Sanal ortam kontrol ediliyor...
if not exist venv (
    py -m venv venv
)

call venv\Scripts\activate

echo [2/3] Kutuphaneler kontrol ediliyor...
pip install --upgrade pip >nul
pip install discord.py pymongo easyocr pillow numpy >nul

echo [3/3] Bot baslatiliyor...
timeout /t 1 >nul
cls
color 0b
echo ================================
echo     🚀 ADOREXRD BOT CALISIYOR 🚀
echo ================================
echo.
python main.py

pause
