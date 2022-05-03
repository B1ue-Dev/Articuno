import interactions
from interactions.ext import wait_for
import os, datetime, logging, io
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")
scope = int(os.getenv("SCOPE"))

#logging.basicConfig(level=logging.DEBUG)



bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.DEFAULT | interactions.Intents.PRIVILEGED,
	presence=interactions.ClientPresence(
		activities=[
			interactions.PresenceActivity(
				type=interactions.PresenceActivityType.WATCHING,
				name="for v4.0.0a"
			),
		],
		status=interactions.StatusType.IDLE,
	),
	#disable_sync=True
)

"""
Main cogs.
"""
bot.load('exts.automod')
#bot.load('exts.basic')
#bot.load('exts.fun')
#bot.load('exts.hacktool')
#bot.load('exts.info')
bot.load('exts.logs')
#bot.load('exts.menus')
#bot.load('exts.misc')
#bot.load('exts.mod')
#bot.load('exts.pokemon')
#bot.load('exts.tag')

"""
Test cogs.
"""
#bot.load('interactions.ext.enhanced')
#bot.load('Cogs.get_method')
#bot.load('test')



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print(f'Logged in as {bot.me.name}')
	print(f'ID: {bot.me.id}')
	print(f'Latency: {websocket}ms')

"""
@bot.command(name="test", description="AAAAAAAAAAAAAAAAAAAAAAA", scope=scope)
async def test(ctx: interactions.CommandContext):
	
	data = "AAAAAAAAAAAAAAAAAAAAAAAAAA"
	with io.StringIO(data) as f:
		file = interactions.File(filename="aaaaa.txt", fp=f)
		await ctx.send(files=file)
	
	#await ctx.send("AAAAAAAAAAAAAAAAAAAAAAAAA!")
"""




bot.start()
