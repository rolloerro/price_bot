#!/bin/bash

# Пути к ботам
BOT1="bot1.py"
BOT2="bot2.py"
BOT3="price_bot.py"

# Виртуальное окружение
VENV="./venv/bin/python3"

# Функция для остановки всех ботов
stop_bots() {
    echo "Останавливаем все боты..."
    pkill -f "$BOT1"
    pkill -f "$BOT2"
    pkill -f "$BOT3"
    echo "Все боты остановлены."
}

# Функция для запуска всех ботов
start_bots() {
    echo "Запускаем боты через venv..."
    "$VENV" "$BOT1" &
    "$VENV" "$BOT2" &
    "$VENV" "$BOT3" &
    echo "Все боты запущены!"
}

# Проверяем аргумент скрипта
if [ "$1" == "stop" ]; then
    stop_bots
elif [ "$1" == "start" ]; then
    stop_bots  # сначала чистим старые процессы
    start_bots
else
    echo "Использование: $0 start | stop"
fi
