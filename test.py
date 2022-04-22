"""
import interactions
from interactions import extension_command as command
from interactions import CommandContext
import random, os, io, aiohttp
from dotenv import load_dotenv

load_dotenv()
scope = int(os.getenv("SCOPE"))


async def get_response(url: str = None, params: dict = None):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params) as resp:
			if resp.status == 200:
				if resp.content_type == "application/json":
					return await resp.json()
				elif resp.content_type == "image/png":
					return io.BytesIO(await resp.read())


class Misc(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	

	@command(
		name="test",
		description="Test",
		scope=scope,
	)
	async def hornycard(self, ctx: interactions.CommandContext):
		embed = interactions.Embed(
			title="Test",
			fields=[
				interactions.EmbedField(name="Test", value="test"),
			],
			color=0xC98FFC
		)
		embed.set_author(name=f"{ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=ctx.author.user.avatar_url)
		embed.set_thumbnail(url=ctx.author.user.avatar_url)
		await ctx.send(content=f"{ctx.author.mention}",embeds=embed)





def setup(bot):
	Misc(bot)
"""

# Convert ts into json from a file
import json
data = json.loads(open("./data/pokemon.json", "r").read())
inp = str(input("Name: "))
inp = inp.lower()
if inp in data:
	name = data[inp]['name']
	types = str(data[inp]['types'])
	types = types.replace("'","")
	types = types.replace("[","")
	types = types.replace("]","")
	hp = data[inp]['baseStats']['hp']
	atk = data[inp]['baseStats']['atk']
	defe = data[inp]['baseStats']['def']
	spa = data[inp]['baseStats']['spa']
	spd = data[inp]['baseStats']['spd']
	spe = data[inp]['baseStats']['spe']
	stats = f"HP: {hp}  Atk: {atk}  Def: {defe}  SpA: {spa}  SpD: {spd}  Spe: {spe}"
	num = len(data[inp]['abilities'])
	dct = data[inp]['abilities']
	a = list(dct.keys())
	#for i in range(num - 1):
	#	anp = data[inp]['abilities'][f'{i}']
	print(f"Name: {name}\nTypes: {types}\n{stats}\n{a}")
else:
	print("Not found.")

