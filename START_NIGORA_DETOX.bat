@echo off
title NIGORA DETOX Marketplace & AI Assistant
echo ========================================================
echo   NIGORA DETOX - DETOKS & OZDIRUVCHI MARKETPLACE
echo   Nigora AI Konsultant va Click To'lov Platformasi
echo ========================================================
echo.
echo Server ishga tushirilmoqda...
cd /d "E:\nigora_detox_marketplace"
start http://127.0.0.1:8000
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
