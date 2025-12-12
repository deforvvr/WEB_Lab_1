@echo off
chcp 65001 >nul
cd /d "%~dp0.."
cls
echo ========================================
echo ПРОСТОЕ РЕШЕНИЕ ОШИБКИ
echo ========================================
echo.
echo ВНИМАНИЕ: Сначала остановите сервер (Ctrl+C)!
echo.
pause
cls

echo Шаг 1: Создание папки migrations...
if not exist studio\migrations mkdir studio\migrations
if not exist studio\migrations\__init__.py echo. > studio\migrations\__init__.py
echo [OK]
echo.

echo Шаг 2: Удаление старой базы данных...
if exist db.sqlite3 del /q db.sqlite3
echo [OK]
echo.

echo Шаг 3: Создание миграций...
python manage.py makemigrations studio
echo.

echo Шаг 4: Применение миграций...
python manage.py migrate
echo.

echo Шаг 5: Проверка результата...
if exist db.sqlite3 (
    echo [OK] База данных создана
) else (
    echo [ОШИБКА] База данных не создана!
)
if exist studio\migrations\0001_initial.py (
    echo [OK] Миграции созданы
) else (
    echo [ОШИБКА] Миграции не созданы!
)
echo.

echo ========================================
echo ГОТОВО!
echo ========================================
echo.
echo Теперь запустите: scripts\ЗАПУСК.bat
echo.
pause

