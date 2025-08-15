#!/usr/bin/env python3
"""
ireland_countdown_bot.py

Purpose:
- Send a daily Telegram countdown message to one or more group chats.

Key behaviors:
- Reads BOT_TOKEN from environment (GitHub Actions secret).
- Uses a fixed TARGET_TIME in a chosen timezone (use tz.localize for correctness).
- No pinning (pin code kept but commented out).
- Designed to be triggered daily by GitHub Actions at 09:00 Switzerland time (Europe/Zurich).
  NOTE: Scheduling is done in the workflow YAML (cron in UTC).
"""

import os
import asyncio
from datetime import datetime
import logging
import pytz
from telegram import Bot
from telegram.error import TelegramError

# === Logging Setup ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("countdown_bot")

# === Timezones ===
# Event timezone:
# - If your event is in Australia (e.g., Sydney), set TZ_EVENT to Australia/Sydney.
# - If your event is in Ireland, set TZ_EVENT to Europe/Dublin.
# - Always use tz.localize(...) when constructing TARGET_TIME with pytz.
TZ_EVENT = pytz.timezone("Australia/Sydney")   # Change if needed: "Europe/Dublin", etc.

# Local ops / log timezone:
# - We log using Switzerland local time for clarity around the 09:00 daily run.
TZ_CH = pytz.timezone("Europe/Zurich")

# === Target Event Date/Time ===
# Example: 11 Nov 2025 at 19:30 in the EVENT timezone.
# Adjust as needed. Always use tz.localize with pytz to handle DST correctly.
TARGET_TIME = TZ_EVENT.localize(datetime(2025, 11, 11, 19, 30))

# === Telegram Config ===
# BOT_TOKEN must be provided via environment variable (e.g., GitHub Actions secret).
BOT_TOKEN = os.getenv("BOT_TOKEN")

# List your chat/group IDs here (strings). Negative IDs are supergroups/channels.
GROUP_IDS = [
    "-1002859929632",  # Tiina and Riku
    # Add more IDs on their own lines if needed
]

# === Message Templates ===
MSG_STARTED = "🎉 Australia Tour Countdown has begun! 🎉"
MSG_HEADER = "⏳ **Australia Tour Countdown** ⏳\n\n"
MSG_FOOTER = "_Next update in 24 hours_"

# === Helper: Compose Countdown Text ===
def build_countdown_message(now_event_tz: datetime) -> str:
    """Return a Markdown-formatted countdown message."""
    remaining = TARGET_TIME - now_event_tz
    if remaining.total_seconds() <= 0:
        return MSG_STARTED

    days = remaining.days
    hours, rem = divmod(remaining.seconds, 3600)
    minutes, _ = divmod(rem, 60)

    # Keep hours/minutes commented to keep the message short; easy to re-enable.
    body = (
        f"🗓️ **{days} days**\n"
        # f"🕒 **{hours} hours**\n"
        # f"⏱️ **{minutes} minutes**\n"
    )
    return f"{MSG_HEADER}{body}\n{MSG_FOOTER}"

# === Main Send Function ===
async def send_daily_update() -> None:
    """
    Sends the countdown message to all GROUP_IDS.
    Notes:
    - This function does not schedule itself; run it daily at 09:00 CH via GitHub Actions.
    - Pinning is intentionally disabled (left in comments for easy re-enable).
    """
    # Basic validations
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set in environment")
        return
    if not GROUP_IDS:
        logger.error("GROUP_IDS is empty; nothing to send")
        return

    bot = Bot(token=BOT_TOKEN)

    # Log current times in both event TZ and Switzerland TZ for transparency
    now_event = datetime.now(TZ_EVENT)
    now_ch = datetime.now(TZ_CH)
    logger.info(
        "Preparing countdown message | Event time now: %s | CH time now: %s",
        now_event.strftime("%Y-%m-%d %H:%M:%S %Z"),
        now_ch.strftime("%Y-%m-%d %H:%M:%S %Z"),
    )

    message = build_countdown_message(now_event)

    # Send to each configured chat
    for chat_id in GROUP_IDS:
        chat_id = str(chat_id).strip()
        if not chat_id:
            continue
        try:
            sent_msg = await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown"
            )
            logger.info("Message sent to chat %s", chat_id)

            # === Pinning disabled by request (kept for future use) ===
            # try:
            #     await sent_msg.pin(disable_notification=True)
            #     logger.info("Message pinned in chat %s", chat_id)
            # except TelegramError as e:
            #     logger.warning("Pinning failed in chat %s: %s", chat_id, e)

        except TelegramError as e:
            logger.error("Failed to send message to chat %s: %s", chat_id, e)

# === Entrypoint ===
if __name__ == "__main__":
    logger.info("Starting daily update (designed for 09:00 CH via GitHub Actions)...")
    asyncio.run(send_daily_update())
