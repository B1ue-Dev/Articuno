import interactions
from interactions import *
from interactions import extension_listener as listener


class Logs(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot
    

    @listener
    async def on_message_create(self, message):
        await ctx.send(f"{message.content}")
