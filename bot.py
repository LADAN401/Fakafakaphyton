
import telebot
import os
import time
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN missing")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# -------- TOOL LOGIC -------- #

def decode_swap(text: str):
    """
    Very simple offline intent decoder
    Example input:
    Swapped 1.2 ETH for 2500 ABC
    """

    pattern = r"swapped\s+([\d\.]+)\s+(\w+)\s+for\s+([\d\.]+)\s+(\w+)"
    match = re.search(pattern, text.lower())

    if not match:
        return None

    amount_in, token_in, amount_out, token_out = match.groups()

    return {
        "amount_in": amount_in,
        "token_in": token_in.upper(),
        "amount_out": amount_out,
        "token_out": token_out.upper()
    }

# -------- BOT COMMANDS -------- #

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🛠 Swap Intent Decoder (Demo)\n\n"
        "Send a message like:\n"
        "`Swapped 1.2 ETH for 2500 ABC`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    decoded = decode_swap(message.text)

    if not decoded:
        bot.reply_to(
            message,
            "❌ Could not decode message\n"
            "Try:\n"
            "`Swapped 1.2 ETH for 2500 ABC`",
            parse_mode="Markdown"
        )
        return

    reply = (
        "🔴 *Swap Detected*\n\n"
        f"• Sent: `{decoded['amount_in']} {decoded['token_in']}`\n"
        f"• Received: `{decoded['amount_out']} {decoded['token_out']}`\n\n"
        "⚠️ Demo decoder (no blockchain API)"
    )

    bot.reply_to(message, reply, parse_mode="Markdown")

print("🤖 Swap Intent Decoder Bot started")

# Keep alive (Bothost-safe)
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
