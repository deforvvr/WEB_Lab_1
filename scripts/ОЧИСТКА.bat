@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ========================================
echo Очистка проекта от временных файлов
echo ========================================
echo.

echo Удаление кэша Python...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "studio\__pycache__" rmdir /s /q "studio\__pycache__"
if exist "studio\migrations\__pycache__" rmdir /s /q "studio\migrations\__pycache__"
if exist "theater_studio\__pycache__" rmdir /s /q "theater_studio\__pycache__"

echo Удаление временных файлов...
del /q *.pyc 2>nul
del /q studio\*.pyc 2>nul
del /q theater_studio\*.pyc 2>nul

echo.
echo Очистка завершена!
echo.
echo Примечание: База данных db.sqlite3 и медиафайлы не удалены.
echo.
pause

