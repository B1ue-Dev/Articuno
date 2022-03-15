import interactions
from interactions import Intents, Client
import json, asyncio



with open('./data/config.json') as bot_data:
	data = json.load(bot_data)
	bot_token = data['TOKEN']


bot = Client(token=bot_token,
				intents=Intents.DEFAULT,
				disable_sync=False
)



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Ready!')
	print(f'Latency: {websocket}ms')





bot.start()
