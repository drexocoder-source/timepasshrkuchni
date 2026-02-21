from pyrogram import filters
import requests
from DazaiRobot import pbot

@pbot.on_message(filters.command('latest'))
def schedule(_, message):
    try:
        results = requests.get(
            'https://subsplease.org/api/?f=schedule&h=true&tz=Japan',
            timeout=10
        ).json()
    except Exception:
        message.reply_text("Failed to fetch schedule. Try again later.")
        return

    lines = []
    for result in results.get('schedule', []):
        title = result['title']
        time = result['time']
        aired = bool(result['aired'])
        link = f"https://subsplease.org/shows/{result['page']}"

        if aired:
            title = f"~~[{title}]({link})~~"
        else:
            title = f"[{title}]({link})"

        lines.append(f"**{title}** - **{time}**")

    text = "\n".join(lines)
    final = f"**Today's Schedule:**\nTime-Zone: Tokyo (GMT +9)\n\n{text}"

    # Telegram hard limit protection
    if len(final) > 4000:
        final = final[:4000] + "\n..."

    message.reply_text(final, disable_web_page_preview=True)

__mod_name__ = "sᴄʜᴇᴅᴜʟᴇ"

__help__ = """
 ❍ `/latest`: to see latest anime episode
"""
