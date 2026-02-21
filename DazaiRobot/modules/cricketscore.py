"""
Advanced Cricket Score - Paged View
"""

import urllib.request
from bs4 import BeautifulSoup
from telethon import events, Button
from DazaiRobot import telethn as meow
from telethon.tl import functions, types


# -------------------------------
# ADMIN CHECK
# -------------------------------

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        participant = await meow(
            functions.channels.GetParticipantRequest(chat, user)
        )
        return isinstance(
            participant.participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )

    if isinstance(chat, types.InputPeerUser):
        return True


# -------------------------------
# FETCH SCORES
# -------------------------------

def fetch_scores():
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    matches = soup.find_all("description")

    match_list = []
    for match in matches:
        text = match.get_text()
        match_list.append(text)

    return match_list


# -------------------------------
# FORMAT MATCH VIEW
# -------------------------------

def format_match(match_text, page, total):
    return (
        f"🏏 <b>LIVE CRICKET SCORE</b>\n"
        f"────┈┄┄╌╌╌╌┄┄┈────\n\n"
        f"<code>{match_text}</code>\n\n"
        f"────┈┄┄╌╌╌╌┄┄┈────\n"
        f"📄 Page {page+1} / {total}"
    )


# -------------------------------
# COMMAND HANDLER
# -------------------------------

@meow.on(events.NewMessage(pattern=r"/(c|cs)$"))
async def cricket_score(event):
    if event.fwd_from:
        return

    if event.is_group:
        if not await is_register_admin(event.input_chat, event.sender_id):
            await event.reply(
                "🚨 Need Admin Power.. You can't use this command.. "
                "But you can use it in my PM."
            )
            return

    matches = fetch_scores()

    if not matches:
        await event.reply("❌ No live matches found.")
        return

    page = 0
    total = len(matches)

    buttons = []
    if total > 1:
        buttons = [
            [
                Button.inline("⬅️ Prev", data=f"score_{page-1}"),
                Button.inline("➡️ Next", data=f"score_{page+1}")
            ]
        ]

    await event.reply(
        format_match(matches[page], page, total),
        buttons=buttons,
        parse_mode="HTML"
    )


# -------------------------------
# CALLBACK HANDLER
# -------------------------------

@meow.on(events.CallbackQuery(pattern=r"score_"))
async def callback_pagination(event):
    matches = fetch_scores()
    total = len(matches)

    page = int(event.data.decode().split("_")[1])

    if page < 0:
        page = total - 1
    if page >= total:
        page = 0

    buttons = []
    if total > 1:
        buttons = [
            [
                Button.inline("⬅️ Prev", data=f"score_{page-1}"),
                Button.inline("➡️ Next", data=f"score_{page+1}")
            ]
        ]

    await event.edit(
        format_match(matches[page], page, total),
        buttons=buttons,
        parse_mode="HTML"
    )


__mod_name__ = "Cricket Score 🏏"

__help__ = """
*Cricket Score - Advanced View*
 ❍ `/c` : View live cricket scores (paged)
 ❍ `/cs` : View live cricket scores (paged)
"""
