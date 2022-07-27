"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from interactions.ext.wait_for import setup
from const import TOKEN, VERSION, EXT_CORE
from status import WebSocketClient

# logging.basicConfig(level=logging.DEBUG)

client = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT
    | interactions.Intents.GUILD_MEMBERS
    | interactions.Intents.GUILD_MESSAGE_CONTENT
    | interactions.Intents.GUILD_PRESENCES,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.WATCHING, name=f"for {VERSION}"
            )
        ],
        status=interactions.StatusType.ONLINE,
    ),
)
client._websocket = WebSocketClient(TOKEN, client._intents)
setup(client)
client.load("interactions.ext.files")
client.load("utils.cache")

# [client.load(f"exts.core.{ext}") for ext in EXT_CORE]
client.load("exts.fun.whos_that_pokemon")


@client.event
async def on_ready():
    """Fires up READY"""
    websocket = f"{client.latency * 1:.0f}"
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
    logging.debug("""[%s] Logged in as %s. Latency: %sms.""", log_time, client.me.name, websocket)
    print(f"""[{log_time}] Logged in as {client.me.name}. Latency: {websocket}ms.""")


client.start()
