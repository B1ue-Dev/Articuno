import interactions
import os, logging, utils.file_sending
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")
google_cloud = os.getenv("GOOGLE_CLOUD")
google_cse = os.getenv("GOOGLE_CSE")

#logging.basicConfig(level=logging.DEBUG)



bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.ALL,
	presence=interactions.ClientPresence(
		activities=[
			interactions.PresenceActivity(
				type=interactions.PresenceActivityType.WATCHING,
				name="for v4.0.1"
			),
		],
		status=interactions.StatusType.ONLINE,
	),
	#disable_sync=True
)
bot.load('utils.cache')

#bot.load('exts.automod')
#bot.load('exts.basic')
@bot.load('exts.emoji')
#bot.load('exts.fun')
#bot.load('exts.hacktool')
#bot.load('exts.info')
#bot.load('exts.logs')
#bot.load('exts.menus')
#bot.load('exts.misc')
#bot.load('exts.mod')
#bot.load('exts.pokemon')
#bot.load('exts.snipe')
#bot.load('exts.tag')



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print(f'Logged in as {bot.me.name}')
	print(f'ID: {bot.me.id}')
	print(f'Latency: {websocket}ms')
	await bot.change_presence(
		interactions.ClientPresence(
			activities=[
				interactions.PresenceActivity(
					type=interactions.PresenceActivityType.WATCHING,
					name="for v4.0.1"
				)
			],
			status=interactions.StatusType.ONLINE,
		)
	)







bot.start()
