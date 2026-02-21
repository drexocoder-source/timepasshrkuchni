import urllib.parse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext

from DazaiRobot import BOT_NAME, dispatcher
from DazaiRobot.modules.disable import DisableAbleCommandHandler


def handwrite(update: Update, context: CallbackContext):
    message = update.effective_message

    # Get text from reply or args
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    else:
        if not context.args:
            return message.reply_text("✍️ Give me some text to write.")
        text = " ".join(context.args)

    # URL encode text (important fix)
    encoded_text = urllib.parse.quote_plus(text)
    api_url = f"https://apis.xditya.me/write?text={encoded_text}"

    wait = message.reply_text("✍️ Writing your text...")

    try:
        message.reply_photo(
            photo=api_url,
            caption=(
                f"✨ *Handwritten Successfully*\n\n"
                f"🖋 Requested by: *{update.effective_user.first_name}*\n"
                f"🤍 Powered by: *{BOT_NAME}*"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📄 Open Image",
                            url=api_url
                        )
                    ]
                ]
            ),
        )
    except Exception:
        message.reply_text("❌ Failed to generate handwritten image.")
    finally:
        wait.delete()


__help__ = """
✍️ *Write Tool*

• /write <text>
• Reply to a message with /write

Creates a handwritten styled image.
"""

WRITE_HANDLER = DisableAbleCommandHandler("write", handwrite)
dispatcher.add_handler(WRITE_HANDLER)

__mod_name__ = "WriteTool"
__command_list__ = ["write"]
__handlers__ = [WRITE_HANDLER]