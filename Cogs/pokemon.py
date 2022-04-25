import interactions
from interactions import extension_command as command
import aiohttp, json, os, io
from dotenv import load_dotenv
from interactions.ext.enhanced import (
	extension_command,
	EnhancedExtension,
	option,
	ext_subcommand_base
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

	base = ext_subcommand_base("pokedex", scope=scope)

	@base.subcommand(
		name="search",
		description="Show the information about a Pokemon"
	)
	@option(
		type=interactions.OptionType.STRING,
		name="name",
		autocomplete=True
	)
	async def pokemon(self, ctx: interactions.CommandContext,
		name: str
	):
		name_lower = name.lower()
		url = "https://some-random-api.ml/pokedex"
		params = {
			"pokemon": name
		}
		resp = await get_response(url, params)
		desp = resp['description']
		gen = resp['generation']
		id = resp['id']
		abilities = str(resp['abilities'])
		abilities = abilities.replace("'", "")
		abilities = abilities.replace("[", "")
		abilities = abilities.replace("]", "")
		evs = int(resp['family']['evolutionStage'])
		if evs != 0:
			evs = str(resp['family']['evolutionLine'])
			evs = evs.replace("'", "")
			evs = evs.replace("[", "")
			evs = evs.replace("]", "")
		else:
			evs = None
		height = resp['height']
		weight = resp['weight']
		sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"
		data = json.loads(open("./data/pokemon.json", "r").read())
		if name_lower in data:
			name = data[name_lower]['name']
			types = str(data[name_lower]['types'])
			types = types.replace("'","")
			types = types.replace("[","")
			types = types.replace("]","")
			hp = data[name_lower]['baseStats']['hp']
			atk = data[name_lower]['baseStats']['atk']
			defe = data[name_lower]['baseStats']['def']
			spa = data[name_lower]['baseStats']['spa']
			spd = data[name_lower]['baseStats']['spd']
			spe = data[name_lower]['baseStats']['spe']
			stats = "**HP:** {}\n**Attack:** {}\n**Defense:** {}\n**Special Attack:** {}\n**Special Defense:** {}\n**Speed:** {}".format(hp, atk, defe, spa, spd, spe)
			egg_group = str(data[name_lower]['eggGroups'])
			egg_group = egg_group.replace("'","")
			egg_group = egg_group.replace("[","")
			egg_group = egg_group.replace("]","")
			footer = interactions.EmbedFooter(text="First introduced in Generation {}".format(gen), icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png")._json
			thumbnail = interactions.EmbedImageStruct(url=sprites_url_still)._json
			fields = [
				interactions.EmbedField(name="Information", value=f"**Entry:** {id}\n**Type(s):** {types}\n**Abilities:** {abilities}\n**Egg Groups:** {egg_group}\n**Height:** {height}\n**Weight:** {weight}", inline=True),
				interactions.EmbedField(name="Stats", value=stats, inline=True)
			]
			embed = interactions.Embed(
				title=f"{name}",
				description=f"{desp}",
				footer=footer,
				thumbnail=thumbnail,
				fields=fields,
			)
			if evs is not None:
				embed.add_field(name="Evolution Line", value=evs, inline=True)
			await ctx.send(embeds=embed)
		else:
			await ctx.send("Pokemon not found.")


	base.finish()


	@base.autocomplete("name")
	async def auto_complete(self, ctx:interactions.CommandContext, name: str = ""):
		if name != "":
			letters: list = name
		else:
			letters = []
		data = json.loads(open("./data/pokemon.json", "r").read())
		if len(name) == 0:
			await ctx.populate(
				[
					interactions.Choice(
						name=name[0].capitalize(), value=name[0].capitalize()) for name in (
							list(data.items())[0:9] if len(data) > 10 else list(data.items()
						)
					)
				]
			)
		else:
			choices: list = []
			for pkmn_name in data:
				focus: str = "".join(letters)
				if focus.lower() in pkmn_name and len(choices) < 20:
					choices.append(interactions.Choice(name=pkmn_name.capitalize(), value=pkmn_name.capitalize()))
			await ctx.populate(choices)



	@interactions.extension_listener(name="on_message_create")
	async def message_create(self, message: interactions.Message):
		channel = await message.get_channel()
		if message.content.startswith("$shiny"):
			ends = int(len(message.content) - 7)
			msg = str(message.content)[-ends:].lower()
			data = json.loads(open("./data/pokemon.json", "r").read())
			if msg in data:
				img = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{msg}.gif"
				embed = interactions.Embed(
					image=interactions.EmbedImageStruct(url=img)._json
				)
				await channel.send(embeds=embed)
			return

		elif message.content.startswith("$"):
			ends = int(len(message.content) - 1)
			msg = str(message.content)[-ends:].lower()
			data = json.loads(open("./data/pokemon.json", "r").read())
			if msg in data:
				img = f"https://play.pokemonshowdown.com/sprites/ani/{msg}.gif"
				embed = interactions.Embed(
					image=interactions.EmbedImageStruct(url=img)._json
				)
				await channel.send(embeds=embed)
			return






def setup(bot):
	Pokemon(bot)
