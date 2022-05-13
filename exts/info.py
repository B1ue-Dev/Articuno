import interactions
from interactions import extension_command as command
import os, datetime, random
from dotenv import load_dotenv

load_dotenv()
scope = int(os.getenv("SCOPE"))





class Info(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot


	@command(
		name="info",
		description="Information command",
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
						required=True
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="avatar",
				description="Shows avatar of targeted user",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="server",
				description="Shows information of current server"
			)
		]
	)
	async def _info(self, ctx: interactions.CommandContext,
		sub_command: str,
		user: interactions.Member = None
	):
		if sub_command == "user":
			await self._info_user(ctx, user)
		if sub_command == "avatar":
			await self._info_avatar(ctx, user)
		if sub_command == "server":
			await self._info_server(ctx)



	async def _info_user(self, ctx: interactions.CommandContext, user: str):
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
			interactions.EmbedField(name="Created on", value=f"<t:{created_at}>", inline=True),
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
	

	async def _info_avatar(self, ctx: interactions.CommandContext, user: str):
		avatar = user.user.avatar_url
		avatar_jpg = user.user.avatar_url[:-4] + ".jpg"
		avatar_png = user.user.avatar_url[:-4] + ".png"
		avatar_webp = user.user.avatar_url[:-4] + ".webp"
		message = f"[JPG]({avatar_jpg})  [PNG]({avatar_png})  [WEBP]({avatar_webp})"
		if avatar[:-4] == ".gif":
			message += "  [GIF]" + "(" + avatar[:-4] + ".gif)"
		embed = interactions.Embed(
			title=f"{user.user.username}#{user.user.discriminator}",
			description=f"{message}",
			color=random.randint(0, 0xFFFFFF),
			image=interactions.EmbedImageStruct(url=avatar),
			footer=interactions.EmbedFooter(
				text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
				icon_url=f"{ctx.author.user.avatar_url}"
			)
		)
		await ctx.send(embeds=embed)
	

	async def _info_server(self, ctx: interactions.CommandContext):
		guild = interactions.Guild(**await self.bot._http.get_guild(ctx.guild_id), _client=self.bot._http)
		user = interactions.User(**await self.bot._http.get_user(int(guild.owner_id)), _client=self.bot._http)
		name = guild.name
		id = int(guild.id)
		icon = guild.icon_url
		boost = guild.premium_subscription_count
		members = await guild.get_all_members()
		member_counts = len(members)
		human = 0
		bot = 0
		for member in members:
			if member.user.bot is True:
				bot += 1
			else:
				human += 1
		channels = await guild.get_all_channels()
		text_channels = 0
		voice_channels = 0
		categories = 0
		for channel in channels:
			if channel.type is interactions.ChannelType.GUILD_TEXT:
				text_channels += 1
			elif channel.type is interactions.ChannelType.GUILD_VOICE:
				voice_channels += 1
			elif channel.type is interactions.ChannelType.GUILD_CATEGORY:
				categories += 1
		verification_level = int(guild.verification_level)
		splash_bool = False
		banner_bool = False
		if boost <= 2:
			boost_comment = "Level 0"
		elif 2 <= boost < 7:
			boost_comment = "Level 1"
			splash_bool = True
		elif 7 <= boost < 14:
			boost_comment = "Level 2"
			banner_bool = True
		elif boost >= 14:
			boost_comment = "Level 3"
		if verification_level == 0:
			verification_comment = "Unrestricted."
		elif verification_level == 1:
			verification_comment = "Must have verified email on account."
		elif verification_level == 2:
			verification_comment = "Must be registered on Discord for longer than 5 minutes."
		elif verification_level == 3:
			verification_comment = "Must be a member of the server for longer than 10 minutes."
		elif verification_level == 4:
			verification_comment = "Must have a verified phone number."
		role_count = len(guild.roles)
		region = guild.region
		joined_at = guild.id.epoch
		fields = [
			interactions.EmbedField(name="ID", value=f"{id}", inline=True),
			interactions.EmbedField(name="Owner", value=f"{user.mention}\n{user.username}#{user.discriminator}", inline=True),
			interactions.EmbedField(name="Boosts", value=f"Number: {boost}\n{boost_comment}", inline=True),
			interactions.EmbedField(name="Member", value=f"Total: {member_counts}\nHuman: {human}\nBot: {bot}", inline=True),
			interactions.EmbedField(name="Channel", value=f"Text channels: {text_channels}\nVoice channels: {voice_channels}\nCategories: {categories}", inline=True),
			interactions.EmbedField(name="Verify Level", value=f"Level: {verification_level}\n{verification_comment}", inline=True),
			interactions.EmbedField(name="Created on", value=f"<t:{joined_at}>", inline=True),
			interactions.EmbedField(name="Region", value=f"{region}", inline=True),
			interactions.EmbedField(name="Roles", value=f"{role_count} roles", inline=True),
		]
		thumbnail = interactions.EmbedImageStruct(url=icon)
		footer = interactions.EmbedFooter(
			text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
			icon_url=f"{ctx.author.user.avatar_url}"
		)
		embed = interactions.Embed(
			title=f"{name}",
			color=0x788cdc,
			footer=footer,
			thumbnail=thumbnail,
			fields=fields
		)
		if splash_bool is True and guild.splash_url is not None:
			embed.add_field(name="Splash URL", value=f"[Splash_url]({guild.splash_url})", inline=True)
		if banner_bool is True and guild.banner_url is not None:
			embed.add_field(name="Banner URL", value=f"[Banner_url]({guild.banner_url})", inline=True)
		await ctx.send(embeds=embed)





def setup(bot):
	Info(bot)
