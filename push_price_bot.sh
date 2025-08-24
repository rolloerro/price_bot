#!/bin/bash

# Дружеский привет
echo "🚀 Привет! Готовим прайс бот к заливке на GitHub..."

# Переходим в папку с ботом (если запускаешь скрипт из другой папки)
cd "$(dirname "$0")"

# Создаём .gitignore, если его нет
if [ ! -f .gitignore ]; then
  echo "venv/" > .gitignore
  echo ".DS_Store" >> .gitignore
  echo ".vscode/" >> .gitignore
  echo ".gitignore создан ✅"
fi

# Инициализация git репозитория, если ещё не инициализирован
if [ ! -d .git ]; then
  git init
  echo "Git репозиторий инициализирован ✅"
fi

# Добавляем все файлы и коммитим
git add .
git commit -m "Добавлен прайс бот" || echo "⚠️ Нечего коммитить, возможно уже закоммичено"

# Создаём ветку main, если ещё не создана
git branch -M main 2>/dev/null || echo "Ветка main уже существует"

# Подключаем удалённый репозиторий (замени ссылку на свой)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/rolloerro/price_bot.git
# Пушим на GitHub
git push -u origin main

echo "🎉 Прайс бот успешно залит на GitHub!"
