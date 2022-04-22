import interactions
from interactions import extension_command as command
import aiohttp, json, os, io
from dotenv import load_dotenv
from interactions.ext.enhanced import (
	extension_command,
	EnhancedExtension,
	option
)

load_dotenv()
scope = int(os.getenv("SCOPE"))
apikey = os.getenv("APIKEY")


async def get_response(url: str = None, params: dict = None):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params) as resp:
			if resp.status == 200:
				if resp.content_type == "application/json":
					return await resp.json()
				elif resp.content_type in {"image/png", "image/jpeg", "image/gif"}:
					return io.BytesIO(await resp.read())
	await session.close()




class Pokemon(EnhancedExtension):
	def __init__(self, bot):
		self.bot = bot


	@extension_command(
		name="pokemon",
		description="Show the information about a Pokemon",
		scope=scope	
	)
	@option(str, "name", "Name of the Pokemon")
	async def pokemon(self, ctx: interactions.CommandContext,
		name: str
	):
		url = "https://some-random-api.ml/pokedex"
		params = {
			"pokemon": name
		}
		resp = await get_response(url, params)
		with open("./data/pokemon.json") as f:
			data = json.load(f)
			name = name.lower()
			if name in data:
				name = data[name]['name']
				num = data[name]['num']
				desp = resp['description']
				types = str(data[name]['types'])
				types = types.replace("'", "")
				types = types.replace("[", "")
				types = types.replace("]", "")
				hp = data[name]['baseStats']['hp']
				atk = data[name]['baseStats']['atk']
				defe = data[name]['baseStats']['def']
				spa = data[name]['baseStats']['spa']
				spd = data[name]['baseStats']['spd']
				spe = data[name]['baseStats']['spe']
				stats = "Hp: {}\nAtk: {}\nDef: {}\nSp.Atk: {}\nSp.Def: {}\nSpe: {}".format(hp, atk, defe, spa, spd, spe)
				abilities = str(resp[abilities])
				abilities = abilities.replace("'", "")
				abilities = abilities.replace("[", "")
				abilities = abilities.replace("]", "")
				gen = int(resp[generation])
		author = interactions.EmbedFooter(text=f"ID: {num} • First introduced in Generation {gen}")
		fields = [
			interactions.EmbedField(name="Stats", value=stats, inline=True),
			interactions.EmbedField(name="Abilities", value=abilities, inline=True)
		]
		embed = interactions.Embed(
			title=f"{name}",
			description=f"{desp}",
			author=author,
			fields=fields
		)
		await ctx.send(embeds=embed)








def setup(bot):
	Pokemon(bot)
