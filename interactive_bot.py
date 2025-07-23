import os
import logging
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIGURATION SECTION ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Target time for the countdown (16th August 2025, 19:30 Dublin time)
TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === COUNTDOWN COMMAND ===
async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /countdown command - sends countdown message."""
    try:
        now = datetime.now(pytz.timezone('Europe/Dublin'))
        remaining = TARGET_TIME - now

        if remaining.total_seconds() <= 0:
            message = "🎉 The Ireland IST Expedition has begun! 🎉"
        else:
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            message = (
                "⏳ **Ireland IST Expedition Countdown** ⏳\n\n"
                f"🗓️ **{days} days**\n"
                f"🕒 **{hours} hours**\n"
                f"⏱️ **{minutes} minutes**\n\n"
                "_Test command triggered_"
            )

        sent_msg = await update.message.reply_text(message, parse_mode="Markdown")
        try:
            await sent_msg.pin(disable_notification=True)
            logger.info(f"Message pinned in chat {update.effective_chat.id}")
        except Exception as e:
            logger.warning(f"Pinning failed: {e}")
    except Exception as e:
        logger.error(f"Error in countdown: {e}")
        await update.message.reply_text("⚠️ Failed to update countdown")

# === BOT SETUP ===
def main():
    """Initialize and configure the bot application."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("countdown", countdown))
    app.run_polling()

# === ENTRY POINT ===
if __name__ == "__main__":
    logger.info("Starting interactive bot...")
    main()
