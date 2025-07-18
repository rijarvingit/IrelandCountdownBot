from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import pytz
import os
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def send_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        now = datetime.now(pytz.timezone('Europe/Dublin'))
        remaining = TARGET_TIME - now
        
        if remaining.total_seconds() <= 0:
            message = "🎉 The Ireland IST Expedition has begun! 🎉"
        else:
            days, seconds = remaining.days, remaining.seconds
            hours, minutes = seconds // 3600, (seconds % 3600) // 60
            
            message = (
                "⏳ *Ireland IST Expedition Countdown*\n\n"
                f"🗓️ *{days} days*\n🕒 *{hours} hours*\n"
                f"⏱️ *{minutes} minutes*\n\n"
                f"_Updated: {now.strftime('%Y-%m-%d %H:%M')}_"
            )
        
        # Send and attempt to pin
        sent_msg = await update.message.reply_text(message, parse_mode="Markdown")
        try:
            await sent_msg.pin(disable_notification=True)
            logger.info("Message pinned successfully")
        except Exception as e:
            logger.warning(f"Pinning failed (ensure bot has pin permissions): {e}")
            await update.message.reply_text("⚠️ Note: Couldn't pin this update (check bot permissions)")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("🚨 Failed to update countdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("countdown", send_update))
    app.run_polling()

if __name__ == "__main__":
    main()
