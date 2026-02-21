import random
import urllib.parse
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from DazaiRobot import pbot


@pbot.on_message(filters.command(["wall", "wallpaper"]))
async def wall(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("✨ Give me something to search.\nExample: `/wall anime`")

    query = " ".join(message.command[1:])
    await message.reply_text("🔍 Searching HD wallpaper...")

    # Encode query safely
    encoded = urllib.parse.quote(query)

    # Unsplash random image source (no API key needed)
    image_url = f"https://source.unsplash.com/1920x1080/?{encoded}"

    try:
        await message.reply_photo(
            photo=image_url,
            caption=f"🖼 **Wallpaper for:** `{query}`\n\n🥀 Requested by: {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔗 Open Image", url=image_url)]
                ]
            ),
        )
    except Exception:
        await message.reply_text(f"❌ No wallpaper found for `{query}`.")