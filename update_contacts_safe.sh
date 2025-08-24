#!/bin/bash

README="README.md"
BRANCH="main"

# Новые контакты
NEW_TELEGRAM="@MSL72Rph"
NEW_EMAIL="pharmdoktor1972@icloud.com"

# Проверяем, что файл существует
if [ ! -f "$README" ]; then
    echo "❌ Файл $README не найден!"
    exit 1
fi

# Обновляем блок контактов
awk -v tg="$NEW_TELEGRAM" -v em="$NEW_EMAIL" '
BEGIN {in_contacts=0; contacts_updated=0}
/^## Контакты/ {
    print
    print "- Telegram: " tg
    print "- Email: " em
    in_contacts=1
    contacts_updated=1
    next
}
in_contacts {
    # продолжаем игнорировать строки до конца блока (пустые или начинаются с "-")
    if ($0 ~ /^$/ || $0 ~ /^-/) next
    else in_contacts=0
}
{print}
END {
    if (contacts_updated==0) {
        print "\n## Контакты\n- Telegram: " tg "\n- Email: " em
    }
}
' "$README" > "${README}.tmp"

mv "${README}.tmp" "$README"

# Git команды
git add "$README"
git commit -m "Обновлены контакты в профиле (безопасная версия)"
git push -u origin "$BRANCH"

echo "✅ Контакты безопасно обновлены и отправлены на GitHub!"
