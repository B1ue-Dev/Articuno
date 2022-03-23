import interactions
from interactions import extension_command as command
from interactions import CommandContext
import platform, psutil, datetime, json, utils.utils as utils, json

with open("./data/servers.json") as f:
	data = json.load(f)
	ids = data['ID']


load_time = datetime.datetime.now()


class Basic(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	

	@command(
		name="ping",
		description="Ping Articuno"
	)
	async def ping(self, ctx: CommandContext):
		if int(ctx.guild_id) in ids:
			return
		else:
			websocket = f"{self.bot.latency * 1:.0f}"
			await ctx.send(f"Pong! {websocket}ms")
	

	@command(
		name="stats",
		description="Get Articuno's stats"
	)
	async def stat(self, ctx: CommandContext):
		if int(ctx.guild_id) in ids:
			return
		else:
			proc = psutil.Process()
			mems = proc.memory_full_info()
			cpus = psutil.cpu_percent()
			thread_counts = proc.num_threads()
			mem = f"{utils.natural_size(mems.rss)}\n{utils.natural_size(mems.vms)}"
			cpu = f"{cpus}%\n{thread_counts} Threads"
			latency = f"{self.bot.latency * 1:.0f}ms"
			python = platform.python_version()
			os = str(platform.platform())
			uptime = utils.pretty_date(load_time)
			fields = [
				interactions.EmbedField(name="Latency", value=latency, inline=True),
				interactions.EmbedField(name="Python", value=python, inline=True),
				interactions.EmbedField(name="CPU", value=cpu, inline=True),
				interactions.EmbedField(name="Memory", value=mem, inline=True),
				interactions.EmbedField(name="Uptime", value=uptime, inline=True),
				interactions.EmbedField(name="System", value=os, inline=True)
			]
			url = f"https://cdn.discordapp.com/avatars/{int(self.bot.me.id)}/{self.bot.me.icon}"
			thumbnail = interactions.EmbedImageStruct(url=url)._json
			footer = interactions.EmbedFooter(text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=f"{ctx.author.user.avatar_url}")
			github = interactions.Button(
				style = interactions.ButtonStyle.LINK,
				label = "GitHub",
				url = "https://github.com/Jimmy-Blue/Articuno"
			)
			embed = interactions.Embed(title="Articuno Stats", color=0x236adf, thumbnail=thumbnail, footer=footer, fields=fields)
			await ctx.send(embeds=embed, components=[github])




def setup(bot):
	Basic(bot)
