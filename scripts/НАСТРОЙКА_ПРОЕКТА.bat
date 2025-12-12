@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ========================================
echo Настройка проекта Django
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    pause
    exit /b 1
)

echo Шаг 1: Установка зависимостей...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА при установке зависимостей!
    pause
    exit /b 1
)
echo Зависимости установлены.
echo.

echo Шаг 2: Удаление старой базы данных (если есть)...
if exist "db.sqlite3" (
    del /q db.sqlite3
    echo Старая база данных удалена.
)
echo.

echo Шаг 3: Создание миграций...
python manage.py makemigrations
if errorlevel 1 (
    echo ОШИБКА при создании миграций!
    pause
    exit /b 1
)
echo Миграции созданы.
echo.

echo Шаг 4: Применение миграций...
python manage.py migrate
if errorlevel 1 (
    echo ОШИБКА при применении миграций!
    pause
    exit /b 1
)
echo Миграции применены.
echo.

echo ========================================
echo Проект настроен!
echo ========================================
echo.
echo Теперь вы можете:
echo 1. Создать администратора: python manage.py createsuperuser
echo 2. Запустить сервер: scripts\ЗАПУСК.bat
echo.
pause

