from setuptools import setup

APP = ['Гримуар.py']  # Главный исполняемый файл
DATA_FILES = [
    'bufer.json',
    'calendar.html',
    'calendar.ics',
    'icon.icns',
    'import_ics_to_calendar.sh',
    'index.global.min.js',
    'logic.py',
    'ui_main.py'
]
OPTIONS = {
    'argv_emulation': True,  # Для корректной работы аргументов командной строки
    'iconfile': 'icon.icns',  # Иконка приложения
    'packages': ['PySide6', 'psycopg', 'ics'],  # Основные зависимости
    'plist': {
        'CFBundleName': 'Гримуар',  # Имя приложения
        'CFBundleShortVersionString': '1.0.0',  # Версия
        'CFBundleGetInfoString': 'Приложение для работы с календарем',
        'NSHumanReadableCopyright': '© 2024 Ваше Имя',
    'strip': True,  # Удаляет debug-символы
    'optimize': 2,  # Оптимизация кода Python
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)