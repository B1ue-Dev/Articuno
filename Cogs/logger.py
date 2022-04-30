import interactions
from interactions import extension_listener as listener
import datetime


class Logs(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	
	@listener(name="on_message_create")
	async def _message_create(self, message: interactions.Message):
		print(f"{message.author.username}#{message.author.discriminator} said: {message.content}")


	@listener(name="on_guild_create")
	async def _guild_create(self, guild: interactions.Guild):
		channel = interactions.Channel(**await self.bot._http.get_channel(957090401418899526), _client=self.bot._http)
		print(f"Joined guild {guild.name}")
	

	@listener(name="on_guild_member_add")
	async def _guild_member_add(self, member: interactions.GuildMember):
		if int(member.guild_id) == int(738938246574374913):
			guild = interactions.Guild(**await self.bot._http.get_guild(member.guild_id), _client=self.bot._http)
			channel = interactions.Channel(**await self.bot._http.get_channel(862636687226044436), _client=self.bot._http)
			embed = interactions.Embed(
				title="Welcome! 🥳",
				description=f"Welcome to {guild.name}, **{member.user.username}#{member.user.discriminator}**!",
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
			guild = interactions.Guild(**await self.bot._http.get_guild(member.guild_id), _client=self.bot._http)
			channel = interactions.Channel(**await self.bot._http.get_channel(862636687226044436), _client=self.bot._http)
			embed = interactions.Embed(
				title="Goodbye! 😢",
				description=f"Goodbye **{member.user.username}#{member.user.discriminator}**. Thanks for joining {guild.name}.",
				timestamp=datetime.datetime.utcnow(),
				footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
				thumbnail=interactions.EmbedImageStruct(url=member.user.avatar_url)._json,
			)
			await channel.send(embeds=embed)
		else:
			return






def setup(bot):
	Logs(bot)