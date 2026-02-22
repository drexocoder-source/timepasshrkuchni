import logging
import sys
import time
import asyncio

from aiohttp import ClientSession
from Python_ARQ import ARQ
from pyrogram import Client
from telethon import TelegramClient
import telegram.ext as tg

from DazaiRobot.config import *
from DazaiRobot.globals import DEMONS, DEV_USERS, DRAGONS, TIGERS, WOLVES

StartTime = time.time()

# ───────────── LOGGING ─────────────
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)

if sys.version_info < (3, 7):
    LOGGER.error("Python 3.7+ required.")
    sys.exit(1)

# ───────────── BOT CLIENTS ─────────────
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
dispatcher = updater.dispatcher

telethn = TelegramClient("Dazai", API_ID, API_HASH)
pbot = Client(
    "DazaiRobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)

aiohttpsession = None
arq = None

async def init_async():
    global aiohttpsession, arq
    aiohttpsession = ClientSession()
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
    LOGGER.info("ARQ client initialized")

async def shutdown_async():
    if aiohttpsession:
        await aiohttpsession.close()

print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

# ───────────── PATCH HANDLERS ─────────────
from DazaiRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

# ───────────── STARTUP ─────────────
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_async())

    LOGGER.info("Starting Telethon...")
    telethn.start(bot_token=TOKEN)

    LOGGER.info("Starting Pyrogram...")
    pbot.start()

    LOGGER.info("Starting Polling...")
    updater.start_polling(drop_pending_updates=True)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info("Shutting down...")
    finally:
        loop.run_until_complete(shutdown_async())
        pbot.stop()
        telethn.disconnect()
        updater.stop()
        loop.close()
