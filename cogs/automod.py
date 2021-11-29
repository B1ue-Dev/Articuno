import discord
from discord.ext import commands
import urllib.request


class AutoMod(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		message_content = message.content.lower()
		if "@everyone" in message.content or "@here" in message.content:
			if message.author.guild_permissions.administrator:
			# If the user has administrator role (admin or owner), it will not be blocked
				return
			else:
				# If the user doesn't have enough role and try to ping everyone, it will
				# be blocked
				await message.delete()
				await message.channel.send(f"<@{message.author.id}>, don't try to ping everyone.")

		
		# if someone mention the bot
		if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
			await message.send("It seems like you mention me. Use ``/`` to see a list of available commands.")


		# if there is a discord nitro scam link in message content
		with urllib.request.urlopen('https://raw.githubusercontent.com/Jimmy-Blue/discord-scam-links/main/list.txt') as f:
			html = f.read().decode('utf-8')
		message.content = message.content.lower()
		for line in html.splitlines():
			if line in message.content:
				await message.delete()
				await message.channel.send(f"<@{message.author.id}>, sending a scam link is not a good idea.")


		# if there is a server invite link
			message.content = message.content.lower()
			if "discord.gg" in message.content or "discordapp.com/invite" in message.content or "discord.me" in message.content or "discord.io" in message.content or "discord.com/invite" in message.content or "discord.gg/" in message.content:
				if message.author.guild_permissions.administrator:
					return
				else:
					await message.delete()
					await message.channel.send(f"<@{message.author.id}>, sending a server invite link is not allowed.")





def setup(bot):
	bot.add_cog(AutoMod(bot))