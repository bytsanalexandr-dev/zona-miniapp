import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logger = logging.getLogger(__name__)

WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://example.railway.app")

WELCOME_TEXT = (
    "⛓ <b>ЗОНА — Симулятор криминальной империи</b>\n\n"
    "От зека до хозяина мира.\n"
    "Нажми кнопку чтобы начать свой путь."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="🔱 Играть в ЗОНУ",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])
    await update.message.reply_html(WELCOME_TEXT, reply_markup=keyboard)


async def run_bot(token: str):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Bot polling started")
    await app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)


if __name__ == "__main__":
    import asyncio
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN env variable")
    asyncio.run(run_bot(token))
