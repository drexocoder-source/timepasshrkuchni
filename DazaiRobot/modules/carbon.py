from pyrogram import filters

from DazaiRobot import pbot
from DazaiRobot.utils.errors import capture_err
from DazaiRobot.utils.functions import make_carbon

import asyncio

@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if message.reply_to_message and message.reply_to_message.text:
        txt = message.reply_to_message.text
    else:
        try:
            txt = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("Reply or give text.")

    m = await message.reply_text("Generating carbon...")

    loop = asyncio.get_running_loop()
    carbon = await loop.run_in_executor(None, make_carbon, txt)

    await m.edit_text("Uploading...")
    await pbot.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"» Requested by: {message.from_user.mention}",
    )
    await m.delete()
    carbon.close()


__mod_name__ = "Cᴀʀʙᴏɴ"

__help__ = """
ᴍᴀᴋᴇs ᴀ ᴄᴀʀʙᴏɴ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ.

❍ /carbon *:* ᴍᴀᴋᴇs ᴄᴀʀʙᴏɴ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.
"""
