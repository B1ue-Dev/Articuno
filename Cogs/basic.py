import interactions
from interactions import extension_command as command
import platform, psutil, utils.utils as utils, datetime, os, utils.utils as utils
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))
load_time = datetime.datetime.now()





class Basic(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot


	@command(
		name='ping',
		description='Ping Articuno',
		scope=scope
	)
	async def _ping(self, ctx: interactions.CommandContext):
		websocket = f"{self.bot.latency * 1:.0f}"

		if int(websocket) < int(99):
			message = f"{websocket}ms <:Connection_Best:936294842286342204>"
		elif int(100) <= int(websocket) < int(199):
			message = f"{websocket}ms<:Connection_Stable:936294747516067841>"
		elif int(websocket) > int(200):
			message = f"{websocket}ms <:Connection_Bad:936294724954894436>"

		footer = interactions.EmbedFooter(
			text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
			icon_url=f"{ctx.author.user.avatar_url}"
		)
		embed = interactions.Embed(
			title=":ping_pong: Pong!",
			description=f"Websocket: {message}",
			color=0xff8b00,
			footer=footer
		)

		await ctx.send(embeds=embed)



	@command(
		name="stats",
		description="Shows the stats of Articuno",
		scope=scope
	)
	async def _stats(self, ctx: interactions.CommandContext):
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
		footer = interactions.EmbedFooter(
			text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
			icon_url=f"{ctx.author.user.avatar_url}"
		)
		github = interactions.Button(
			style = interactions.ButtonStyle.LINK,
			label = "GitHub",
			url = "https://github.com/Jimmy-Blue/Articuno"
		)
		embed = interactions.Embed(
			title="Articuno Stats",
			color=0x236adf,
			thumbnail=thumbnail,
			footer=footer,
			fields=fields
		)

		await ctx.send(embeds=embed, components=[github])



	@command(
		name="credits",
		description="Developers/Contributors to this project",
		scope=scope
	)
	async def credits(self, ctx: interactions.CommandContext):
		fields = [
			interactions.EmbedField(name="**BlueZ#7181**", value="``Leader``\n> Owner, creator and debugger for Articuno. Mostly handle with code and errors.", inline=True),
			interactions.EmbedField(name="**Manana#3313**\n**꒓ꆂꌚꑛꂑꁍꆂ#8149**", value="``Tester``\n> Insiders for this project.")
		]
		footer = interactions.EmbedFooter(
			text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
			icon_url=f"{ctx.author.user.avatar_url}"
		)
		embed = interactions.Embed(
			title="Credits",
			description="Developers and contributors in this project:",
			color=0x236adf,
			footer=footer,
			fields=fields
		)

		await ctx.send(embeds=embed)
	


	@command(
		name="invite",
		description="Invite Articuno to your server",
		scope=scope
	)
	async def invite(self, ctx: interactions.CommandContext):
		footer = interactions.EmbedFooter(
			text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
			icon_url=f"{ctx.author.user.avatar_url}"
		)
		embed = interactions.Embed(
			title="Invite Articuno to your server",
			description="[Invite](https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=2146958847&scope=bot%20applications.commands)\n\nSupport server: https://discord.gg/MCTppQWZcA",
			color=0x236adf,
			footer=footer
		)

		await ctx.send(embeds=embed)






def setup(bot):
	Basic(bot)
