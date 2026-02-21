import secureme
from telethon import events
from DazaiRobot.events import register

# ─────────────────────────────
# ⚡ GOJO ENCRYPT
# ─────────────────────────────

@register(pattern="^/encrypt(?: |$)(.*)")
async def gojo_encrypt(event):
    text = None

    # If replying to message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply and reply.text:
            text = reply.text
    else:
        text = event.pattern_match.group(1)

    if not text:
        return await event.reply(
            "⚡ ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ!\n\n"
            "➤ ᴜsᴀɢᴇ:\n"
            "/encrypt <text>\n"
            "ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ."
        )

    try:
        encrypted = secureme.encrypt(text)
        await event.reply(
            f"🔐 Ꮐᴏᴊᴏ ᴇɴᴄʀʏᴘᴛɪᴏɴ\n"
            f"`{encrypted}`"
        )
    except Exception as e:
        await event.reply("❌ ᴇɴᴄʀʏᴘᴛɪᴏɴ ғᴀɪʟᴇᴅ.")


# ─────────────────────────────
# ⚡ GOJO DECRYPT
# ─────────────────────────────

@register(pattern="^/decrypt(?: |$)(.*)")
async def gojo_decrypt(event):
    text = None

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply and reply.text:
            text = reply.text
    else:
        text = event.pattern_match.group(1)

    if not text:
        return await event.reply(
            "⚡ ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ!\n\n"
            "➤ ᴜsᴀɢᴇ:\n"
            "/decrypt <text>\n"
            "ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴇɴᴄʀʏᴘᴛᴇᴅ ᴍᴇssᴀɢᴇ."
        )

    try:
        decrypted = secureme.decrypt(text)
        await event.reply(
            f"🔓 Ꮐᴏᴊᴏ ᴅᴇᴄʀʏᴘᴛɪᴏɴ\n"
            f"`{decrypted}`"
        )
    except Exception:
        await event.reply("❌ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴄᴏʀʀᴜᴘᴛᴇᴅ ᴇɴᴄʀʏᴘᴛᴇᴅ ᴛᴇxᴛ.")

import math
import re

from telegram import Update, ParseMode
from telegram.ext import CommandHandler
from DazaiRobot import dispatcher


# ─────────────────────────────
# ⚡ SAFE CALCULATOR ENGINE
# ─────────────────────────────

SAFE_DICT = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "abs": abs,
    "round": round,
}


def safe_eval(expression):
    # Replace ^ with **
    expression = expression.replace("^", "**")

    # Allow only safe characters
    if not re.match(r"^[0-9+\-*/().,% eipowabsqrtlogtantcos]+$", expression.replace(" ", "")):
        return None

    return eval(expression, {"__builtins__": None}, SAFE_DICT)


# ─────────────────────────────
# ⚡ /calc COMMAND
# ─────────────────────────────
@register(pattern="^/calc(?: |$)(.*)")
def calc(update: Update, context):
    message = update.effective_message

    if not context.args:
        return message.reply_text("⚡ Usage: /calc 25*(4+6)")

    expression = " ".join(context.args)

    try:
        result = safe_eval(expression)

        if result is None:
            raise ValueError

        message.reply_text(
            f"⚡ <b>{expression}</b> = <code>{result}</code>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception:
        message.reply_text("❌ Invalid mathematical expression.")



# ─────────────────────────────

__mod_name__ = "𝙏𝙤𝙤𝙡𝙨"

__help__ = """
⚡ Ꮐᴏᴊᴏ ᴛᴏᴏʟs

❍ /calc <expression>
❍ /encrypt — ᴇɴᴄʀʏᴘᴛ ᴛᴇxᴛ  
❍ /decrypt — ᴅᴇᴄʀʏᴘᴛ ᴛᴇxᴛ  

ʀᴇᴘʟʏ ᴏʀ ᴘᴀss ᴛᴇxᴛ ᴀғᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ.
"""