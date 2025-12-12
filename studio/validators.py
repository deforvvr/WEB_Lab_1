from django.core.exceptions import ValidationError
import re


def validate_password_complexity(password):
    """
    Валидация пароля согласно требованиям:
    - не менее 8 символов
    - не более 128 символов
    - как минимум одна заглавная и одна строчная буква
    - только латинские или кириллические буквы
    - как минимум одна цифра
    - только арабские цифры
    - без пробелов
    - специальный символ
    """
    errors = []
    
    # Проверка длины
    if len(password) < 8:
        errors.append('Пароль должен содержать не менее 8 символов.')
    if len(password) > 128:
        errors.append('Пароль должен содержать не более 128 символов.')
    
    # Проверка на пробелы
    if ' ' in password:
        errors.append('Пароль не должен содержать пробелы.')
    
    # Проверка на заглавные и строчные буквы (латиница или кириллица)
    has_uppercase = bool(re.search(r'[A-ZА-ЯЁ]', password))
    has_lowercase = bool(re.search(r'[a-zа-яё]', password))
    
    if not has_uppercase:
        errors.append('Пароль должен содержать хотя бы одну заглавную букву (латиница или кириллица).')
    if not has_lowercase:
        errors.append('Пароль должен содержать хотя бы одну строчную букву (латиница или кириллица).')
    
    # Проверка на наличие только латинских или кириллических букв
    # Разрешаем только буквы, цифры и специальные символы
    # Экранируем специальные символы для regex
    allowed_chars_pattern = r'^[a-zA-Zа-яА-ЯёЁ0-9' + re.escape(r'!@#$%^&*()_+-=[]{};\':"|,.<>/?') + r']+$'
    if not re.match(allowed_chars_pattern, password):
        errors.append('Пароль содержит недопустимые символы. Разрешены только латинские или кириллические буквы, арабские цифры и специальные символы.')
    
    # Проверка на наличие цифры (только арабские)
    has_digit = bool(re.search(r'[0-9]', password))
    if not has_digit:
        errors.append('Пароль должен содержать хотя бы одну цифру (0-9).')
    
    # Проверка на специальный символ
    special_chars = r'!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?'
    # Экранируем специальные символы для regex
    escaped_chars = re.escape(special_chars)
    has_special = bool(re.search(r'[' + escaped_chars + ']', password))
    if not has_special:
        errors.append('Пароль должен содержать хотя бы один специальный символ (!@#$%^&*()_+-=[]{};\':"|,.<>/?).')
    
    if errors:
        raise ValidationError(errors)
    
    return password

