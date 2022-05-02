import interactions
from interactions import Intents, Client
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")



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
