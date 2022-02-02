import discord
from discord.ext import commands
import urllib.request


# Excuse me but I am lazy
listener = commands.Cog.listener


# Color
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868





class Automod(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	

	@listener()
	async def on_message(self, message):
		message.content = message.content.lower()

		# If @everyone or @here mention in the message
		if "@everyone" in message.content or "@here" in message.content:
			if message.author.guild_permissions.kick_members:
				return
			else:
				await message.delete()
				await message.channel.send(f"<@{message.author.id}>, it is better not to ping everyone.")


		# If someone sends a scam link
		with urllib.request.urlopen('https://raw.githubusercontent.com/Jimmy-Blue/discord-scam-links/articuno/list.txt') as f:
			html = f.read().decode('utf-8')
		message.content = message.content.lower()
		for line in html.splitlines():
			if line in message.content:
				if message.author.guild_permissions.administrator:
					await message.delete()
				else:
					await message.delete()
					await message.channel.send(f"<@{message.author.id}>, it is better not to send a scam link.")


		# If someone sends an invite link
		if message.guild.id == 859030372783751168:
			message.content = message.content.lower()
			if "discord.gg" in message.content or "discordapp.com/invite" in message.content or "discord.me" in message.content or "discord.io" in message.content or "discord.com/invite" in message.content or "discord.gg/" in message.content:
				if message.author.guild_permissions.administrator:
					return
				else:
					await message.delete()
					await message.channel.send(f"<@{message.author.id}>, sending a server invite link is not allowed.")



def setup(bot):
	bot.add_cog(Automod(bot))
