from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import pytz
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def send_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send countdown and shut down gracefully."""
    try:
        now = datetime.now(pytz.timezone('Europe/Dublin'))
        remaining = TARGET_TIME - now
        
        if remaining.total_seconds() <= 0:
            message = "🎉 The Ireland IST Expedition has begun! 🎉"
        else:
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            message = (
                "⏳ **Ireland IST Expedition Countdown** ⏳\n\n"
                f"🗓️ **{days} days**\n"
                f"🕒 **{hours} hours**\n"
                f"⏱️ **{minutes} minutes**\n"
                f"⏲️ **{seconds} seconds**\n\n"
                "_Next update tomorrow_"
            )
        
        await update.message.reply_text(message, parse_mode="Markdown")
        
    finally:
        # Shut down the bot after sending the message
        await context.application.shutdown()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("countdown", send_update))
    
    # Run until shutdown is triggered
    app.run_polling()

if __name__ == "__main__":
    main()
