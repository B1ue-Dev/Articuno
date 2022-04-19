import interactions
from interactions import extension_command as command
import os
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))





class Info(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot


	@command(
		name="info",
		description="An information command",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="user",
				description="Shows information of targeted user",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					)
				],
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="server",
				description="Shows information of current server",
			)
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
			footer = interactions.EmbedFooter(
				text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
				icon_url=f"{ctx.author.user.avatar_url}"
			)
			embed = interactions.Embed(
				title=f"{name}#{discriminator}",
				color=highest_role_color,
				thumbnail=thumbnail,
				footer=footer,
				fields=fields
			)

			await ctx.send(embeds=embed)

		if sub_command == "server":
			guild = await ctx.get_guild()
			name = guild.name
			id = guild.icon_url
			await ctx.send(f"{id}")





def setup(bot):
	Info(bot)
