import interactions
from interactions import CommandContext, Embed, Option, OptionType
from interactions import extension_command as command
from interactions import extension_component as component
from interactions import extension_listener as listener
from interactions import extension_user_command as user_command
from interactions import extension_message_command as message_command
import platform, psutil, utils.utils as utils, datetime, os, utils.utils as utils
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))


load_time = datetime.datetime.now()




class Basic(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot

	
	@command(name='ping',
			description='Ping Articuno',
			scope=scope)
	async def ping(self, ctx: CommandContext):
		websocket = f"{self.bot.latency * 1:.0f}"
		if int(websocket) < int(99):
			message = f"{websocket}ms <:Connection_Best:936294842286342204>"
		elif int(100) <= int(websocket) < int(199):
			message = f"{websocket}ms<:Connection_Stable:936294747516067841>"
		elif int(websocket) > int(200):
			message = f"{websocket}ms <:Connection_Bad:936294724954894436>"
		embed = interactions.Embed(title=":ping_pong: Pong!", description=f"Websocket: {message}", color=0xff8b00, footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}"))
		await ctx.send(embeds=embed)

	
	@command(name="stats",
			description="Shows the stats of Articuno",
			scope=scope)
	async def stats(self, ctx: CommandContext):
		proc = psutil.Process()
		mems = proc.memory_full_info()
		cpus = psutil.cpu_percent()
		thread_counts = proc.num_threads()
		mem = f"{utils.natural_size(mems.rss)}\n{utils.natural_size(mems.vms)}"
		cpu = f"{cpus}%\n{thread_counts} Threads"
		version = "v4.0.0a"
		latency = f"{self.bot.latency * 1:.0f}ms"
		python = platform.python_version()
		os = str(platform.platform())
		uptime = utils.pretty_date(load_time)
		fields = [
			interactions.EmbedField(name="Version", value=version, inline=True),
			interactions.EmbedField(name="Latency", value=latency, inline=True),
			interactions.EmbedField(name="Python", value=python, inline=True),
			interactions.EmbedField(name="CPU", value=cpu, inline=True),
			interactions.EmbedField(name="Memory", value=mem, inline=True),
			interactions.EmbedField(name="Uptime", value=uptime, inline=True),
			interactions.EmbedField(name="System", value=os, inline=True)
		]
		thumbnail = interactions.EmbedImageStruct(url=self.bot.me.icon_url)._json
		footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}")
		github = interactions.Button(
			style = interactions.ButtonStyle.LINK,
			label = "GitHub",
			url = "https://github.com/Jimmy-Blue/Articuno"
		)
		embed = Embed(title="Articuno Stats", color=0x236adf, thumbnail=thumbnail, footer=footer, fields=fields)
		await ctx.send(embeds=embed, components=[github])
	

	@command(name="credits",
			description="Developers/Contributors to this project",
			scope=scope)
	async def credits(self, ctx: CommandContext):
		fields = [
			interactions.EmbedField(name="**BlueZ#7181**", value="``Leader``\n> Owner, creator and debugger for Articuno. Mostly handle with code and errors.", inline=True),
			interactions.EmbedField(name="**Manana#3313**\n**꒓ꆂꌚꑛꂑꁍꆂ#8149**", value="``Tester``\n> Insiders for this project.")
		]
		footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}")
		embed = Embed(title="Credits", description="Developers and contributors in this project:", color=0x236adf, footer=footer, fields=fields)
		await ctx.send(embeds=embed)
	

	@command(name="invite",
			description="Invite Articuno to your server",
			scope=scope)
	async def invite(self, ctx: CommandContext):
		footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}")
		embed = Embed(title="Invite Articuno to your server", description="[Invite](https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=2146958847&scope=bot%20applications.commands)\n\nSupport server: https://discord.gg/MCTppQWZcA", color=0x236adf, footer=footer)
		await ctx.send(embeds=embed)


	# Base: info
	@command(
		name="info",
		description="An information command",
		scope=scope,
		options=[
			Option(
				type=OptionType.SUB_COMMAND,
				name="user",
				description="Shows information of targeted user",
				options=[
					Option(
						type=OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					)
				],
			),
			Option(
				type=OptionType.SUB_COMMAND,
				name="server",
				description="Shows information of current server",
			),
		]
	)
	async def info(self, ctx: interactions.CommandContext,
		sub_command: str,
		user: interactions.Member = None,
		server: interactions.Guild = None,
	):
		if sub_command == "user":
			role = await (await ctx.get_guild()).get_role(role_id=user.roles[0])
			name = user.user.username
			discriminator = int(user.user.discriminator)
			nick = user.nick
			id = int(user.user.id)
			joined_at = round(user.joined_at.timestamp())
			created_at = user.user.id.epoch
			avatar = user.user.avatar_url
			highest_role_color = role.color
			public_flags = user.user.public_flags
			hypesquad = None
			if isinstance(public_flags, int) is True:
				if public_flags & 1 << 6:
					hypesquad = "<:bravery:957684396268322886> Bravery"
				elif public_flags & 1 << 7:
					hypesquad = "<:brilliance:957684592498843658> Brilliance"
				elif public_flags & 1 << 8:
					hypesquad = "<:balance:957684753174241330> Balance"
			else:
				hypesquad = None
			bot = user.user.bot
			if bot is True:
				bot = "Yes"
			else:
				bot = "No"
			early_supporter = None
			if isinstance(public_flags, int) is True:
				if public_flags & 1 << 9:
					early_supporter = "Yes"
				else:
					early_supporter = "No"
			else:
				early_supporter = "No"
			fields = [
				interactions.EmbedField(name="Name", value=f"{name}", inline=True),
				interactions.EmbedField(name="Nickname", value=f"{nick}", inline=True),
				interactions.EmbedField(name="ID", value=f"{id}", inline=True),
				interactions.EmbedField(name="Joined at", value=f"<t:{joined_at}>", inline=True),
				interactions.EmbedField(name="Created at", value=f"<t:{created_at}>", inline=True),
				interactions.EmbedField(name="Highest role", value=f"{role.mention}", inline=True),
				interactions.EmbedField(name="Hypesquad", value=f"{hypesquad}", inline=True),
				interactions.EmbedField(name="Bot", value=f"{bot}", inline=True),
				interactions.EmbedField(name="Early supporter", value=f"{early_supporter}", inline=True),
			]
			thumbnail = interactions.EmbedImageStruct(url=avatar)
			footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}")
			embed = Embed(title=f"{name}#{discriminator}", color=highest_role_color, thumbnail=thumbnail, footer=footer, fields=fields)
			await ctx.send(embeds=embed)
		if sub_command == "server":
			guild = await ctx.get_guild()
			name = guild.name
			id = guild.icon_url
			await ctx.send(f"{id}")

			










def setup(bot):
	Basic(bot)