#!/usr/bin/env python3
"""
Run this script LOCALLY (not on Heroku) to generate your STRING_SESSION.
Copy the printed string and paste it into Heroku Config Vars as STRING_SESSION.

Usage:
    pip install telethon
    python generate_session.py
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID   = 35057620
API_HASH = "010824c75f6d2116f660933cf4536d20"


async def main():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        print("\n✅ STRING_SESSION generated successfully!\n")
        print("Copy everything between the lines below:\n")
        print("─" * 60)
        print(client.session.save())
        print("─" * 60)
        print("\nPaste it into Heroku → Settings → Config Vars → STRING_SESSION\n")


if __name__ == "__main__":
    asyncio.run(main())
