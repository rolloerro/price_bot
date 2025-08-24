import telebot
TOKEN = "8411928903:AAHvbnpukpJIXFVCUvu-pkJGwmDREwYRFko"
bot = telebot.TeleBot(TOKEN)
updates = bot.get_updates(offset=-1)
print("Очередь обновлений очищена")
