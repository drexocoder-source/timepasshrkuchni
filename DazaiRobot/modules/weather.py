import io
import aiohttp

from telethon import events
from DazaiRobot.events import register


# ─────────────────────────────
# 🌤 WEATHER MODULE (Gojo Stable Version)
# ─────────────────────────────

import aiohttp
from DazaiRobot.events import register


@register(pattern=r"^/weather(?: |$)(.*)")
async def weather_func(event):
    if event.fwd_from:
        return

    city = event.pattern_match.group(1).strip()

    if not city:
        return await event.reply("🌤 Usage: /weather <city>\nExample: /weather Delhi")

    url = f"https://wttr.in/{city}?format=3"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": "curl"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:

                if resp.status != 200:
                    return await event.reply("❌ City not found.")

                result = await resp.text()

        await event.reply(f"🌤 `{result}`")

    except Exception as e:
        await event.reply("⚠️ Failed to fetch weather. Try again later.")
# ─────────────────────────────

__mod_name__ = "Wᴇᴀᴛʜᴇʀ"

__help__ = """
🌤 ᴡᴇᴀᴛʜᴇʀ ᴍᴏᴅᴜʟᴇ

• /weather <city>
• /weather moon  → Moon phase

Example:
 /weather Delhi
"""