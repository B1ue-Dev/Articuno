import interactions
from interactions import extension_listener as listener
from interactions import extension_command as command
import os, asyncio
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))


_snipe_message_author = {}
_snipe_message_author_id = {}
_snipe_message_author_avatar_url = {}
_snipe_message_content = {}
_snipe_message_content_id = {}
_snipe_message_attachments = {}





class Snipe(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	

	@listener(name="on_message_delete")
	async def _message_delete(self, message: interactions.Message):
		_message: interactions.Message = self.bot._http.cache.messages.get(str(message.id))
		_channel_id = int(_message.channel_id)

		_snipe_message_author[_channel_id] = str(f"{_message.author}#{_message.author.discriminator}")
		_snipe_message_author_id[_channel_id] = int(_message.author.id)
		_snipe_message_author_avatar_url[_channel_id] = str(_message.author.avatar_url)
		_snipe_message_content[_channel_id] = str(_message.content)
		_snipe_message_content_id[_channel_id] = int(_message.id)
		if _message.attachments is None:
			_snipe_message_attachments[_channel_id] = None
		else:
			_snipe_message_attachments[_channel_id] = str(_message.attachments[0].url)
		await asyncio.sleep(10)
		del _snipe_message_author[_channel_id]
		del _snipe_message_author_id[_channel_id]
		del _snipe_message_author_avatar_url[_channel_id]
		del _snipe_message_content[_channel_id]
		del _snipe_message_content_id[_channel_id]
		del _snipe_message_attachments[_channel_id]

	

	@command(
		name="snipe",
		description="Snipe a deleted message",
		#scope=738938246574374913
	)
	async def _snipe(self, ctx: interactions.CommandContext):
		channel = await ctx.get_channel()
		channel_id = int(channel.id)
		try:
			author = interactions.EmbedAuthor(name=_snipe_message_author[channel_id], icon_url=_snipe_message_author_avatar_url[channel_id])
			footer = interactions.EmbedFooter(name=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}", icon_url=ctx.author.user.avatar_url)
			embed = interactions.Embed(
				description=f"<@{_snipe_message_author_id[channel_id]}> said: {_snipe_message_content[channel_id]}",
				author=author,
				footer=footer
			)
			if str(_snipe_message_attachments[channel_id]) is not None:
				embed.set_thumbnail(url=_snipe_message_attachments[channel_id])
			await ctx.send(embeds=embed)
		except:
			await ctx.send("No message to snipe.", ephemeral=True)






def setup(bot):
	Snipe(bot)