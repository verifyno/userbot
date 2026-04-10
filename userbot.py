#!/usr/bin/env python3
"""
Telegram Userbot — Heroku Deployment
Logs in with your own Telegram account and sets your profile
name to: pairing [custom emoji 6170209141953403618]
"""

import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.sessions import StringSession

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Credentials (loaded from Heroku Config Vars) ───────────────────────────────
API_ID      = int(os.environ["API_ID"])
API_HASH    = os.environ["API_HASH"]
# STRING_SESSION is generated once locally and stored as a Heroku config var
# so the bot never needs an interactive login on the server.
STRING_SESSION = os.environ["STRING_SESSION"]

# ── Custom emoji ───────────────────────────────────────────────────────────────
EMOJI_ID = 6170209141953403618

def custom_emoji_tag(emoji_id: int) -> str:
    return f'<tg-emoji emoji-id="{emoji_id}">⚡</tg-emoji>'


# ── Main ───────────────────────────────────────────────────────────────────────
async def main():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        logger.error("Session is invalid or expired. Please regenerate STRING_SESSION.")
        return

    me = await client.get_me()
    logger.info("Logged in as: %s (id=%s)", me.username or me.first_name, me.id)

    # Change profile name on every startup
    new_name = f"pairing {custom_emoji_tag(EMOJI_ID)}"
    await client(UpdateProfileRequest(first_name=new_name))
    logger.info("Profile name updated → pairing [custom emoji]")

    # ── Event handlers (extend here) ──────────────────────────────────────────

    @client.on(events.NewMessage(incoming=True))
    async def on_message(event):
        # Basic logger — remove or replace with your own logic
        logger.info("New message from %s: %s", event.sender_id, event.raw_text[:80])

    # ── Keep alive ────────────────────────────────────────────────────────────
    logger.info("Userbot is running.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
