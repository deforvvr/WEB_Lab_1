@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ========================================
echo Проверка структуры проекта
echo ========================================
echo.

echo Проверка наличия Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python с https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo [OK] Python найден
    python --version
)

echo.
echo Проверка зависимостей...
python -m pip show django >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Django не установлен
    echo Выполните: pip install -r requirements.txt
) else (
    echo [OK] Django установлен
    python -m pip show django | findstr "Version"
)

echo.
echo Проверка структуры папок...
if exist "templates\" (
    echo [OK] Папка templates существует
) else (
    echo [ОШИБКА] Папка templates не найдена!
)

if exist "static\" (
    echo [OK] Папка static существует
) else (
    echo [ОШИБКА] Папка static не найдена!
)

if exist "static\styles.css" (
    echo [OK] Файл styles.css найден
) else (
    echo [ОШИБКА] Файл static\styles.css не найден!
)

if exist "static\src\" (
    echo [OK] Папка static\src существует
) else (
    echo [ОШИБКА] Папка static\src не найдена!
)

if exist "studio\" (
    echo [OK] Папка studio существует
) else (
    echo [ОШИБКА] Папка studio не найдена!
)

if exist "theater_studio\" (
    echo [OK] Папка theater_studio существует
) else (
    echo [ОШИБКА] Папка theater_studio не найдена!
)

if exist "manage.py" (
    echo [OK] Файл manage.py найден
) else (
    echo [ОШИБКА] Файл manage.py не найден!
)

echo.
echo Проверка миграций...
if exist "db.sqlite3" (
    echo [OK] База данных существует
) else (
    echo [INFO] База данных еще не создана
    echo Выполните: python manage.py migrate
)

echo.
echo ========================================
echo Проверка завершена
echo ========================================
pause

