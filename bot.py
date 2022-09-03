"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from interactions.ext.wait_for import setup
from const import TOKEN, VERSION

# logging.basicConfig(level=logging.DEBUG)

client = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.WATCHING, name=f"for {VERSION}"
            )
        ],
        status=interactions.StatusType.ONLINE,
    ),
    # disable_sync=True,
)
setup(client)
client.load("interactions.ext.files")
client.load("utils.cache")
client.load("utils.error")
client.load("exts.core.__init__")
client.load("exts.server.__init__")
client.load("exts.fun.__init__")
client.load("exts.utils.__init__")


@client.event
async def on_ready():
    """Fires up READY"""
    websocket = f"{client.latency * 1:.0f}"
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    logging.debug(
        """[%s] Logged in as %s. Latency: %sms.""", log_time, client.me.name, websocket
    )
    print(f"""[{log_time}] Logged in as {client.me.name}. Latency: {websocket}ms.""")


client.start()
