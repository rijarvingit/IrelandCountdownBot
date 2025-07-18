from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import pytz
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Target time: 16th August 2025, 19:30 Dublin time
TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Securely loaded from GitHub Secrets

async def send_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the countdown message and schedule the next update."""
    try:
        now = datetime.now(pytz.timezone('Europe/Dublin'))
        remaining = TARGET_TIME - now
        
        if remaining.total_seconds() <= 0:
            await update.message.reply_text("🎉 The Ireland IST Expedition has begun! 🎉")
            return
        
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        message = (
            "⏳ **Ireland IST Expedition Countdown** ⏳\n\n"
            f"🗓️ **{days} days**\n"
            f"🕒 **{hours} hours**\n"
            f"⏱️ **{minutes} minutes**\n"
            f"⏲️ **{seconds} seconds**\n\n"
            "_Next update in 24 hours_"
        )
        
        await update.message.reply_text(message, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error sending update: {e}")

def main():
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("countdown", send_update))
    app.run_polling()

if __name__ == "__main__":
    main()
