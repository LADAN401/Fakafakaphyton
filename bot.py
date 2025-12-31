import telebot
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN is missing")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello World 👋")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Bot is alive ✅")

print("🤖 Bot started")

# Keep bot alive (important for Bothost)
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
