import interactions
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")



bot = interactions.Client(token=bot_token,
	intents=interactions.Intents.DEFAULT,
	#disable_sync=False
)


bot.load('exts.basic')


@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Ready!')
	print(f'Latency: {websocket}ms')





bot.start()
