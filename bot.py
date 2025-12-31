import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEX = "https://api.dexscreener.com"

REF_LINK = "https://t.me/based_eth_bot?start=r_Elite_xyz_b_"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Elite Degen 🦅 is online!\n\nSend a Base token CA to scan."
    )

# Scan token
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Simple CA check
    if not (text.startswith("0x") and len(text) == 42):
        return

    token = text.lower()

    try:
        url = f"{DEX}/tokens/v1/base/{token}"
        r = requests.get(url, timeout=10)
        data = r.json()

        if not data:
            await update.message.reply_text("❌ Token not found on DexScreener")
            return

        pair = data[0]

        name = pair.get("baseToken", {}).get("name", "Unknown")
        price = pair.get("priceUsd", "N/A")
        liq = pair.get("liquidity", {}).get("usd", "N/A")
        paid = "🟢 Dex Paid" if pair.get("paid") else "🔴 Dex Not Paid"

        msg = (
            f"🦅 *Elite Degen Scan*\n\n"
            f"*Token:* {name}\n"
            f"*CA:* `{token}`\n"
            f"*Price:* ${price}\n"
            f"*Liquidity:* ${liq}\n"
            f"*Status:* {paid}"
        )

        keyboard = [
            [InlineKeyboardButton("Buy with BaseBot", url=f"{REF_LINK}{token}")]
        ]

        await update.message.reply_text(
            msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception:
        await update.message.reply_text("⚠️ DexScreener error, try again later.")

# App
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scan))

print("Elite Degen Bot running...")
app.run_polling()
