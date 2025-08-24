import asyncio
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ⚠️ ВСТАВЬ СВОЙ ТОКЕН
TOKEN = "7564134625:AAEzOcBSyFcK41PqMj4FCRWA0nLBekbL_70"

# ---------- Вспомогательные клавиатуры ----------
def kb_home():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В меню", callback_data="home")]])

def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("😰 Началось прямо сейчас", callback_data="now")],
        [InlineKeyboardButton("🫁 Дыхательные техники", callback_data="breathing_menu")],
        [InlineKeyboardButton("🎯 Успокоение 5-4-3-2-1", callback_data="grounding")],
        [InlineKeyboardButton("📞 SOS / Геолокация", callback_data="sos")],
        [InlineKeyboardButton("ℹ️ Что со мной происходит?", callback_data="info")],
        [InlineKeyboardButton("❗ Когда вызывать скорую", callback_data="when_call")]
    ])

def kb_stop():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ Стоп метроном", callback_data="metronome_stop")]])

# ---------- Старт ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌸 Привет! Я помогу, если началась паническая атака.\n"
        "Ты в безопасности. Это пройдёт. Я рядом.\n\n"
        "Выбери то, что тебе ближе 👇"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=kb_main())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=kb_main())

# ---------- Универсальный метроном ----------
async def run_metronome(context: ContextTypes.DEFAULT_TYPE, chat_id: int,
                        title: str, phases: list[tuple[str, int]],
                        cycles: int = 4):
    """
    phases: список фаз [(название, секунды), ...]
    cycles: количество циклов
    """
    # Сообщение, которое будем редактировать каждую секунду
    msg = await context.bot.send_message(chat_id, f"▶️ Старт: {title}\nГотовимся…", reply_markup=kb_stop())

    # Сохраняем таск в user_data, чтобы можно было остановить
    task = asyncio.current_task()
    context.user_data["metronome_task"] = task
    try:
        for c in range(1, cycles + 1):
            for (label, secs) in phases:
                # по секунде шагаем и редактируем текст
                for s in range(1, secs + 1):
                    bar = "•" * s + " " * (secs - s)
                    txt = (
                        f"{title}\n"
                        f"Цикл {c}/{cycles}\n"
                        f"{label}: {s}/{secs} сек\n"
                        f"[{bar}]"
                    )
                    await msg.edit_text(txt, reply_markup=kb_stop())
                    await asyncio.sleep(1)
        await msg.edit_text(f"✅ Завершено: {title}\nДыши спокойно.", reply_markup=kb_home())
    except asyncio.CancelledError:
        # Пользователь нажал Стоп
        try:
            await msg.edit_text(f"⏹️ Остановлено: {title}", reply_markup=kb_home())
        except Exception:
            pass
        raise
    finally:
        # Убираем ссылку на таск
        context.user_data.pop("metronome_task", None)

