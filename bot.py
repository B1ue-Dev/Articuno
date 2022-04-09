import interactions
from interactions.ext import wait_for
import os, datetime
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")
scope = int(os.getenv("SCOPE"))



bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.DEFAULT | interactions.Intents.PRIVILEGED,
	disable_sync=True
)
#bot.load('Cogs.admin')
#bot.load('Cogs.basic')
#bot.load('Cogs.fun')
#bot.load('Cogs.hacktool')
#bot.load('Cogs.logs')
#bot.load('Cogs.menus')
bot.load('Cogs.tag')
#bot.load('Cogs.test')



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Ready!')
	print(f'Latency: {websocket}ms')
	message = bot._http.get_message
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