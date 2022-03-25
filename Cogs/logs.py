from statistics import median
import discord
from discord.ext import commands
from discord.utils import find
import random
from datetime import datetime
import json



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



# Again, I am lazy
listener = commands.Cog.listener


class Logs(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@listener()
	async def on_member_join(self, member):
		guild = member.guild
		# Welcome channel
		welcome1 = discord.utils.get(guild.channels, name="welcome-goodbye")
		# Log channel
		log = discord.utils.get(guild.channels, name="logs")
		# Welcome role
		memberRole1 = discord.utils.get(guild.roles, name="👤 Member")
		#memberRole2 = discord.utils.get(guild.roles, name="Simp")
		# Embed message in welcome channel
		join = discord.Embed(color=random.randint(0, 0xFFFFFF))
		join.set_thumbnail(url=member.avatar_url)
		join.set_footer(text=f"Member ID: {member.id}")
		join.add_field(name="Welcome :partying_face:", value=f"Welcome to {guild.name}, **{member.name}**", inline=False)
		# Embed message in log channel
		logger = discord.Embed(title="Member joined", color=random.randint(0, 0xFFFFFF))
		logger.set_thumbnail(url=member.avatar_url)
		logger.set_footer(text=f"Member ID: {member.id}")
		logger.add_field(name="Member's name", value=f"{str(member)}\n<@!{member.id}>", inline=True)
		logger.add_field(name="Member's ID", value=f"{member.id}", inline=True)
		logger.add_field(name="Joined on", value=member.joined_at.strftime("%B %d, %Y\n%H:%M:%S"), inline=False)
		logger.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y\n%H:%M:%S"), inline=False)
		try:
			await member.add_roles(memberRole1)
		except:
			pass
		try:
			await welcome1.send(embed=join)
		except:
			pass
		try:
			await log.send(embed=logger)
		except:
			pass


	@listener()
	async def on_member_remove(self, member):
		guild = member.guild
		now = datetime.now()
		# Goodbye channel
		bye1 = discord.utils.get(guild.channels, name="welcome-goodbye")
		# Log channel
		log = discord.utils.get(guild.channels, name="logs")
		# Embed message in goodbye channel
		left = discord.Embed(color=random.randint(0, 0xFFFFFF))
		left.set_thumbnail(url=member.avatar_url)
		left.set_footer(text=f"Member ID: {member.id}")
		left.add_field(name="Goodbye :cry:", value=f"Goodbye, **{member.name}**. Thanks for joining {guild.name}", inline=False)
		# Embed message in log channel
		logger = discord.Embed(title="Member left", color=random.randint(0, 0xFFFFFF))
		logger.set_thumbnail(url=member.avatar_url)
		logger.set_footer(text=f"Member ID: {member.id}")
		logger.add_field(name="Member's name", value=f"{str(member)}\n<@!{member.id}>", inline=True)
		logger.add_field(name="Member's ID", value=f"{member.id}", inline=True)
		logger.add_field(name="Left on", value=now.strftime("%B %d, %Y\n%H:%M:%S"), inline=False)
		logger.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y\n%H:%M:%S"), inline=False)
		try:
			await bye1.send(embed=left)
		except:
			pass
		try:
			await log.send(embed=logger)
		except:
			pass


	@listener()
	async def on_message_delete(self, message):
		guild = message.guild
		try:
			log = discord.utils.get(guild.channels, name="logs")
			embed = discord.Embed(timestamp=message.created_at, color=red)
			embed.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.avatar_url)
			embed.set_footer(text=f"Author ID: {message.author.id} • Message ID: {message.id}")
			embed.add_field(name="**Member**", value=f"<@{message.author.id}>", inline=True)
			embed.add_field(name="**Channel**", value=f"<#{message.channel.id}>", inline=True)
			embed.add_field(name="**Deleted message content**", value=message.content, inline=False)
			await log.send(embed=embed)
		except AttributeError:
			ids = str(guild.id)
			if ids == "946606961594597376":
				embed1 = discord.Embed(description=f"{message.author.mention} said: {message.content}")
				embed1.set_author(name=f"{message.author}", url=f"{message.author.avatar_url}")
				try:
					for attachment in message.attachments:
					#embed.add_field(name="Attachments", value=f"[{attachment.filename}]({attachment.url})")
						embed1.set_image(url=attachment.url)
				except:
					pass
				await message.channel.send(embed=embed1)


	@listener()
	async def on_message_edit(self, before, after):
		guild = before.guild
		log = discord.utils.get(guild.channels, name="logs")
		embed = discord.Embed(timestamp=before.created_at, colour=red) 
		embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
		embed.set_footer(text=f"Author ID: {before.author.id} • Message ID: {before.id}")
		embed.add_field(name="**Member**", value=f"<@{before.author.id}>", inline=True)
		embed.add_field(name="**Channel**", value=f"<#{before.channel.id}>", inline=True)
		embed.add_field(name="**Message content before edited**", value=before.content, inline=False)
		embed.add_field(name="**Message content after edited**", value=after.content, inline=False)
		try:
			await log.send(embed=embed)
		except discord.errors.Forbidden:
			return # Bot does not have enough permission (plus, this is meant to work with only Pokemon Hangout and mine)


	# Real work start here
	@listener()
	async def on_guild_join(self, guild):
		general = find(lambda x: x.name == ['general', 'bot', 'chat'],  guild.text_channels)
		if general and general.permissions_for(guild.me).send_messages:
			await general.send(f'Hello there, {format(guild.name)}. Thanks for inviting me to your server.\n\nUse **$help** for a list of available commands. Alternatively, you can use "/" and choose Articuno to see the list.')
		# Development channel (Pokemon Hangout)
		now = datetime.now()
		current_time = now.strftime("%B %d, %Y\n%H:%M:%S")
		# Guild data
		member = guild.member_count
		name = guild.name
		id = guild.id
		owner = guild.owner
		# Format the message to be sent
		development2 = await self.bot.fetch_channel(str(906232173684744222))
		embed2 = discord.Embed(title=f"Joined {name}", color=blue)
		embed2.set_thumbnail(url=guild.icon_url)
		embed2.add_field(name="Member", value=member)
		embed2.add_field(name="Created on", value=str(guild.created_at.strftime("%B %d, %Y\n%H:%M:%S")))
		embed2.add_field(name="Joined on", value=str(current_time))
		embed2.add_field(name=f"Server ID", value=id)
		embed2.add_field(name="Owner", value=owner)
		await development2.send(embed=embed2)


	@listener()
	async def on_guild_remove(self, guild):
		now = datetime.now()
		current_time = now.strftime("%B %d, %Y\n%H:%M:%S")
		development2 = await self.bot.fetch_channel(str(906232173684744222))
		embed2 = discord.Embed(title=f"Left {guild.name}", color=blue)
		embed2.set_thumbnail(url=guild.icon_url)
		embed2.add_field(name=f"Server ID", value=guild.id)
		embed2.add_field(name="Owner", value=guild.owner)
		embed2.add_field(name="Left on", value=str(current_time))
		await development2.send(embed=embed2)






def setup(bot):
	bot.add_cog(Logs(bot))
