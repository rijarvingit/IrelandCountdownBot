import os
import asyncio
from datetime import datetime
import pytz
import logging
from telegram import Bot
from telegram.error import TelegramError

# === CONFIGURATION SECTION ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Target time for the countdown (16th August 2025, 19:30 Dublin time)
TARGET_TIME = datetime(2025, 8, 16, 19, 30, tzinfo=pytz.timezone('Europe/Dublin'))

# Get bot token and group IDs from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [
    "-1002859929632",  # Active group for testing
    "-1002890597287",  # Commented out for now
]

# === MAIN COUNTDOWN FUNCTION ===
async def send_daily_update():
    """Send countdown message to all configured Telegram groups."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set")
        return
    if not GROUP_IDS or not GROUP_IDS[0]:
        logger.error("GROUP_IDS not set or empty")
        return

    bot = Bot(token=BOT_TOKEN)
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
            "_Next update in 24 hours_"
        )

    for chat_id in GROUP_IDS:
        try:
            sent_msg = await bot.send_message(chat_id=chat_id.strip(), text=message, parse_mode="Markdown")
            logger.info(f"Message sent to chat {chat_id}")
            try:
                await sent_msg.pin(disable_notification=True)
                logger.info(f"Message pinned in chat {chat_id}")
            except TelegramError as e:
                logger.warning(f"Pinning failed in chat {chat_id}: {e}")
        except TelegramError as e:
            logger.error(f"Failed to send message to chat {chat_id}: {e}")

if __name__ == "__main__":
    logger.info("Starting daily update...")
    asyncio.run(send_daily_update())
