import interactions
from interactions import extension_listener as listener
import datetime, random


class Automod(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot


	@listener(name="on_message_create")
	async def _message_create(self, message: interactions.Message):
		if message.guild_id == 738938246574374913 and message.guild_id is not None:
			message_content = message.content.lower()

			# If someone sends an invite link
			if "discord.gg/" in message_content or "discordapp.com/invite" in message_content or "discord.com/invite" in message_content:
				await message.delete()
				await message.get_channel().send(f"{message.member.mention} Your message was deleted because it contained an unauthorized invite link.")




def setup(bot):
	Automod(bot)
