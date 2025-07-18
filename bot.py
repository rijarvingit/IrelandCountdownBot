from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import pytz
import os
import logging

# === CONFIGURATION SECTION ===
# Set up basic logging to track bot activity
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Target time for the countdown (16th August 2025, 19:30 Dublin time)
TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))

# Get bot token from environment variables (set in GitHub Secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === TEMPORARY GROUP ID FETCHER ===
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Temporary command to fetch group ID
    Usage: Send /getid in any chat to see its ID
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🔍 Chat Information:\n"
        f"ID: `{chat_id}`\n"
        f"Type: {update.effective_chat.type}\n"
        f"Title: {getattr(update.effective_chat, 'title', 'N/A')}",
        parse_mode="Markdown"
    )

# === MAIN COUNTDOWN FUNCTION ===
async def send_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /countdown command - calculates time remaining and sends formatted message
    """
    try:
        # Get current time in Dublin timezone
        now = datetime.now(pytz.timezone('Europe/Dublin'))
        remaining = TARGET_TIME - now
        
        # Prepare message based on whether event has started
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
                "_Next update in 24 hours_"
            )
        
        # Send and pin the message
        sent_msg = await update.message.reply_text(message, parse_mode="Markdown")
        try:
            await sent_msg.pin(disable_notification=True)
            logger.info(f"Message pinned in chat {update.effective_chat.id}")
        except Exception as e:
            logger.warning(f"Pinning failed: {e}")

    except Exception as e:
        logger.error(f"Error in send_update: {e}")
        await update.message.reply_text("⚠️ Failed to update countdown")

# === BOT SETUP ===
def main():
    """Initialize and configure the bot application"""
    # Create Application instance with your bot token
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("getid", get_id))      # Temporary ID fetcher
    app.add_handler(CommandHandler("countdown", send_update))  # Main functionality
    
    # Start the bot in polling mode
    app.run_polling()

# === ENTRY POINT ===
if __name__ == "__main__":
    # This block runs when executing the script directly
    logger.info("Starting bot application...")
    main()
