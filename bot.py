"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import logging
import json
import asyncio
import requests
import interactions
from interactions.ext.wait_for import setup
from interactions.ext.tasks import IntervalTrigger, create_task
from utils import cache
from const import TOKEN, VERSION
from status import WebSocketClient

logging.basicConfig(level=logging.DEBUG)


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
bot.load('exts.tag')
bot.load('exts.tts')

_ON_READY_TRIGGER = 0


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

    if _ON_READY_TRIGGER == 0:
        url = "https://json.psty.io/api_v1/stores/backup"
        headers = {
            "Api-Key": "2f44b242-76ca-4129-b55e-7910078d6930",
            "Content-Type": "application/json"
        }
        resp = requests.get(url, headers=headers)
        with open('./db/tag.json', 'w', encoding='utf8') as cont:
            json.dump(resp.json()['data'], cont, indent=4)
        _ON_READY_TRIGGER = 1
    else:
        pass

    await bot.change_presence(
        interactions.ClientPresence(
            activities=[
                interactions.PresenceActivity(
                    type=interactions.PresenceActivityType.WATCHING,
                    name=f"for {VERSION}"
                )
            ],
            status=interactions.StatusType.ONLINE
        )
    )


@create_task(IntervalTrigger(1800))  # Trigger this task every 30 minutes
async def _back_up():
    url = "https://json.psty.io/api_v1/stores/backup"
    headers = {
        "Api-Key": "2f44b242-76ca-4129-b55e-7910078d6930",
        "Content-Type": "application/json"
    }
    with open('./db/tag.json', 'r', encoding='utf8') as cont:
        tag = json.load(cont)
        requests.put(url, headers=headers, data=json.dumps(tag))


_back_up.start()
bot.start()
