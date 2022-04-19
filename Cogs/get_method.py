import interactions
import os
from interactions.ext import wait_for
from dotenv import load_dotenv
load_dotenv()

scope = int(os.getenv("SCOPE"))






class Get_method(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot


	@interactions.extension_command(
		name="get_user",
		description="None",
		scope=scope,
		options = [
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="id",
				description="None",
				required=True,
			)
		]
	)
	async def _get_user(self, ctx: interactions.CommandContext, id: str):
		user = interactions.User(**await self.bot._http.get_user(id), _client=self.bot._http)
		username = user.username
		discriminator = user.discriminator
		avatar_url = user.avatar_url
		await ctx.send(content="{}#{} ({})\n{}".format(username, discriminator, id, avatar_url))
	


	@interactions.extension_command(
		name="get_member",
		description="None",
		scope=scope,
		options = [
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="id",
				description="None",
				required=True,
			)
		]
	)
	async def _get_member(self, ctx: interactions.CommandContext, id: str):
		member = interactions.Member(**await self.bot._http.get_member(ctx.guild_id,id), _client=self.bot._http)
		username = member.user.username
		discriminator = member.user.discriminator
		nick = member.nick
		id = int(member.user.id)
		avatar_url = member.user.avatar_url
		joined_at = round(member.joined_at.timestamp())
		created_at = member.user.id.epoch
		await ctx.send(content="{}#{} ({})\n{}\nJoined at: <t:{}>\nCreated at: <t:{}>\nNick: {}".format(username, discriminator, id, avatar_url, joined_at, created_at, nick))


	@interactions.extension_command(
		name="get_guild",
		description="None",
		scope=scope,
	)
	async def _get_guild(self, ctx: interactions.CommandContext):
		guild = interactions.Guild(**await self.bot._http.get_guild(ctx.guild_id), _client=self.bot._http)
		user = interactions.User(**await self.bot._http.get_user(guild.owner_id), _client=self.bot._http)
		username = user.username
		discriminator = user.discriminator
		name = guild.name
		id = int(guild.id)
		icon_url = guild.icon_url
		await ctx.send(content="{} ({})\n{}\nOwner: {}#{} ({})".format(name, id, icon_url, username, discriminator, guild.owner_id))



def setup(bot):
	Get_method(bot)
