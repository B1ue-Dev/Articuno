"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import logging
import asyncio
import interactions
from interactions.ext.wait_for import setup
from utils import cache
from const import TOKEN, VERSION
from status import WebSocketClient

# logging.basicConfig(level=logging.DEBUG)


bot = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.ALL,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.WATCHING,
                name=f"for {VERSION}"
            )
        ],
        status=interactions.StatusType.ONLINE
    )
)
bot._websocket = WebSocketClient(TOKEN, bot._intents)
setup(bot)
bot.load('utils.cache')
bot.load('interactions.ext.files')

bot.load('exts.automod')
bot.load('exts.basic')
bot.load('exts.emoji')
bot.load('exts.eval')
bot.load('exts.fun')
bot.load('exts.hacktool')
bot.load('exts.hug')
bot.load('exts.info')
bot.load('exts.logs')
bot.load('exts.menus')
bot.load('exts.misc')
bot.load('exts.mod')
bot.load('exts.pokemon')
bot.load('exts.snipe')
# bot.load('exts.tag')
bot.load('exts.tts')


@bot.event
async def on_ready():
    global _ON_READY_TRIGGER
    await asyncio.sleep(2)
    _set_user_count: set = set()
    _set_guild_count: set = set()
    for guild in cache.__cached__:
        _set_guild_count.add(guild)
        for member in cache.__cached__[guild]:
            _set_user_count.add(member)
    user_count = len(_set_user_count)
    guild_count = len(_set_guild_count)
    websocket = f"{bot.latency * 1:.0f}"
    print(f'Logged in as {bot.me.name}')
    print(f'ID: {bot.me.id}')
    print(f'Latency: {websocket}ms')
    print(f'Connected to {guild_count} guilds with {user_count} users')


bot.start()
