import interactions
from interactions import Intents, Client
import os
bot_token = os.environ['TOKEN']



bot = Client(token=bot_token,
				intents=Intents.DEFAULT,
				disable_sync=False
)


bot.load('Cogs.basic')


@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Ready!')
	print(f'Latency: {websocket}ms')





bot.start()
