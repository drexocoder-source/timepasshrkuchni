import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext

from DazaiRobot import BOT_NAME, BOT_USERNAME, dispatcher
from DazaiRobot.modules.disable import DisableAbleCommandHandler

def handwrite(update: Update, context: CallbackContext):
    message = update.effective_message

    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        if len(context.args) == 0:
            return message.reply_text("Give me some text to write ✍️")
        text = " ".join(context.args)

    m = message.reply_text("Writing the text... ✍️")

    try:
        api_url = f"https://apis.xditya.me/write?text={text}"

        message.reply_photo(
            photo=api_url,
            caption=f"""
Successfully Written Text 💘

✨ **Written By :** [{BOT_NAME}](https://t.me/{BOT_USERNAME})
🥀 **Requested by :** {update.effective_user.first_name}
❄ **Link :** `{api_url}`""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• ᴏᴘᴇɴ ɪᴍᴀɢᴇ •", url=api_url),
                    ],
                ]
            ),
        )

    except Exception as e:
        message.reply_text("Failed to write text. Try again later.")

    m.delete()


__help__ = """
 Writes the given text on white page with a pen 🖊

❍ /write <text> *:*Writes the given text.
"""

WRITE_HANDLER = DisableAbleCommandHandler("write", handwrite, run_async=True)
dispatcher.add_handler(WRITE_HANDLER)

__mod_name__ = "WʀɪᴛᴇTᴏᴏʟ"

__command_list__ = ["write"]
__handlers__ = [WRITE_HANDLER]
