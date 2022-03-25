import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.context import InteractionContext
from discord_slash.utils.manage_commands import create_option, create_choice
import aiohttp, requests
import utils, random, json
import platform, psutil
from jishaku.features.baseclass import Feature as jsk


# Excuse me but I am lazy
subcommand = cog_ext.cog_subcommand
slash = cog_ext.cog_slash


# Color
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868





class Basic(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@slash(name="ping",
		description="Ping Articuno",
		)
	async def _ping(self, ctx: SlashContext):
		websocket = f"{self.bot.latency * 1000:.0f}"
		if int(websocket) < int(99):
			message = f"{websocket}ms <:Connection_Best:936294842286342204>"
		elif int(100) <= int(websocket) < int(199):
			message = f"{websocket}ms<:Connection_Stable:936294747516067841>"
		elif int(websocket) > int(200):
			message = f"{websocket}ms <:Connection_Bad:936294724954894436>"
		embed = discord.Embed(title=":ping_pong: Pong!", description=f"Websocket: {message}", color=orange)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)


	@slash(name="stats",
		description="See the stats of Articuno"
		)
	async def _stats(self, ctx: SlashContext):
		try:
			proc = psutil.Process()
			mem = proc.memory_full_info()
			cpu = psutil.cpu_percent()
			thread_count = proc.num_threads()
		except:
			pass	
		embed=discord.Embed(title="Articuno Stats", color=blue)
		thumbnail = self.bot.user.avatar_url # Thumbnail
		embed.set_thumbnail(url=thumbnail)
		version = "v3.0.3" # Version
		embed.add_field(name="Version", value=version)
		server_count = len(self.bot.guilds) # Server Count
		embed.add_field(name="Server Count",value=server_count)
		user_count = len(self.bot.users) # User Count
		embed.add_field(name="User Count",value=user_count)
		latency = f"{self.bot.latency * 1000:.0f}ms" # Latency
		embed.add_field(name="Latency", value=latency)
		python = platform.python_version() # Python Version
		embed.add_field(name="Python", value=python)
		embed.add_field(name="Uptime", value=f"<t:{utils.timestamp(jsk.load_time)}:R>") # Uptime
		try:
			embed.add_field(name="Memory",value=f"{utils.natural_size(mem.rss)}\n{utils.natural_size(mem.vms)}")
			embed.add_field(name="CPU", value=f"{cpu}%\n{thread_count} threads")
		except:
			pass
		os = str(platform.platform()) # OS
		embed.add_field(name="System", value=os)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		buttons = [
			create_button(style=ButtonStyle.URL, label="GitHub", url="https://github.com/Jimmy-Blue/Articuno")
		]
		action_row = create_actionrow(*buttons)
		await ctx.send(embed=embed, components=[action_row])


	@slash(name="credits",
		description="Developers/Contributors to this project"
		)
	async def _credits(self, ctx: SlashContext):
		embed = discord.Embed(title=f'Credits', description=f"Developers and contributors in this project:", color=blue)
		embed.add_field(name="**BlueZ#7181**", value=f"``Leader`` Owner, creator and debugger for Articuno. Mostly handle with stuffs and errors.")
		embed.add_field(name="**Manana#3313**\n**꒓ꆂꌚꑛꂑꁍꆂ#8149**", value="``Tester`` Insiders for this project.")
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)


	@slash(name="invite",
		description="Invite Articuno to your server"
		)
	async def _invite(self, ctx: SlashContext):
		embed = discord.Embed(title=f"Invite me to your server", description=f"[Invite](https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=1644972474366&scope=bot%20applications.commands)\n\nSupport server: https://discord.gg/MCTppQWZcA", color=blue)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)


	# Base: info
	# Subcommand: user
	@subcommand(base="info", 
				name="user", 
				description="Check the information about a user",
				options=[
					create_option(
						name="user",
						description="Targeted user",
						option_type=6,
						required=False)
					]
				)
	async def _info(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author
		profile = user.public_flags
		# Check hypesquad
		hypesquad = "None"
		if profile.hypesquad_bravery == True:
			hypesquad = "<:bravery:875411242917969961> Bravery"
		if profile.hypesquad_brilliance == True:  
			hypesquad = "<:brilliance:875411403413000233> Brilliance"        
		if profile.hypesquad_balance == True:
			hypesquad = "<:balance:875411281350369330> Ballance"
		supporter = "No"
		if profile.early_supporter == True:
			supporter = "<:earlysupporter:875412600341540874> Yes"
		# Check if bot
		if not user.bot:
			bot = "No"
		else:
			bot = "Yes"
		# Highest role's color
		color = user.top_role.color
		# Joined date
		joined = f"<t:{round(user.joined_at.timestamp())}>"
		joined_ago = f"<t:{round(user.joined_at.timestamp())}:R>"
		# Account creation date
		created = f"<t:{round(user.created_at.timestamp())}>"
		created_ago = f"<t:{round(user.created_at.timestamp())}:R>"
		embed=discord.Embed(colour=color)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_author(name=f"{user.name}'s information", icon_url=user.avatar_url)
		embed.add_field(name="Name", value=user, inline=True)
		embed.add_field(name="Nickname", value=user.nick, inline=True)
		embed.add_field(name="ID", value=user.id, inline=True)
		embed.add_field(name="Joined on", value=f"{joined}\n||({joined_ago})||", inline=True)
		embed.add_field(name="Top role", value=f"<@&{user.top_role.id}>", inline=True)
		embed.add_field(name="Created on", value=f"{created}\n||({created_ago})||", inline=True)
		embed.add_field(name="Hypesquad", value=f"{hypesquad}")
		embed.add_field(name="Bot?", value=bot)
		embed.add_field(name="Early Supporter?", value=supporter)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)

	# Subcommand: avatar
	@subcommand(base="info",
				name="avatar",
				description="Check the profile picture of a user",
				options=[
					create_option(
						name="user",
						description="Targeted user",
						option_type=6,
						required=False
						)
					]
				)
	async def _avatar(self, ctx: SlashContext, user: str = None):
		if not user:
			user = ctx.author
		avatar = user.avatar_url
		member = user
		# Image but in different format
		jpeg = user.avatar_url_as(format="jpeg")
		png = user.avatar_url_as(format="png")
		embed = discord.Embed(title=user, description=f"[**JPEG**]({jpeg})  [**PNG**]({png})", color=random.randint(0, 0xFFFFFF))
		#embed.set_author(icon_url=avatar)
		embed.set_image(url=avatar)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)

	# Subcommand: server
	@subcommand(base="info",
				name="server",
				description="Check the information about the server"
				)
	async def _server(self, ctx: SlashContext):
		name = str(ctx.guild.name)
		id = str(ctx.guild.id)
		memberCount = str(ctx.guild.member_count)
		# Check the number of real user (human) and bot
		memberer = 0
		for member in ctx.guild.members:
			if not member.bot:
				memberer += 1
			if ctx.invoked_subcommand is None:
				bots = sum(1 for member in ctx.guild.members if member.bot)
		icon = ctx.guild.icon_url
		owner = ctx.guild.owner
		region = str(ctx.guild.region)
		created = f"<t:{round(ctx.guild.created_at.timestamp())}>"
		created_ago = f"<t:{round(ctx.guild.created_at.timestamp())}:R>"
		# Check the number of boost
		boost = ctx.guild.premium_subscription_count
		splash = False
		banner = False
		if boost <= 2:
			comment = "Level 0"
		if 2 <= boost < 7:
			comment = "Level 1"
			splash = True
			splash = bool(splash)
		if 7 <= boost < 14:
			comment = "Level 2"
			banner = True
			banner = bool(banner)
		if boost >= 14:
			comment = "Level 3"
		text_channel = len(ctx.guild.text_channels)
		voice_channel = len(ctx.guild.voice_channels)
		category = len(ctx.guild.categories)
		# Verify level
		verify_level = ctx.guild.verification_level
		verify = str(verify_level)
		if verify == "none":
			verify_level = verify
			text = "No criteria set."
		elif verify == "low":
			verify_level = verify
			text = "Must have a verified email."
		elif verify == "medium":
			verify_level = verify
			text = "Must be registered for 5+ minutes."
		elif verify == "high":
			verify_level = verify
			text = "Must be a member of the guild itself for 10+ minutes."
		elif verify == "extreme":
			verify_level = verify
			text = "Must have a verified phone number."
		# Role number
		role_number = len(ctx.guild.roles)
		# Banner
		splash_url = ctx.guild.splash_url_as(format="png")
		banner_url = ctx.guild.banner_url_as(format="png")
		embed = discord.Embed(title=name, color=blue)
		embed.set_thumbnail(url=icon)
		embed.add_field(name="ID", value=id, inline=True)
		embed.add_field(name="Owner", value=f"<@{owner.id}>\n{owner}", inline=True)
		embed.add_field(name="Boost", value=f"Number: {boost}\n{comment}",inline=True)
		embed.add_field(name="Member", value=f"Total: {memberCount}\nHumans: {memberer}\nBots: {bots}", inline=True)
		embed.add_field(name="Channels", value=f"Text channels: {text_channel}\nVoice channels: {voice_channel}\nCategories: {category}")
		embed.add_field(name="Verify level", value=f"Level: {verify_level}\n{text}")
		embed.add_field(name="Created on", value=f"{created}\n||({created_ago})||", inline=True)
		embed.add_field(name="Region", value=region, inline=True)
		embed.add_field(name="Roles", value=f"{role_number}")
		if splash is True:
			embed.add_field(name="\u200b", value=f"[**Server Invite Background**]({splash_url})\n")
		else:
			pass
		if banner is True:
			embed.add_field(name="\u200b", value=f"[**Banner Background**]({banner_url})\n")
		else:
			pass
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)

	"""
	# An AI system
	@commands.Cog.listener()
	async def on_message(self, message): 
		with open("./data/config.json", "r") as f:
			data = json.load(f)
			key = data['APIKEY']
		with open("./data/ai.json", "r") as r:
			data = json.load(r)
			channel = data['AI_CHANNEL']

		if message.author.id == self.bot.user.id:
			return
		if message.channel.id in channel:
			await message.channel.trigger_typing()
			try:
				url = "https://random-stuff-api.p.rapidapi.com/ai"
				querystring = {"msg":message.content,"bot_name":"Articuno","bot_gender":"male","bot_master":"Blue"}
				headers = {
					'authorization': "nhdoHbSSw3c0",
					'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
					'x-rapidapi-key': "aad44bed6dmshba8fa4c3f4d92c2p118235jsne1aae4f19e3f"
				}
				response = requests.request("GET", url, headers=headers, params=querystring)
				data = response.json()
				msg = data['AIResponse']
				await message.channel.send(msg)
			except:
				async with aiohttp.ClientSession() as aiSession:
					async with aiSession.get(f'https://some-random-api.ml/chatbot?message={message.content}&key={key}') as response:
						data = await response.json()
						reply = data['response']
						await aiSession.close()
						await message.channel.send(reply)
	"""





def setup(bot):
	bot.add_cog(Basic(bot))
