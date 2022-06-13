"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import os
import interactions
from interactions.ext.wait_for import setup
from const import TOKEN


client = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT,
    # disable_sync=False # Uncomment this if you want to disable the synchronization process.
)
setup(client)


client.load("utils.cache")
client.load("interactions.ext.files")

[client.load(f"exts.{ext}") for ext in [file.replace(".py", "") for file in os.listdir('exts') if not file.startswith("_")]]


@client.event
async def on_ready():
    websocket = f"{client.latency * 1:.0f}"
    print("Ready!")
    print(f"Latency: {websocket}ms")


client.start()
