#!/bin/bash

# Путь к папке с ботами
BOT_DIR="$HOME/bots/price_bot"

# Переходим в папку проекта
cd "$BOT_DIR" || { echo "Папка $BOT_DIR не найдена!"; exit 1; }

# Активируем виртуальное окружение
source venv/bin/activate || { echo "Не удалось активировать venv!"; exit 1; }

# Запускаем оба бота параллельно
python price_bot.py &
python panic_bot.py &

echo "Оба бота запущены. Логи выводятся в терминал."
wait