# ---------- Кнопки ----------
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "home":
        await start(update, context)
        return

    if data == "now":
        txt = (
            "😰 *Паника прямо сейчас*\n\n"
            "1) Скажи себе: _«Я в безопасности. Это паническая атака. Она пройдёт»_.\n"
            "2) Ладонь на живот. Почувствуй дыхание.\n"
            "3) 3 цикла:\n"
            "   • Вдох носом — 4 сек\n"
            "   • Пауза — 2 сек\n"
            "   • Выдох через губы — 6 сек\n\n"
            "Дальше открой «🫁 Дыхательные техники», если нужно."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "breathing_menu":
        await q.edit_message_text(
            "🫁 Выбери технику дыхания:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◼️ Квадрат 4-4-4-4", callback_data="breath_square"),
                 InlineKeyboardButton("▶️ Метроном 4-4-4-4", callback_data="metro_square")],
                [InlineKeyboardButton("4-7-8 (объяснение)", callback_data="breath_478"),
                 InlineKeyboardButton("▶️ Метроном 4-7-8", callback_data="metro_478")],
                [InlineKeyboardButton("🌬️ Губное дыхание", callback_data="breath_pursed")],
                [InlineKeyboardButton("🧘 Расслабление мышц", callback_data="pmr")],
                [InlineKeyboardButton("🏠 В меню", callback_data="home")]
            ])
        )
        return

    if data == "breath_square":
        txt = (
            "◼️ *Дыхание «Квадрат» 4-4-4-4*\n\n"
            "Вдох 4 → Пауза 4 → Выдох 4 → Пауза 4.\n"
            "3–5 циклов. Дыши животом, плечи расслаблены.\n\n"
            "✨ Подсказка: считай «раз-два-три-четыре»."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "breath_478":
        txt = (
            "🌙 *Дыхание 4-7-8 (замедляет пульс)*\n\n"
            "Вдох носом — 4 сек → Задержка — 7 сек → Выдох через губы — 8 сек.\n"
            "Сделай 4 цикла. Если тяжело — уменьши цифры (например, 3-5-6), сохранив _соотношение_."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "breath_pursed":
        txt = (
            "🌬️ *Губное дыхание*\n\n"
            "1) Вдох носом 2–3 сек\n"
            "2) Сомкни губы «трубочкой» и выдыхай вдвое дольше\n"
            "3) Повтори 5–10 циклов — ощущение нехватки воздуха снизится."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "pmr":
        txt = (
            "🧘 *Постепенное мышечное расслабление*\n\n"
            "Напряги на 5 сек и расслабь по очереди:\n"
            "• Стопы → голени → бёдра\n"
            "• Живот → спина → плечи\n"
            "• Кисти → предплечья → лицо\n\n"
            "Отмечай разницу — тревога снижается."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "grounding":
        txt = (
            "🎯 *Метод 5-4-3-2-1*\n\n"
            "5 предметов видишь 👀\n"
            "4 звука слышишь 👂\n"
            "3 поверхности чувствуешь ✋\n"
            "2 запаха 👃\n"
            "1 вкус 👅\n\n"
            "Дыши ровно. Тревога спадает волнами — подожди спад."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "when_call":
        txt = (
            "❗ *Когда вызывать скорую (103/112)*\n\n"
            "— Давящая боль в груди >5–10 мин, с иррадиацией в руку/челюсть/спину\n"
            "— Хрипы/свист, посинение губ, обморок, судороги\n"
            "— Травма, бред, подозрение на отравление\n\n"
            "Не уверен(а)? Лучше вызвать — безопасность важнее."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "info":
        txt = (
            "ℹ️ *Что происходит при панической атаке?*\n\n"
            "Организм ошибочно включает «тревогу».\n"
            "Учащается дыхание → головокружение, «ком в горле», покалывания — это _гипервентиляция_.\n"
            "Сердцебиение — не удушье. Цель — замедлить дыхание и вернуть внимание в тело."
        )
        await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb_home())
        return

    if data == "sos":
        geo_kb = ReplyKeyboardMarkup(
            [[KeyboardButton("📍 Отправить геолокацию", request_location=True)],
             [KeyboardButton("🏠 В меню")]],
            resize_keyboard=True, one_time_keyboard=True
        )
        await q.edit_message_text("Ожидаю геолокацию… (смотри кнопки ниже)", reply_markup=kb_home())
        await q.message.chat.send_message(
            "📞 *SOS / Геолокация*\n\n"
            "Шаблон для близкого:\n"
            "«У меня паническая атака. Нужна поддержка. Вот моя геолокация ниже.»",
            parse_mode="Markdown",
            reply_markup=geo_kb
        )
        return

    # ---- Метрономы ----
    if data == "metro_478":
        if context.user_data.get("metronome_task"):
            await q.edit_message_text("⏳ Метроном уже идёт. Нажми «⏹️ Стоп», чтобы остановить.", reply_markup=kb_stop())
            return
        phases = [("Вдох", 4), ("Задержка", 7), ("Выдох", 8)]
        context.application.create_task(
            run_metronome(context, q.message.chat_id, "Дыхание 4-7-8", phases, cycles=4)
        )
        await q.edit_message_text("▶️ Запускаю метроном 4-7-8…", reply_markup=kb_stop())
        return

    if data == "metro_square":
        if context.user_data.get("metronome_task"):
            await q.edit_message_text("⏳ Метроном уже идёт. Нажми «⏹️ Стоп», чтобы остановить.", reply_markup=kb_stop())
            return
        phases = [("Вдох", 4), ("Пауза", 4), ("Выдох", 4), ("Пауза", 4)]
        context.application.create_task(
            run_metronome(context, q.message.chat_id, "Дыхание «Квадрат» 4-4-4-4", phases, cycles=4)
        )
        await q.edit_message_text("▶️ Запускаю метроном «Квадрат»…", reply_markup=kb_stop())
        return

    if data == "metronome_stop":
        task = context.user_data.get("metronome_task")
        if task and not task.done():
            task.cancel()
            await q.edit_message_text("⏹️ Останавливаю метроном…", reply_markup=kb_home())
        else:
            await q.edit_message_text("Метроном не запущен.", reply_markup=kb_home())
        return

# ---------- Сообщения: геолокация и «В меню» ----------
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🏠 В меню":
        await update.message.reply_text("Главное меню:", reply_markup=kb_main())
        return

    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        url = f"https://maps.google.com/?q={lat},{lon}"
        txt = (
            "✅ Геолокация получена.\n"
            f"Координаты: {lat:.5f}, {lon:.5f}\n"
            f"🔗 {url}\n\n"
            "Отправь ссылку близкому или продиктуй диспетчеру 103/112."
        )
        await update.message.reply_text(txt)
        await update.message.reply_text("Вернуться в меню:", reply_markup=kb_main())
        return

# ---------- MAIN ----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.LOCATION | filters.TEXT, on_message))

    print("🚀 Паник-бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
