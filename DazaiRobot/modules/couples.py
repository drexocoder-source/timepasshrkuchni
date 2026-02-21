import random
import time
from telegram import Update, ParseMode
from telegram.ext import CommandHandler
from DazaiRobot import dispatcher

# ─────────────────────────────
# STORAGE (12H RESET)
# ─────────────────────────────

COUPLE_DB = {}  # {chat_id: {"pair": (id1, id2), "time": timestamp}}
COOLDOWN = 60 * 60 * 12  # 12 hours

GOJO_IMAGE = "https://graph.org/file/2735689fc11a2a52bcca1-7908d1df4682dba93f.jpg"  # change to your telegraph image


# ─────────────────────────────
# COUPLES COMMAND
# ─────────────────────────────

def couples(update: Update, context):
    chat = update.effective_chat
    message = update.effective_message
    bot = context.bot

    if chat.type not in ["group", "supergroup"]:
        return message.reply_text("This command works only in groups.")

    chat_id = chat.id
    current_time = time.time()

    # If already selected and not expired
    if chat_id in COUPLE_DB:
        data = COUPLE_DB[chat_id]
        if current_time - data["time"] < COOLDOWN:
            user1_id, user2_id = data["pair"]

            user1 = bot.get_chat_member(chat_id, user1_id).user
            user2 = bot.get_chat_member(chat_id, user2_id).user

            remaining = int(COOLDOWN - (current_time - data["time"]))
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60

            caption = (
                "ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\n\n"
                f"💞 ᴛᴏᴅᴀʏ's ᴄᴏᴜᴘʟᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʜᴏsᴇɴ\n\n"
                f"💙 <a href='tg://user?id={user1.id}'>{user1.first_name}</a>\n"
                f"❤️ <a href='tg://user?id={user2.id}'>{user2.first_name}</a>\n\n"
                f"⏳ ʀᴇsᴇᴛ ɪɴ {hours}ʜ {minutes}ᴍ"
            )

            return bot.send_photo(
                chat_id,
                GOJO_IMAGE,
                caption=caption,
                parse_mode=ParseMode.HTML
            )

    # Collect active members from administrators + message sender
    members = []

    try:
        for admin in bot.get_chat_administrators(chat_id):
            if not admin.user.is_bot:
                members.append(admin.user.id)

        # include command user
        if not update.effective_user.is_bot:
            members.append(update.effective_user.id)

    except:
        return message.reply_text("I couldn't fetch members.")

    members = list(set(members))

    if len(members) < 2:
        return message.reply_text("Not enough members to select a couple.")

    user1_id, user2_id = random.sample(members, 2)

    COUPLE_DB[chat_id] = {
        "pair": (user1_id, user2_id),
        "time": current_time
    }

    user1 = bot.get_chat_member(chat_id, user1_id).user
    user2 = bot.get_chat_member(chat_id, user2_id).user

    caption = (
        "㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ!\n\n"
        "💘 ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ 💘\n\n"
        f"💙 <a href='tg://user?id={user1.id}'>{user1.first_name}</a>\n"
        f"❤️ <a href='tg://user?id={user2.id}'>{user2.first_name}</a>\n\n"
        "✨ ʙᴏɴᴅ ᴠᴀʟɪᴅ ғᴏʀ 12 ʜᴏᴜʀs ✨\n\n"
        "◉ ɢᴏᴊᴏ ᴅᴇᴄʀᴇᴇs ɪᴛ!"
    )

    bot.send_photo(
        chat_id,
        GOJO_IMAGE,
        caption=caption,
        parse_mode=ParseMode.HTML
    )


# ─────────────────────────────
# REGISTER HANDLER
# ─────────────────────────────

COUPLES_HANDLER = CommandHandler("couples", couples, run_async=True)
dispatcher.add_handler(COUPLES_HANDLER)


__mod_name__ = "𝘾𝙤𝙪𝙥𝙡𝙚𝙨"

__help__ = """
💘 /couples

Randomly selects 2 group members as Couple Of The Day.
Valid for 12 hours.
"""