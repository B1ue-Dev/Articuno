import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import asyncio
from typing import Union
import requests
import random

snipe_message_author = {}
snipe_message_author_id = {}
snipe_message_content = {}
snipe_message_content_id = {}
snipe_message_attachments = {}


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


# Lazy, excuse me
listener = commands.Cog.listener
slash = cog_ext.cog_slash
subcommand = cog_ext.cog_subcommand





class Server(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	guild_ids = [833886728259239968, 859030372783751168, 738938246574374913]


	@slash(name="clean",
		description="(Admin only) Purge an amount of messages (default: 5)",
		)
	async def _clean(self, ctx: SlashContext, amount = int(5)):
		perms = ctx.author.guild_permissions
		try:
			channel_perms = ctx.channel.permissions_for(ctx.author)
		except AttributeError:
			pass
		try:
			if not (perms.administrator or perms.manage_messages or channel_perms.manage_messages):
				await ctx.send("You don't have permission to do this.", hidden=True)
		except:
			if not (perms.administrator or perms.manage_messages):
				await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			if int(amount) >= int(101):
				await ctx.send("The limit is 100 messages per time.", hidden=True)
			else:
				await ctx.channel.purge(limit=int(amount), bulk=True)
				message0 = await ctx.send(f"{amount} messages have been deleted. This message will be deleted after 3 seconds")
				await asyncio.sleep(3)
				await message0.delete()

	# Legacy, will be removed in the future
	@commands.command(aliases=['purge', 'delete', 'del'])
	@commands.has_permissions(manage_messages=True)
	async def clean(self, ctx, amount=5):
		'''
		if amount >= 101:
			await ctx.send("Uh, I only allow you to delete 100 messages a time.")
		else:
			await ctx.message.delete()
			await ctx.channel.purge(limit=amount, bulk=True)
			message0 = await ctx.send(f"{amount} messages have been deleted. This message will be deleted after 3 seconds.")
			await asyncio.sleep(3)
			await message0.delete()
		'''
		await ctx.send(f"``$clean`` has moved to ``/clean``. Use that instead.")


	@commands.command()
	@commands.has_permissions(manage_emojis=True)
	async def emojisteal(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji], name=None):
		if not name:
			name = emoji.name
		try:
			await ctx.guild.create_custom_emoji(name=name, image=await emoji.url.read())
			await ctx.send(f"Successfully added the emoji ``[:{name}:]``")
		except:
			await ctx.send(f"Your server has maxed out emoji slot. I cannot add any more emoji.")


	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_emojis=True)
	async def emojiadd(self, ctx, url, name):
		try:
			response = requests.get(url)
		except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
			return await ctx.send("The URL you have provided is invalid.")
		if response.status_code == 404:
			return await ctx.send("The URL you have provided leads to a 404.")
		try:
				await ctx.guild.create_custom_emoji(name=name, image=response.content)
				await ctx.send(f"Successfully added the emoji ``[:{name}:]``")
		except discord.InvalidArgument:
				return await ctx.send("Invalid image type. Only PNG, JPEG and GIF are supported.")

	
	@commands.command(aliases=['emoji'])
	async def emojiurl(self, ctx, emoji: discord.Emoji):
		embed = discord.Embed(title=f"``<:{emoji.name}:{emoji.id}>``", description=f"[Emoji link]({emoji.url})" ,color = random.randint(0, 0xFFFFFF))
		image = emoji.url
		embed.set_image(url=image)
		await ctx.send(f"<{image}>")
		await ctx.send(embed=embed)


	@commands.command(name="emojidelete", aliases=['emojiremove'])
	@commands.guild_only()
	@commands.has_permissions(manage_emojis=True)
	async def deleteemoji(self, ctx, *emojis: discord.Emoji):
		'''
		guild = ctx.guild
		if ctx.author.guild_permissions.manage_emojis:
			if emoji.guild_id != ctx.guild.id:
				await ctx.send("That emoji is not from this server.")
			else:
				await ctx.send(f'Successfully deleted (or not): ``[:{emoji.name}:]``')
				await emoji.delete()
		else:
			await ctx.send("You do not have permission to do this.")
		'''
		if ctx.author.guild_permissions.manage_emojis:
			for emoji in emojis:
				if emoji.guild_id != ctx.guild.id:
					await ctx.send("That emoji is not from this server.")
				else:
					await ctx.send(f"Successfully deleted the emoji ``[:{emoji.name}:{emoji.id}]``")
					await emoji.delete()
		else:
			await ctx.send("You do not have permission to do this.")


	# Snipe deleted message in channel
	@listener()
	async def on_message_delete(self, message):
		snipe_message_author[message.channel.id] = message.author
		snipe_message_author_id[message.channel.id] = message.author.id
		snipe_message_content[message.channel.id] = message.content
		snipe_message_content_id[message.channel.id] = message.id
		snipe_message_attachments[message.channel.id] = message.attachments
		await asyncio.sleep(120)
		del snipe_message_author[message.channel.id]
		del snipe_message_author_id[message.channel.id]
		del snipe_message_content[message.channel.id]
		del snipe_message_content_id[message.channel.id]
		del snipe_message_attachments[message.channel.id]

	@commands.command()
	async def snipe(self, ctx):
		'''
		channel = ctx.channel
		try:
			embed = discord.Embed(description=f"<@!{snipe_message_author_id[channel.id]}> said: {snipe_message_content[channel.id]}")
			embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_author(name= f"{snipe_message_author[channel.id]}")
			try:
				for attachment in snipe_message_attachments[channel.id]:
					#embed.add_field(name="Attachments", value=f"[{attachment.filename}]({attachment.url})")
					embed.set_thumbnail(url=attachment.url)
			except:
				pass
			await ctx.send(embed=embed)
		except: 
			await ctx.send(f"There are no recently deleted messages in <#{channel.id}>.")
		'''
		await ctx.send(f"``$snipe`` has moved to ``/snipe``. Use that instead.")


	@slash(name="snipe",
		description="Snipe the last deleted message in the channel",
		)
	async def _snipe(self, ctx: SlashContext):
		channel = ctx.channel
		try:
			embed = discord.Embed(description=f"<@!{snipe_message_author_id[channel.id]}> said: {snipe_message_content[channel.id]}")
			embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
			embed.set_author(name= f"{snipe_message_author[channel.id]}")
			try:
				for attachment in snipe_message_attachments[channel.id]:
					#embed.add_field(name="Attachments", value=f"[{attachment.filename}]({attachment.url})")
					embed.set_thumbnail(url=attachment.url)
			except:
				pass
			await ctx.send(embed=embed)
		except: 
			await ctx.send(f"There are no recently deleted messages in <#{channel.id}>.")






def setup(bot):
	bot.add_cog(Server(bot))
