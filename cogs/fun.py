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
import requests
import random
import aiohttp
import io
import utils
import urllib
import json
from googleapiclient.discovery import build
# Again, I just import everything




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
	guild_ids = [833886728259239968, 859030372783751168, 738938246574374913]

	# I use some API here. They are mostly from https://some-random-api.ml/
	# The API is free to use. You can use this API for your own project or based on my code.
	# I do not claim any ownership over the API.


	'''
	Using ``random`` module
	'''

	@slash(name="ship",
		description="Ship two people",
		)
	async def _ship(self, ctx: SlashContext, user1: str = None, user2: str = None):
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
			comment = "Really low! {}".format(random.choice(
				[
				'Friendzone.', 
				'Just "friends".', 
				'There is barely any love.',
				'I sense a small bit of love!',
				'Still in that friendzone ;(',
            	'No, just no!',
            	'But there is a small sense of romance from one person!'
				]
			))
			heart = ":broken_heart:"
		elif 31 <= shipnumber <= 70:
			comment = "Moderate! {}".format(random.choice(
				[
				'Fair enough!',
				'A small bit of love is in the air...',
				'I feel like there is some romance progressing!',
				'I am starting to feel some love!',
				'At least this is acceptable.',
				'...',
				'I sense a bit of potential!',
				'But it is very one-sided OwO.'
				]
			))
			heart = ":mending_heart:"
		elif 71 <= shipnumber <= 90:
			comment = "Almost perfect! {}".format(random.choice(
				[
				'I definitely can see that love is in the air.',
				'I feel the love! There is a sign of a match!',
				'A few things can be imporved to make this a match made in heaven!',
				'I can definitely feel the love.',
				'This has a big potential.',
				'I can see the love is there! Somewhere...'
				]
			))
			heart = random.choice(
				[
				':revolving_hearts:',
				':heart_exclamation:',
				':heart_on_fire:',
				':heartbeat:'
				]
			)
		elif 90 < shipnumber <= 100:
			comment = "True love! {}".format(random.choice(
				[
				'It is a match!', 
				'There is a match made in heaven!', 
				'It is definitely a match!',
				'Love is truely in the air!', 
				'Love is most definitely in the air!'
				]
			))
			heart = random.choice(
				[
				':sparkling_heart:',
				':heart_decoration:',
				':hearts:',
				':two_hearts:',
				':heartpulse:'
				]
			)
		# Choose color
		if shipnumber <= 40:
			shipColor = 0xE80303
		elif 41 < shipnumber < 80:
			shipColor = 0xff6600
		else:
			shipColor = 0x3be801
		embed = discord.Embed(title="Love test for: ", description=f"**{user1}** and **{user2}** {heart}" ,color=shipColor)
		embed.add_field(name="Results:", value=f"{shipnumber}%  {comment}", inline=True)
		embed.set_author(name="Shipping", icon_url=ctx.author.avatar)
		await ctx.send(embed=embed)


	@slash(name="roll",
		description="Roll a dice",
		)
	async def _roll(self, ctx: SlashContext):
		dice = [1, 2, 3, 4, 5, 6]
		number = random.choice(dice)
		msg = await ctx.send("I am rolling the dice now!")
		await asyncio.sleep(2.5)
		await msg.edit(content=f"The number is {number}.")
	

	@slash(name="flip",
		description="Flip a coin",
		)
	async def _flip(self, ctx: SlashContext):
		flip = ['heads', 'tails']
		number = random.choice(flip)
		msg = await ctx.send("I am flipping the coin now!")
		await asyncio.sleep(2.5)
		await msg.edit(content=f"The coin landed on {number}.")


	@slash(name="gay",
		description="Calculate the gay percentage of a user",
		)
	async def _gay(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author.name
		number = random.randint(0, 100)
		embed = discord.Embed(color=random.randint(0, 0xFFFFFF))
		embed.add_field(name=f"Gay measure tool", value=f"**{user}** is {number}% gay.")
		await ctx.send(embed=embed)




	'''
	Some kind of API requests, GET thing
	'''

	@slash(name="quote",
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


	@slash(name="coffee",
		description="Get a coffee",
		)
	async def _coffee(self, ctx: SlashContext):
		response = requests.get('https://coffee.alexflipnote.dev/random.json')
		data = response.json()
		embed = discord.Embed(title="Coffee ☕", color=brown)
		embed.set_image(url=data['file'])
		await ctx.send(embed=embed)


	@slash(name="xkcd",
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
								color = random.randint(0, 0xFFFFFF))
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
								color = random.randint(0, 0xFFFFFF))
			embed.set_image(url=img)
			embed.set_footer(text=f"Day {day}, ID: {num}")
			await ctx.send(embed=embed)


	@slash(name="urban",
		description="Urban dictionary",
		)
	async def _urban(self, ctx, word: str):
		author = ctx.author.id
		button = [
			create_button(
				style=ButtonStyle.gray,
				emoji = "⬅️",
				custom_id="prev",
			),
			create_button(
				style=ButtonStyle.gray,
				emoji = "➡️",
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
			embed = discord.Embed(title=f"{response['list'][ran]['word']}", color=gray)
			embed.add_field(name="Definition", value=response["list"][ran]["definition"])
			embed.add_field(name="Example", value=response["list"][ran]["example"])
			embed.set_footer(text=f"👍 {response['list'][0]['thumbs_up']} | 👎 {response['list'][0]['thumbs_down']} • Page 0/{page}")
			msg = await ctx.send(embed=embed, components=[buttons])
			while True:
				try:
					op: ComponentContext = await wait_for_component(self.bot, components=[buttons], messages=msg.id, timeout=30)
					if author == op.author_id:
						if op.custom_id == "prev":
							if ran == 0:
								ran = int(0)
							else:
								ran = int(ran - 1)
							embed = discord.Embed(title=f"{response['list'][ran]['word']}", color=gray)
							embed.add_field(name="Definition", value=response["list"][ran]["definition"])
							embed.add_field(name="Example", value=response["list"][ran]["example"])
							embed.set_footer(text=f"👍 {response['list'][ran]['thumbs_up']} | 👎 {response['list'][ran]['thumbs_down']} • Page {ran}/{page}")
							await op.edit_origin(embed=embed)
						elif op.custom_id == "next":
							if ran == len(response["list"]) - 1:
								ran = int(len(response["list"]) - 1)
							else:
								ran = int(ran + 1)
							embed = discord.Embed(title=f"{response['list'][ran]['word']}", color=gray)
							embed.add_field(name="Definition", value=response["list"][ran]["definition"])
							embed.add_field(name="Example", value=response["list"][ran]["example"])
							embed.set_footer(text=f"👍 {response['list'][ran]['thumbs_up']} | 👎 {response['list'][ran]['thumbs_down']} • Page {ran}/{page}")
							await op.edit_origin(embed=embed)
					else:
						await op.edit_origin()
				except TimeoutError:
					await msg.edit(components=[])
					break


	@slash(name="pokemon",
		description="Show the infomation about a specific Pokemon",
		guild_ids=guild_ids
		)
	async def _pokemon(self, ctx: SlashContext, pokemon):
		async with aiohttp.ClientSession() as session:
			response = await session.get(f'https://some-random-api.ml/pokedex?pokemon={pokemon}')
			if str(response.status) == "404":
				await ctx.send("I could not find that pokemon. Please try again.", hidden=True)
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
				evs = evs.replace("'","")
				evs = evs.replace("]","")
				evs = evs.replace("[","")
				hp = (stats['hp'])
				attack = (stats['attack'])
				defense = (stats['defense'])
				speed = (stats['speed'])
				spattack = (stats['sp_atk'])
				spdef = (stats['sp_def'])
				abilities = (rj['abilities'])
				abilities = str(abilities)
				abilities = abilities.replace("'","")
				abilities = abilities.replace("[","")
				abilities = abilities.replace("]","")
				weight = (rj['weight'])
				height = (rj['height'])
				weight = weight.replace(u'\xa0', u' ')
				height = height.replace(u'\xa0', u' ')
				species = str(species)
				species = species.replace("'","")
				species = species.replace("[","")
				species = species.replace("]","")
				species = species.replace(",","")
				ptype = str(ptype)
				ptype = ptype.replace("'","")
				ptype = ptype.replace("[","")
				ptype = ptype.replace("]","")
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
					embed=discord.Embed(title=name, description=desc, color=random.randint(0, 0xFFFFFF))
				except:
					embed=discord.Embed(title=name, description=desc)
				embed.set_thumbnail(url=img)
				embed.add_field(name="Information",
					value=f"Pokedex Entry: {pid}\nFirst introduced in generation {(rj['generation'])}\nType(s): {ptype}\nAbilities: {abilities}",
					inline=True
					)
				embed.add_field(name="Base Stats",
					value=f"HP: {hp}\nDefense: {defense}\nSpeed: {speed}\nAttack: {attack}\nSpecial Attack: {spattack}\nSpecial Defense: {spdef}",
					inline=True
					)
				if len(evs) != 0:
					embed.add_field(name="Evolution Line",
					value=evs,
					inline=True
					)
				embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
				await ctx.send(embed=embed)

	




def setup(bot: commands.Bot):
	bot.add_cog(Fun(bot))
