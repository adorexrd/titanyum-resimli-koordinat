@echo off
title Discord Resimli Koordinat Bot Baslat
echo [1/3] Sanal ortam oluşturuluyor...
python -m venv venv

echo [2/3] Gerekli kutuphaneler yukleniyor...
call venv\Scripts\activate
pip install --upgrade pip
pip install discord.py pymongo easyocr pillow numpy

echo [3/3] Bot baslatiliyor...
python index.py

pause
