import interactions
from interactions import *
from interactions import extension_command as command
from interactions.ext import wait_for
import os, asyncio, json
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))

with open ("./test.json") as f:
	data = json.load(f)
	ids = data['ID']



class Test(Extension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)
	

	@command(
		name="page",
		description="A page test",
		scope=scope
	)
	async def test(self, ctx: CommandContext):
		page = 0
		buttons = [
			Button(
				style=ButtonStyle.PRIMARY,
				label="►",
				custom_id="next"
			)
		]
		msg: CommandContext = await ctx.send(content=f"This is page {page} ||You will see this again||", components = buttons)
		while True:
			try:
				res = await self.bot.wait_for_component(components=buttons, messages = int(msg.id), timeout = 8)
				footer = interactions.EmbedFooter(text="test", icon_url=self.bot.me.icon_url)
				page += 1
				await res.edit(embeds=interactions.Embed(title=f"Page {page}", description=f"This is page {page}", color=0x000000, footer=footer))
			except asyncio.TimeoutError:
				await msg.edit(components=[])
				break
	#TODO:
	"""
	
	"""
def setup(bot):
	Test(bot)
