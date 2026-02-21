# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# PROVIDED BY https://t.me/ProjectCodeX

# IMPORTS
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#DazaiRobot => Your Bots File Name
import DazaiRobot.modules.sql.users_sql as sql
from DazaiRobot import DEV_USERS, OWNER_ID, pbot as pgram
from DazaiRobot.modules.sql.users_sql import get_all_users

# get_arg function to retrieve an argument from a message
def get_broadcast_text(message):
    parts = message.text.split()
    return " ".join([p for p in parts[1:] if not p.startswith("-")])

# Broadcast Function
@pgram.on_message(filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    texttt = message.text.split(" ")

    ALLOWED_USERS = {OWNER_ID} | DEV_USERS

    if user_id not in ALLOWED_USERS:
        return await message.reply_text("You are not authorized.")

    if len(texttt) < 2:
        return await message.reply_text(
            "<b>BROADCASTING COMMANDS</b>\n"
            "-user : users\n"
            "-group : groups\n"
            "-all : both\n"
            "Reply to a message or use: /broadcast -user hello"
        )

    tex = await message.reply_text("<code>Starting global broadcast...</code>")

    usersss = chatttt = uerror = cerror = 0
    chats = sql.get_all_chats() or []
    users = get_all_users()

    if "-all" in texttt:
        texttt.extend(["-user", "-group"])

    reply_msg = message.reply_to_message
    text_msg = get_broadcast_text(message)

    if not reply_msg and not text_msg:
        return await message.reply_text("Reply to a message or give text.")

    # USERS
    if "-user" in texttt:
        for chat in users:
            try:
                if reply_msg:
                    await reply_msg.copy(chat.user_id)
                else:
                    await client.send_message(chat.user_id, text_msg)
                usersss += 1
                await asyncio.sleep(0.3)
            except Exception:
                uerror += 1

    # GROUPS
    if "-group" in texttt:
        for chat in chats:
            try:
                if reply_msg:
                    await reply_msg.copy(chat.chat_id)
                else:
                    await client.send_message(chat.chat_id, text_msg)
                chatttt += 1
                await asyncio.sleep(0.3)
            except Exception:
                cerror += 1

    await tex.edit_text(
        f"<b>Broadcast Finished</b>\n\n"
        f"Users: {usersss}\nFailed: {uerror}\n\n"
        f"Groups: {chatttt}\nFailed: {cerror}"
    )
