import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand, ComponentContext, http
from discord_slash.http import SlashCommandRequest
from discord_slash.utils.manage_components import (
	create_button,
	create_actionrow,
	create_select,
	create_select_option,
	wait_for_component,
)
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.context import InteractionContext, MenuContext
from discord_slash.utils.manage_commands import create_option, create_choice
import asyncio
from asyncio import TimeoutError
import urllib, os, requests, random, aiohttp, utils, io
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("APIKEY")
google_cloud = os.getenv("GOOGLE_CLOUD")
google_cse = os.getenv("GOOGLE_CSE")



# Color
red = 0xff0000
orange = 0xff7100
yellow = 0xfbff00
green = 0x1a7c37
blue = 0x0025fa
purple = 0x5c00fa
brown = 0xc4771d

# As again, lazy
subcommand = cog_ext.cog_subcommand
slash = cog_ext.cog_slash


class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@slash(
		name="coffee",
		description="Get a coffee",
	)
	async def _coffee(self, ctx: SlashContext):
		response = requests.get('https://coffee.alexflipnote.dev/random.json')
		data = response.json()
		embed = discord.Embed(title="Coffee ☕", color=brown)
		embed.set_image(url=data['file'])
		await ctx.send(embed=embed)

	@slash(
		name="ship",
		description="Ship two people",
	)
	async def _ship(self,
					ctx: SlashContext,
					user1: str = None,
					user2: str = None):
		shipnumber = int(random.randint(0, 100))
		if not user1:
			user1 = ctx.author.name
			user_2 = random.choice(ctx.guild.members)
			user2 = user_2.name
		if not user2:
			user_1 = user1
			user2 = user_1
			user1 = ctx.author.name
		# Choose comment and heart emoji
		if 0 <= shipnumber <= 30:
			comment = "Really low! {}".format(
				random.choice([
					'Friendzone.', 'Just "friends".',
					'There is barely any love.',
					'I sense a small bit of love!',
					'Still in that friendzone ;(', 'No, just no!',
					'But there is a small sense of romance from one person!'
				]))
			heart = ":broken_heart:"
		elif 31 <= shipnumber <= 70:
			comment = "Moderate! {}".format(
				random.choice([
					'Fair enough!', 'A small bit of love is in the air...',
					'I feel like there is some romance progressing!',
					'I am starting to feel some love!',
					'At least this is acceptable.', '...',
					'I sense a bit of potential!',
					'But it is very one-sided OwO.'
				]))
			heart = ":mending_heart:"
		elif 71 <= shipnumber <= 90:
			comment = "Almost perfect! {}".format(
				random.choice([
					'I definitely can see that love is in the air.',
					'I feel the love! There is a sign of a match!',
					'A few things can be imporved to make this a match made in heaven!',
					'I can definitely feel the love.',
					'This has a big potential.',
					'I can see the love is there! Somewhere...'
				]))
			heart = random.choice([
				':revolving_hearts:', ':heart_exclamation:', ':heart_on_fire:',
				':heartbeat:'
			])
		elif 90 < shipnumber <= 100:
			comment = "True love! {}".format(
				random.choice([
					'It is a match!', 'There is a match made in heaven!',
					'It is definitely a match!', 'Love is truely in the air!',
					'Love is most definitely in the air!'
				]))
			heart = random.choice([
				':sparkling_heart:', ':heart_decoration:', ':hearts:',
				':two_hearts:', ':heartpulse:'
			])
		# Choose color
		if shipnumber <= 40:
			shipColor = 0xE80303
		elif 41 < shipnumber < 80:
			shipColor = 0xff6600
		else:
			shipColor = 0x3be801
		embed = discord.Embed(
			title="Love test for: ",
			description=f"**{user1}** and **{user2}** {heart}",
			color=shipColor)
		embed.add_field(name="Results:",
						value=f"{shipnumber}%  {comment}",
						inline=True)
		embed.set_author(name="Shipping", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@slash(
		name="roll",
		description="Roll a dice",
	)
	async def _roll(self, ctx: SlashContext):
		dice = [1, 2, 3, 4, 5, 6]
		number = random.choice(dice)
		msg = await ctx.send("I am rolling the dice now!")
		await asyncio.sleep(2.5)
		await msg.edit(content=f"The number is {number}.")

	@slash(
		name="flip",
		description="Flip a coin",
	)
	async def _flip(self, ctx: SlashContext):
		flip = ['heads', 'tails']
		number = random.choice(flip)
		msg = await ctx.send("I am flipping the coin now!")
		await asyncio.sleep(2.5)
		await msg.edit(content=f"The coin landed on {number}.")

	@slash(
		name="hug",
		description="Hug someone",
		options=[
			create_option(name="user",
						  description="The user to hug",
						  option_type=6,
						  required=True)
		],
	)
	async def _hug(self, ctx: SlashContext, user: str):
		apikey = "YPQ8IU0W2DBT"
		limit = 50
		search_term = ['anime hug', 'cute panda hug', 'cute anime hug']
		search_term = random.choice(search_term)
		choice = random.randint(1, 50)
		try:
			r = requests.get(
				f'https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit={limit}'
			)
			data = r.json()
			gif = data['results'][choice]['media'][0]['gif']['url']
			embed = discord.Embed(
				description=f"{ctx.author.name} hugged {user.name}",
				color=0x3be801)
			embed.set_image(url=gif)
			await ctx.send(embed=embed)
		except:
			r = requests.get(f'https://some-random-api.ml/animu/hug')
			data = r.json()
			gif = data['link']
			embed = discord.Embed(
				description=f"{ctx.author.name} hugged {user.name}",
				color=0x3be801)
			embed.set_image(url=gif)
			await ctx.send(embed=embed)

	@slash(
		name="joke",
		description="Send a joke",
	)
	async def _joke(self, ctx: SlashContext):
		response = requests.get('https://some-random-api.ml/joke')
		data = response.json()
		joke = data['joke']
		embed = discord.Embed(description=joke,
							  color=random.randint(0, 0xFFFFFF))
		await ctx.send(embed=embed)

	@slash(
		name="quote",
		description="Send a quote",
	)
	async def _quote(self, ctx: SlashContext):
		await ctx.defer()
		r = requests.get('https://api.quotable.io/random')
		data = r.json()
		quote = data['content']
		author = data['author']
		added_date = data['dateAdded']
		embed = discord.Embed(title=f"Here is a quote", color=0xffc0cb)
		embed.add_field(name=f"From {author}", value=f"{quote}")
		embed.set_footer(text=f"Added on {added_date}")
		await ctx.send(embed=embed)

	@slash(
		name="xkcd",
		description="Send a xkcd comic",
	)
	async def _xkcd(self, ctx: SlashContext, number: str = None):
		if not number:
			number = random.randint(1, 2574)
			r = requests.get(f'https://xkcd.com/{number}/info.0.json')
			data = r.json()
			num = data['num']
			month = data['month']
			year = data['year']
			title = data['title']
			alt = data['alt']
			day = data['day']
			img = data['img']
			embed = discord.Embed(title=f"{title} - {alt}",
								  description=f"Created on {month}, {year}",
								  color=random.randint(0, 0xFFFFFF))
			embed.set_image(url=img)
			embed.set_footer(text=f"Day {day}, ID: {num}")
			await ctx.send(embed=embed)
		else:
			r = requests.get(f'https://xkcd.com/{number}/info.0.json')
			data = r.json()
			num = data['num']
			month = data['month']
			year = data['year']
			title = data['title']
			alt = data['alt']
			day = data['day']
			img = data['img']
			embed = discord.Embed(title=f"{title} - {alt}",
								  description=f"Created on {month}, {year}",
								  color=random.randint(0, 0xFFFFFF))
			embed.set_image(url=img)
			embed.set_footer(text=f"Day {day}, ID: {num}")
			await ctx.send(embed=embed)

	@slash(
		name="hornycard",
		description="Send a hornycard",
		options=[
			create_option(name="user",
						  description="Targetted user",
						  option_type=6,
						  required=False)
		],
	)
	async def _hornycard(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author
		await ctx.defer()
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://some-random-api.ml/canvas/horny?avatar={user.avatar_url_as(format="png", size=1024)}'
			) as trigImg:
				imageData = io.BytesIO(await trigImg.read())
				await session.close()
				await ctx.send(file=discord.File(imageData, 'image.png'))

	@slash(
		name="simpcard",
		description="Send a simpcard",
		options=[
			create_option(name="user",
						  description="Targetted user",
						  option_type=6,
						  required=False)
		],
	)
	async def _simpcard(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author
		await ctx.defer()
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://some-random-api.ml/canvas/simpcard?avatar={user.avatar_url_as(format="png", size=1024)}'
			) as trigImg:
				imageData = io.BytesIO(await trigImg.read())
				await session.close()
				await ctx.send(file=discord.File(imageData, 'image.png'))

	@slash(
		name="tweet",
		description="Send a tweet",
		options=[
			create_option(name="user",
						  description="Targetted user",
						  option_type=6,
						  required=True),
			create_option(name="comment",
						  description="Comment",
						  option_type=3,
						  required=True)
		],
	)
	async def _tweet(self, ctx: SlashContext, user: str, comment: str):
		number1 = random.randint(0, 100)
		await ctx.defer()
		if len(user.name) > 15:
			name = user.name[:12] + "..."
		else:
			name = user.name
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://some-random-api.ml/canvas/tweet/?avatar={user.avatar_url_as(format="png", size=1024)}&username={name}&displayname={name}&comment={comment}&replies={number1}&theme=dark'
			) as trigImg:
				imageData = io.BytesIO(await trigImg.read())
				await session.close()
				await ctx.send(file=discord.File(imageData, 'image.png'))

	@slash(
		name="youtube",
		description="Send a youtube comment",
		options=[
			create_option(name="user",
						  description="Targetted user",
						  option_type=6,
						  required=True),
			create_option(name="comment",
						  description="Comment",
						  option_type=3,
						  required=True)
		],
	)
	async def _youtube(self, ctx: SlashContext, user: str, comment: str):
		await ctx.defer()
		name = len(user.name)
		if name > 15:
			name = user.name[:12] + "..."
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://some-random-api.ml/canvas/youtube-comment?avatar={user.avatar_url_as(format="png", size=1024)}&username={user.name}&displayname={user.name}&comment={comment}'
			) as trigImg:
				imageData = io.BytesIO(await trigImg.read())
				await session.close()
				await ctx.send(file=discord.File(imageData, 'image.png'))

	@slash(
		name="amogus",
		description="Amogus",
		options=[
			create_option(name="user",
						  description="Targetted user",
						  option_type=6,
						  required=True)
		],
	)
	async def _amogus(self, ctx: SlashContext, user: str = None):
		choice = 'true', 'false'
		sus = random.choice(choice)
		await ctx.defer()
		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://some-random-api.ml/premium/amongus?avatar={user.avatar_url_as(format="png", size=1024)}&username={user.name}&key={key}&imposter={sus}'
			) as trigImg:
				imageData = io.BytesIO(await trigImg.read())
				await session.close()
				await ctx.send(file=discord.File(imageData, 'amogus.gif'))

	@slash(
		name="gay",
		description="Calculate the gay percentage of a user",
	)
	async def _gay(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author.name
		number = random.randint(0, 100)
		embed = discord.Embed(color=random.randint(0, 0xFFFFFF))
		embed.add_field(name=f"Gay measure tool",
						value=f"**{user}** is {number}% gay.")
		await ctx.send(embed=embed)

	@slash(name="ai",
		   description="Chat with Articuno",
		   options=[
			   create_option(name="message",
							 description="Message you want to say",
							 option_type=3,
							 required=True)
		   ])
	async def _ai(self, ctx: SlashContext, message: str):
		try:
			url = "https://random-stuff-api.p.rapidapi.com/ai"
			querystring = {
				"msg": message,
				"bot_name": "Articuno",
				"bot_gender": "male",
				"bot_master": "Blue"
			}
			headers = {
				'authorization':
				"nhdoHbSSw3c0",
				'x-rapidapi-host':
				"random-stuff-api.p.rapidapi.com",
				'x-rapidapi-key':
				"aad44bed6dmshba8fa4c3f4d92c2p118235jsne1aae4f19e3f"
			}
			response = requests.request("GET",
										url,
										headers=headers,
										params=querystring)
			data = response.json()
			msg = data['AIResponse']
			await ctx.send(msg)
		except:
			async with aiohttp.ClientSession() as aiSession:
				async with aiSession.get(
						f'https://some-random-api.ml/chatbot?message={message}&key={key}'
				) as response:
					data = await response.json()
					reply = data['response']
					await aiSession.close()
					await ctx.send(reply)

	@slash(
		name="dictionary",
		description="Define a word",
	)
	async def _dictionary(self, ctx: SlashContext, word: str):
		async with aiohttp.ClientSession() as dictionarySession:
			async with dictionarySession.get(
					f'https://some-random-api.ml/dictionary?word={word}'
			) as response:
				data = await response.json()
				try:
					er = data['error']
					await ctx.send(f"Error: {er}. Please try again.",
								   hidden=True)
				except:
					term = data['word']
					defi = data['definition']
					if len(defi) > 4096:
						defi = defi[:4000] + "..."
					embed = discord.Embed(title=f"Definition of {term}",
										  description=defi,
										  color=0x000000)
					await ctx.send(embed=embed)

	@slash(name="pokemon",
		   description="Show the infomation about a specific Pokemon")
	async def _pokemon(self, ctx: SlashContext, pokemon):
		async with aiohttp.ClientSession() as session:
			response = await session.get(
				f'https://some-random-api.ml/pokedex?pokemon={pokemon}')
			if str(response.status) == "404":
				await ctx.send(
					"I could not find that pokemon. Please try again.",
					hidden=True)
			else:
				rj = await response.json()
				name = (rj['name']).capitalize()
				pid = (rj['id'])
				ptype = (rj['type'])
				desc = (rj['description'])
				species = (rj['species'])
				stats = (rj['stats'])
				evolfam = (rj['family'])
				evs = (evolfam['evolutionLine'])
				evs = str(evs)
				evs = evs.replace("'", "")
				evs = evs.replace("]", "")
				evs = evs.replace("[", "")
				hp = (stats['hp'])
				attack = (stats['attack'])
				defense = (stats['defense'])
				speed = (stats['speed'])
				spattack = (stats['sp_atk'])
				spdef = (stats['sp_def'])
				abilities = (rj['abilities'])
				abilities = str(abilities)
				abilities = abilities.replace("'", "")
				abilities = abilities.replace("[", "")
				abilities = abilities.replace("]", "")
				weight = (rj['weight'])
				height = (rj['height'])
				weight = weight.replace(u'\xa0', u' ')
				height = height.replace(u'\xa0', u' ')
				species = str(species)
				species = species.replace("'", "")
				species = species.replace("[", "")
				species = species.replace("]", "")
				species = species.replace(",", "")
				ptype = str(ptype)
				ptype = ptype.replace("'", "")
				ptype = ptype.replace("[", "")
				ptype = ptype.replace("]", "")
				imgs = (rj['sprites'])
				if int(rj['generation']) < 6:
					img = (imgs['animated'])
				else:
					img = (imgs['normal'])
					url = (imgs['normal'])
				try:
					idx = await session.get(url)
					idx = await idx.read()
					#await url.save(f'{pokemon}av.png',seek_begin = True)
					embed = discord.Embed(title=name,
										  description=desc,
										  color=random.randint(0, 0xFFFFFF))
				except:
					embed = discord.Embed(title=name, description=desc)
					embed.set_thumbnail(url=img)
					embed.add_field(
					name="Information",
					value=
					f"Pokedex Entry: {pid}\nFirst introduced in generation {(rj['generation'])}\nType(s): {ptype}\nAbilities: {abilities}", inline=True)
					embed.add_field(
					name="Base Stats",
					value=
					f"HP: {hp}\nDefense: {defense}\nSpeed: {speed}\nAttack: {attack}\nSpecial Attack: {spattack}\nSpecial Defense: {spdef}", inline=True)
				if len(evs) != 0:
					embed.add_field(name="Evolution Line",
									value=evs,
									inline=True)
					embed.set_footer(icon_url=ctx.author.avatar_url,
								 text=f"Requested by {ctx.author}")
				await ctx.send(embed=embed)

	@slash(
		name="urban",
		description="Urban dictionary",
	)
	async def _urban(self, ctx, word: str):
		author = ctx.author.id
		button = [
			create_button(
				style=ButtonStyle.gray,
				emoji="⬅️",
				custom_id="prev",
			),
			create_button(
				style=ButtonStyle.gray,
				emoji="➡️",
				custom_id="next",
			),
		]
		buttons = create_actionrow(*button)
		url = "http://api.urbandictionary.com/v0/define"
		gray = 0x6d6868
		response = requests.get(url, params=[("term", word)]).json()
		ran = int(0)
		page = (len(response["list"]) - 1)
		if len(response["list"]) == 0:
			embed = discord.Embed(description="No results found!", color=gray)
			await ctx.send(embed=embed, hidden=True)
		else:
			defi = response["list"][ran]["definition"]
			if len(defi) > 700:
				defi = defi[:690] + "..."
			ex = response["list"][ran]["example"]
			if len(ex) > 700:
				ex = ex[:330] + "..."
			embed = discord.Embed(title=f"{response['list'][ran]['word']}",
								  color=gray)
			embed.add_field(name="Definition", value=defi)
			embed.add_field(name="Example", value=ex)
			embed.set_footer(
				text=
				f"👍 {response['list'][0]['thumbs_up']} | 👎 {response['list'][0]['thumbs_down']} • Page 0/{page}"
			)
			msg = await ctx.send(embed=embed, components=[buttons])
			while True:
				try:
					op: ComponentContext = await wait_for_component(
						self.bot,
						components=[buttons],
						messages=msg.id,
						timeout=30)
					if author == op.author_id:
						if op.custom_id == "prev":
							if ran == 0:
								ran = int(0)
							else:
								ran = int(ran - 1)
							defi = response["list"][ran]["definition"]
							if len(defi) > 700:
								defi = defi[:690] + "..."
							ex = response["list"][ran]["example"]
							if len(ex) > 700:
								ex = ex[:330] + "..."
							embed = discord.Embed(
								title=f"{response['list'][ran]['word']}",
								color=gray)
							embed.add_field(name="Definition", value=defi)
							embed.add_field(name="Example", value=ex)
							embed.set_footer(
								text=
								f"👍 {response['list'][ran]['thumbs_up']} | 👎 {response['list'][ran]['thumbs_down']} • Page {ran}/{page}"
							)
							await op.edit_origin(embed=embed)
						elif op.custom_id == "next":
							if ran == len(response["list"]) - 1:
								ran = int(len(response["list"]) - 1)
							else:
								ran = int(ran + 1)
							defi = response["list"][ran]["definition"]
							if len(defi) > 700:
								defi = defi[:690] + "..."
							ex = response["list"][ran]["example"]
							if len(ex) > 700:
								ex = ex[:330] + "..."
							embed = discord.Embed(
								title=f"{response['list'][ran]['word']}",
								color=gray)
							embed.add_field(name="Definition", value=defi)
							embed.add_field(name="Example", value=ex)
							embed.set_footer(
								text=
								f"👍 {response['list'][ran]['thumbs_up']} | 👎 {response['list'][ran]['thumbs_down']} • Page {ran}/{page}"
							)
							await op.edit_origin(embed=embed)
					else:
						await op.edit_origin()
				except TimeoutError:
					await msg.edit(components=[])
					break

	@slash(
		name="img",
		description="Search for an image",
	)
	async def _img(self, ctx: SlashContext, search: str):
		permanent_id = ctx.author.id
		await ctx.defer()
		# Get the image and the number of results
		ran = int(0)
		resource = build("customsearch", "v1",
						 developerKey=google_cloud).cse()
		result = resource.list(q=f"{search}",
							   cx=google_cse,
							   searchType="image").execute()
		url = result["items"][ran]["link"]
		title = result["items"][ran]["title"]
		displayLink = result["items"][ran]["displayLink"]
		contextLink = result["items"][ran]["image"]["contextLink"]
		# Buttons
		buttons = [
			create_button(style=ButtonStyle.blurple,
						  emoji="◀",
						  custom_id="left"),
			create_button(style=ButtonStyle.blurple,
						  emoji="▶",
						  custom_id="right"),
			create_button(style=ButtonStyle.blurple,
						  emoji="🔀",
						  custom_id="random"),
			create_button(style=ButtonStyle.green, emoji="📄",
						  custom_id="page"),
			create_button(style=ButtonStyle.gray,
						  emoji="⏹",
						  custom_id="cancel")
		]
		action_row = [create_actionrow(*buttons)]
		embed = discord.Embed(title=f"Image for: {search}",
							  color=random.randint(0, 0xFFFFFF))
		embed.set_image(url=url)
		embed.set_footer(
			icon_url=
			"https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
			text=f"Google Search • Page {ran}/9")
		embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
		msg = await ctx.send(embed=embed, components=action_row)
		while True:
			try:
				action = await wait_for_component(self.bot,
												  components=action_row,
												  messages=msg.id,
												  timeout=30)
				if action.component_type == 2:
					if permanent_id == action.author.id:
						if action.custom_id == "left":
							if ran == 0:
								ran = int(0)
							else:
								ran = ran - 1
							title = result["items"][ran]["title"]
							displayLink = result["items"][ran]["displayLink"]
							contextLink = result["items"][ran]["image"]["contextLink"]
							url = result["items"][ran]["link"]
							embed = discord.Embed(title=f"Image for: {search}",
									color=random.randint(0, 0xFFFFFF))
							embed.set_image(url=url)
							embed.set_footer(
								icon_url=
								"https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
								text=f"Google Search • Page {ran}/9")
							embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
							await action.edit_origin(embed=embed)
						elif action.custom_id == "right":
							if ran == 9:
								ran = int(9)
							else:
								ran = ran + 1
							title = result["items"][ran]["title"]
							displayLink = result["items"][ran]["displayLink"]
							contextLink = result["items"][ran]["image"]["contextLink"]
							url = result["items"][ran]["link"]
							embed = discord.Embed(title=f"Image for: {search}",
									color=random.randint(0, 0xFFFFFF))
							embed.set_image(url=url)
							embed.set_footer(
								icon_url=
								"https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
								text=f"Google Search • Page {ran}/9")
							embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
							await action.edit_origin(embed=embed)
						elif action.custom_id == "random":
							ran = random.randint(0, 9)
							title = result["items"][ran]["title"]
							displayLink = result["items"][ran]["displayLink"]
							contextLink = result["items"][ran]["image"]["contextLink"]
							url = result["items"][ran]["link"]
							embed = discord.Embed(title=f"Image for: {search}",
									color=random.randint(0, 0xFFFFFF))	
							embed.set_image(url=url)
							embed.set_footer(
								icon_url=
								"https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
								text=f"Google Search • Page {ran}/9")
							embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
							await action.edit_origin(embed=embed)
						elif action.custom_id == "page":

							def check(m):
								return m.author == ctx.author and m.channel == ctx.channel

							await action.send(
								"Which page would you like to go? (0 - 9)",
								hidden=True)
							msg1 = await self.bot.wait_for("message",
														   check=check)
							ran1 = str(msg1.content)
							if ran1.isdigit() is True:
								if 0 <= int(ran1) <= 9:
									ran = int(ran1)
									title = result["items"][ran]["title"]
									displayLink = result["items"][ran]["displayLink"]
									contextLink = result["items"][ran]["image"]["contextLink"]
									url = result["items"][ran]["link"]
									embed = discord.Embed(title=f"Image for: {search}",
											color=random.randint(0, 0xFFFFFF))
									embed.set_image(url=url)
									embed.set_footer(text=f"Page {ran}/9")
									embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
									await msg1.delete()
									await msg.edit(embed=embed)
								else:
									await msg1.delete()
									await action.send(
										"That is not a valid page number! Only from 0 to 9 is allowed.",
										hidden=True)
							else:
								continue
						elif action.custom_id == "cancel":
							await msg.delete()
							return
					else:
						await action.edit_origin()
			except TimeoutError:
				await msg.edit(components=[])
				break

	@slash(
		name="trivia",
		description="Play a trivia game",
	)
	async def _trivia(self, ctx: SlashContext):
		permanent_id = ctx.author.id
		buttons = [
			create_button(
				style=ButtonStyle.green,
				label="True",
				custom_id="True",
			),
			create_button(
				style=ButtonStyle.danger,
				label="False",
				custom_id="False",
			),
			create_button(
				style=ButtonStyle.gray,
				emoji="🙏",
				custom_id="Skip",
			)
		]
		action_row = create_actionrow(*buttons)
		api = "https://opentdb.com/api.php?amount=1&type=boolean"
		async with aiohttp.ClientSession() as triviaSession:
			async with triviaSession.get(api) as response:
				data = await response.json()
				if data["response_code"] == 0:
					category = data["results"][0]["category"]
					question = data["results"][0]["question"]
					correct_answer = data["results"][0]["correct_answer"]
					embed = discord.Embed(
						title="Trivia",
						description=f"**{category}**: {question}")
					embed.set_author(name=ctx.author,
									 icon_url=ctx.author.avatar_url)
					msg = await ctx.send(embed=embed, components=[action_row])
				else:
					await ctx.send(f"Error: {data['response_code']}",
								   hidden=True)
					return
				while True:
					try:
						button_ctx = await wait_for_component(
							self.bot,
							components=[action_row],
							messages=msg.id,
							timeout=10)
						if button_ctx.component_type == 2:  # check if button
							if permanent_id == button_ctx.author.id:
								if button_ctx.custom_id == "True":
									if correct_answer == "True":
										await button_ctx.send(
											content=
											f"{button_ctx.author.mention}, you are correct!",
											hidden=True)
										author_answer = "correct"
									else:
										await button_ctx.send(
											content=
											f"{button_ctx.author.mention}, you are wrong!",
											hidden=True)
										author_answer = "wrong"
								elif button_ctx.custom_id == "False":
									if correct_answer == "False":
										await button_ctx.send(
											content=
											f"{button_ctx.author.mention}, you are correct!",
											hidden=True)
										author_answer = "correct"
									else:
										await button_ctx.send(
											content=
											f"{button_ctx.author.mention}, you are wrong!",
											hidden=True)
										author_answer = "wrong"
								elif button_ctx.custom_id == "Skip":
									await button_ctx.send(
										content=
										f"{button_ctx.author.mention}, you skipped the question.",
										hidden=True)
									author_answer = "skipped"
								for i in range(3):
									action_row["components"][i][
										"disabled"] = True
									embed1 = discord.Embed(
										title="Trivia",
										description=
										f"**{category}**: {question}")
									embed1.set_author(
										name=ctx.author,
										icon_url=ctx.author.avatar_url)
									if author_answer == "correct":
										embed1.add_field(
											name="‎",
											value=
											f"{button_ctx.author.mention} had the correct answer."
										)
									elif author_answer == "wrong":
										embed1.add_field(
											name="‎",
											value=
											f"{button_ctx.author.mention} had the wrong answer."
										)
									elif author_answer == "skipped":
										embed1.add_field(
											name="‎",
											value=
											f"{button_ctx.author.mention} skipped the question."
										)
								await msg.edit(embed=embed1,
											   components=[action_row])
								break
							else:
								await button_ctx.edit_origin()
					except TimeoutError:
						for i in range(3):
							action_row["components"][i]["disabled"] = True
						await msg.edit(content="Timed out.",
									   components=[action_row])
						break

	@subcommand(
		base="rock_paper_scissors",
		name="ai",
		description="Play rock paper scissors against AI",
	)
	async def _rps(self, ctx: SlashContext):
		permanent_id = ctx.author.id
		# Selection
		select = create_select(
			options=[
				create_select_option('rock', '1', '🪨', 'rock'),
				create_select_option('paper', '2', '📝', 'paper'),
				create_select_option('scissors', '3', '✂', 'scissors')
			],
			placeholder="Choose your option",
			min_values="1",
			max_values="1",
		)
		selection = [create_actionrow(select)]
		msg = await ctx.send(f'**{ctx.author.name}** vs **Articuno**',
							 components=selection)
		# Wait for selection
		while True:
			cmp1: ComponentContext = await wait_for_component(
				self.bot, components=selection, messages=msg.id)
			if permanent_id == cmp1.author.id:
				select['disabled'] = True
				await cmp1.edit_origin(
					content=cmp1.origin_message.content +
					f'\n{cmp1.author.mention} has chosen their option!',
					components=[create_actionrow(select)])
				# AI Selection
				choice = random.randint(1, 3)
				choice1 = int(cmp1.selected_options[0])
				choice2 = int(choice)
				choice_convert = {
					1: 'rock',
					2: 'paper',
					3: 'scissors',
				}
				if choice1 == choice2:
					await cmp1.send(
						f"It's a tie! Both players chose {choice_convert[choice1]}!"
					)
				elif (choice1 - choice2) % 3 == 1:
					await cmp1.send(
						f'{choice_convert[choice1].title()} beats {choice_convert[choice2]}!\n'
						f'{cmp1.author.mention} won!')
				elif (choice1 - choice2) % 3 == 2:
					await cmp1.send(
						f'{choice_convert[choice2].title()} beats {choice_convert[choice1]}!\n'
						f'Articuno won!')
				else:
					await cmp1.send('A logic issue occurred.')
				break
			else:
				await cmp1.edit_origin()

	@subcommand(
		base="rock_paper_scissors",
		name="human",
		description="Play rock paper scissors against someone",
	)
	async def _rpsh(self, ctx: SlashContext):
		author = ctx.author.id
		# Rock & Paper & Scissors selection
		select = create_select(
			options=[
				create_select_option('rock', '1', '🪨', 'rock'),
				create_select_option('paper', '2', '📝', 'paper'),
				create_select_option('scissors', '3', '✂', 'scissors')
			],
			placeholder="Choose your option",
			min_values="1",
			max_values="1",
		)
		selection = [create_actionrow(select)]
		# Challenge selection
		request = [
			create_button(
				style=ButtonStyle.green,
				label="Accept",
				custom_id="accept",
			),
			create_button(
				style=ButtonStyle.gray,
				label="Cancel",
				custom_id="cancel",
			)
		]
		requests = [create_actionrow(*request)]
		msg = await ctx.send(f"{ctx.author.mention} opened a challenge.",
							 components=requests)
		# Wait for selection
		while True:
			try:
				op: ComponentContext = await wait_for_component(
					self.bot, components=requests, messages=msg.id, timeout=60)
				if op.custom_id == "accept":
					if op.author_id == author:
						await op.send("You cannot challenge yourself.",
									  hidden=True)
					else:
						await op.edit_origin(
							content=
							f"**{ctx.author.mention}** vs **{op.author.mention}**",
							components=selection)
						challenger = op.author_id
						# Wait for player 1 selection
						while True:
							cmp1: ComponentContext = await wait_for_component(
								self.bot,
								components=selection,
								messages=msg.id)
							if cmp1.author_id == author or cmp1.author_id == challenger:
								cmp_1 = cmp1.author_id
								await cmp1.edit_origin(
									content=cmp1.origin_message.content +
									f'\n\n{cmp1.author.mention} has chosen their option!'
								)
								choice1 = int(cmp1.selected_options[0])
								break
							else:
								await cmp1.edit_origin()
						# Wait for player 2 selection
						while True:
							cmp2: ComponentContext = await wait_for_component(
								self.bot,
								components=selection,
								messages=msg.id)
							if cmp2.author_id != cmp_1 and cmp2.author_id == challenger or cmp2.author_id == author:
								select['disabled'] = True
								await cmp2.edit_origin(
									content=cmp2.origin_message.content +
									f'\n{cmp2.author.mention} has chosen their option!',
									components=[create_actionrow(select)])
								choice2 = int(cmp2.selected_options[0])
								break
							else:
								await cmp2.edit_origin()
						# Compare choices
						choice_convert = {
							1: 'rock',
							2: 'paper',
							3: 'scissors',
						}
						if choice1 == choice2:
							await cmp2.send(
								f"It's a tie! Both players chose {choice_convert[choice1]}!"
							)
						elif (choice1 - choice2) % 3 == 1:
							await cmp2.send(
								f'{choice_convert[choice1].title()} beats {choice_convert[choice2]}!\n'
								f'{cmp1.author.mention} wins!')
						elif (choice1 - choice2) % 3 == 2:
							await cmp2.send(
								f'{choice_convert[choice2].title()} beats {choice_convert[choice1]}!\n'
								f'{cmp2.author.mention} wins!')
						else:
							await cmp2.send('A logic issue occurred')
				elif op.custom_id == "cancel":
					if op.author_id == author:
						await msg.delete()
						return
					else:
						await op.edit_origin()
			except TimeoutError:
				await msg.delete()
				return


def setup(bot: commands.Bot):
	bot.add_cog(Fun(bot))
