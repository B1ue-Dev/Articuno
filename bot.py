import interactions
from interactions.ext import wait_for
import os, datetime, logging
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")
scope = int(os.getenv("SCOPE"))

#logging.basicConfig(level=logging.DEBUG)



bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.ALL,
	presence=interactions.ClientPresence(
		activities=[
			interactions.PresenceActivity(
				type=interactions.PresenceActivityType.WATCHING,
				name="you. 👀"
			),
		],
		status=interactions.StatusType.IDLE,
	),
	disable_sync=True
)

"""
Main cogs.
"""
#bot.load('Cogs.basic')
#bot.load('Cogs.fun')
#bot.load('Cogs.hacktool')
#bot.load('Cogs.info')
#bot.load('Cogs.logger')
#bot.load('Cogs.menus')
#bot.load('Cogs.misc')
bot.load('Cogs.mod')
#bot.load('Cogs.tag')

"""
Test cogs.
"""
bot.load('interactions.ext.enhanced')
#bot.load('Cogs.get_method')
#bot.load('test')




@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print(f'Logged in as {bot.me.name}')
	print(f'ID: {bot.me.id}')
	print(f'Latency: {websocket}ms')
"""
@bot.command(name="test", description="Why?", scope=scope)
async def test(ctx: interactions.CommandContext):
		e = interactions.Embed(
			fields=[
				interactions.EmbedField(
					name='Test',
					value=f'{bot.me.icon_url}',
				)
			],
			timestamp=str(datetime.datetime.utcnow()),
			footer=interactions.EmbedFooter(
				icon_url=bot.me.icon_url,
				text=f'{bot.me.name}'
			),
			thumbnail=interactions.EmbedImageStruct(url=bot.me.icon_url)._json,
		)
		await ctx.send(embeds=e)
"""


bot.start()