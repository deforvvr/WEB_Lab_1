@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ========================================
echo Запуск Django сервера разработки
echo ========================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Пожалуйста, установите Python с https://www.python.org/downloads/
    echo При установке обязательно поставьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo Python найден!
echo.

REM Проверка и создание структуры папок
if not exist "static" (
    echo Создание папки static...
    mkdir static
)
if not exist "static\src" (
    echo Создание папки static\src...
    mkdir static\src
)

REM Копирование изображений если есть папка src
if exist "src" (
    echo Копирование изображений в static\src...
    copy /Y src\*.* static\src\ >nul 2>&1
)

REM Проверка зависимостей
echo Проверка зависимостей...
python -m pip show django >nul 2>&1
if errorlevel 1 (
    echo Django не установлен. Устанавливаю зависимости...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ОШИБКА: Не удалось установить зависимости!
        pause
        exit /b 1
    )
    echo Зависимости установлены!
    echo.
) else (
    echo Зависимости уже установлены.
    echo.
)

REM Применение миграций
echo Проверка и применение миграций базы данных...
python manage.py makemigrations >nul 2>&1
python manage.py migrate
echo.

echo ========================================
echo Запуск сервера...
echo ========================================
echo.
echo Сервер будет доступен по адресу: http://127.0.0.1:8000/
echo Админ-панель: http://127.0.0.1:8000/admin/
echo.
echo Для остановки сервера нажмите Ctrl+C
echo.

python manage.py runserver

pause

