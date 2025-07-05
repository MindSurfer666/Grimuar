#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG="$HOME/Desktop/Гримуар_launch.log"
echo "Запуск из $DIR в $(date)" > "$LOG"
export DYLD_LIBRARY_PATH="$DIR/../Frameworks"
exec "$DIR/Гримуар_bin" >> "$LOG" 2>&1
