# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

APP_NAME = 'Гримуар'
APP_ICON = 'icon.icns'
MAIN_SCRIPT = 'Гримуар.py'
LIBPQ_PATH = '/opt/homebrew/Cellar/libpq/17.5/lib/libpq.5.dylib'

def create_launcher():
    with open('launcher.sh', 'w') as f:
        f.write(f'''#!/bin/bash
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
LOG="$HOME/Desktop/{APP_NAME}_launch.log"
echo "Запуск из $DIR в $(date)" > "$LOG"
export DYLD_LIBRARY_PATH="$DIR/../Frameworks"
exec "$DIR/{APP_NAME}_bin" >> "$LOG" 2>&1
''')
    os.chmod('launcher.sh', 0o755)

create_launcher()

a = Analysis(
    [MAIN_SCRIPT],
    pathex=[os.getcwd()],
    binaries=[(LIBPQ_PATH, 'Frameworks')],
    datas=[
        ('calendar.html', '.'),
        (APP_ICON, '.'),
        ('calendar.ics', '.'),
        ('import_ics_to_calendar.sh', '.'),
        ('index.global.min.js', '.'),
        ('launcher.sh', '.'),
        ('logic.py', '.'),
        ('ui_main.py', '.')
    ],
    hiddenimports=collect_submodules('psycopg'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=f'{APP_NAME}_bin',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,  # Включено для отладки
    icon=APP_ICON,
)

app = BUNDLE(
    exe,
    name=f'{APP_NAME}.app',
    icon=APP_ICON,
    info_plist={
        'CFBundleExecutable': 'launcher',
        'CFBundleIdentifier': f'com.{APP_NAME.lower()}.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': 'False',  # Явно отключаем HiDPI
        'NSSupportsAutomaticGraphicsSwitching': 'False',
        'LSEnvironment': {
            'QT_MAC_WANTS_LAYER': '1',
            'QT_METAL_ENABLED': '0',
            'QT_QUICK_BACKEND': 'software',
            'QT_QPA_PLATFORM': 'minimal',
            'DYLD_FALLBACK_LIBRARY_PATH': '@executable_path/../Frameworks'
        }
    }
)

# Копируем лаунчер
if os.path.exists('dist'):
    shutil.copy('launcher.sh', f'dist/{APP_NAME}.app/Contents/MacOS/launcher')
    os.chmod(f'dist/{APP_NAME}.app/Contents/MacOS/launcher', 0o755)

    print("Сборка завершена. Проверьте:")
    print(f"1. Файл логов: ~/Desktop/{APP_NAME}_launch.log")
    print("2. Структуру app:")
    print(f"  dist/{APP_NAME}.app/Contents/MacOS/ должен содержать:")
    print("  - launcher (скрипт)")
    print(f"  - {APP_NAME}_bin (исполняемый файл)")
else:
    print("Ошибка: папка dist не существует. Сначала выполните сборку.")