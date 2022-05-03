import interactions
from interactions import extension_listener as listener
import datetime, random


class Logs(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	

	@listener(name="on_message_delete")
	async def _message_delete(self, message: interactions.Message):
		_message: interactions.Message = self.bot._http.cache.messages.get(str(message.id))
		channel = interactions.Channel(**await self.bot._http.get_channel(862636687226044436), _client=self.bot._http)

		if _message is not None:
			author = interactions.EmbedAuthor(name=f"{_message.author.username}#{_message.author.discriminator}", icon_url=_message.author.avatar_url)._json
			footer = interactions.EmbedFooter(text=f"Message ID: {_message.id}")._json
			fields = [
				interactions.EmbedField(name="Member", value=f"{_message.member.mention}", inline=True),
				interactions.EmbedField(name="Channel", value=f"<#{_message.channel_id}>", inline=True),
				interactions.EmbedField(name="Deleted message content", value=f"{_message.content}", inline=False),
			]
			embed = interactions.Embed(
				color=0xe03c3c,
				author=author,
				footer=footer,
				timestamp=datetime.datetime.utcnow(),
				fields=fields
			)

			await channel.send(embeds=embed)



	"""
	#TODO: Working on this later.
	@listener(name="on_guild_create")
	async def _guild_create(self, guild: interactions.Guild):
		#channel = interactions.Channel(**await self.bot._http.get_channel(957090401418899526), _client=self.bot._http)
		_guild: interactions.Guild = self.bot._http.cache.guilds.get(int(guild.id))
		print(f"Joined guild {_guild}")
	"""


	@listener(name="on_guild_member_add")
	async def _guild_member_add(self, member: interactions.GuildMember):
		if int(member.guild_id) == int(738938246574374913):
			guild = interactions.Guild(**await self.bot._http.get_guild(int(member.guild_id)), _client=self.bot._http)
			channel = interactions.Channel(**await self.bot._http.get_channel(862636687226044436), _client=self.bot._http)
			embed = interactions.Embed(
				title="Welcome! 🥳",
				description=f"Welcome to {guild.name}, **{member.user.username}#{member.user.discriminator}**! We hope you have a good time here.",
				color=random.randint(0, 0xFFFFFF),
				timestamp=member.joined_at,
				footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
				thumbnail=interactions.EmbedImageStruct(url=member.user.avatar_url)._json,
			)
			await channel.send(embeds=embed)
		else:
			return
	

	@listener(name="on_guild_member_remove")
	async def _guild_member_remove(self, member: interactions.GuildMember):
		if int(member.guild_id) == int(738938246574374913):
			guild = interactions.Guild(**await self.bot._http.get_guild(int(member.guild_id)), _client=self.bot._http)
			channel = interactions.Channel(**await self.bot._http.get_channel(862636687226044436), _client=self.bot._http)
			embed = interactions.Embed(
				title="Goodbye! 😢",
				description=f"Goodbye **{member.user.username}#{member.user.discriminator}**! Thanks for joining {guild.name}.",
				color=random.randint(0, 0xFFFFFF),
				timestamp=datetime.datetime.utcnow(),
				footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
				thumbnail=interactions.EmbedImageStruct(url=member.user.avatar_url)._json,
			)
			await channel.send(embeds=embed)
		else:
			return






def setup(bot):
	Logs(bot)