import asyncio
import urllib.parse
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message
from DazaiRobot import pbot
import random
import time
from pyrogram import filters
from pyrogram.types import Message
from DazaiRobot import pbot

# ─────────────────────────────
# 💙 STORAGE
# ─────────────────────────────

WAIFU_DB = {}  
# {chat_id: {user_id: {"waifu": target_id, "time": timestamp}}}

COOLDOWN = 60 * 60 * 12  # 12 hours


# ─────────────────────────────
# 💙 WAIFU COMMAND
# ─────────────────────────────

@pbot.on_message(filters.command("waifu") & filters.group)
async def waifu(_, message: Message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    current_time = time.time()

    if chat_id not in WAIFU_DB:
        WAIFU_DB[chat_id] = {}

    # Check cooldown
    if user_id in WAIFU_DB[chat_id]:
        data = WAIFU_DB[chat_id][user_id]
        if current_time - data["time"] < COOLDOWN:
            remaining = int(COOLDOWN - (current_time - data["time"]))
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            waifu_user = await pbot.get_users(data["waifu"])

            return await message.reply_photo(
                photo=waifu_user.photo.big_file_id if waifu_user.photo else None,
                caption=(
                    "ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\n"
                    f"💍 ʏᴏᴜʀ ᴡᴀɪꜰᴜ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ!\n"
                    f"💙 {waifu_user.mention}\n"
                    f"⏳ ʀᴇsᴇᴛ ɪɴ {hours}ʜ {minutes}ᴍ"
                )
            )

    # Fetch group members (recent participants)
    members = []
    async for member in pbot.get_chat_members(chat_id):
        if not member.user.is_bot and member.user.id != user_id:
            members.append(member.user.id)

    if len(members) < 1:
        return await message.reply_text("Not enough members to assign waifu.")

    target_id = random.choice(members)

    WAIFU_DB[chat_id][user_id] = {
        "waifu": target_id,
        "time": current_time
    }

    waifu_user = await pbot.get_users(target_id)

    caption = (
        "ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\n"
        "㋡ ɪ ʜᴀᴠᴇ ᴄʜᴏsᴇɴ ʏᴏᴜʀ ᴡᴀɪꜰᴜ ғᴏʀ ᴛʜᴇ ɴᴇxᴛ 12 ʜᴏᴜʀs!\n"
        f"💘 {message.from_user.mention} 💞 {waifu_user.mention}\n"
        "✨ ʙᴏɴᴅ ᴠᴀʟɪᴅ ғᴏʀ 12 ʜᴏᴜʀs ✨"
    )

    if waifu_user.photo:
        await message.reply_photo(
            photo=waifu_user.photo.big_file_id,
            caption=caption
        )
    else:
        await message.reply_text(caption)


