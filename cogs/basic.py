import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
import aiohttp
import requests
import asyncio
import platform
import json
import time
import random




#color
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868




class Stats(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_command(self,ctx):
		self.api.command_run(ctx)
def setup(bot):
	bot.add_cog(Stats(bot))


class Basic(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	guild_ids = [833886728259239968, 859030372783751168]


	#commands
	@cog_ext.cog_slash(name="ping", description="Ping the bot")
	async def _ping(self, ctx: SlashContext):
		websocket = f"{self.bot.latency * 1000:.0f}"
		if int(websocket) < int(99):
			message = f"{websocket}ms 🟢"
		elif int(100) <= int(websocket) < int(199):
			message = f"{websocket}ms 🟡"
		elif int(websocket) > int(200):
			message = f"{websocket}ms 🔴"
		embed = discord.Embed(title=":ping_pong: Pong!", description=f"Websocket: {message}", color=orange)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed.embed)


	@cog_ext.cog_slash(name="stats", description="See Articuno stats")
	async def _stats(self, ctx: SlashContext):
		async with aiohttp.ClientSession():
			python = platform.python_version()
			discordpy = discord.__version__
			latency = f"{self.bot.latency * 1000:.0f}"
			os = str(platform.platform())
			embed=discord.Embed(title="Articuno Stats", color=blue)
			embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/782628076503957524/10ca66e0b32229c171a26d35e53f342b.png?size=256')
			embed.add_field(name="Server Count", value=len(self.bot.guilds))
			embed.add_field(name="User Count", value=len(self.bot.users))
			embed.add_field(name="Python", value=python)
			embed.add_field(name="discord.py", value=discordpy)
			embed.add_field(name="Latency", value=latency)
			embed.add_field(name="Operating System", value=os)
			embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
			await ctx.send(embed=embed)


	# Base: info
	# Subcommand: user
	@cog_ext.cog_subcommand(base="info", name="user", description="Check the informaion about a user")
	async def _info(self, ctx: SlashContext, member : discord.Member = None):
		if not member:
			member = ctx.author
		profile = member.public_flags
		# Check hypesquad
		hypesquad = "None"
		if profile.hypesquad_bravery == True:
			hypesquad = "Bravery"
		if profile.hypesquad_brilliance == True:  
			hypesquad = "Brilliance"        
		if profile.hypesquad_balance == True:
			hypesquad = "Ballance"
        # Check if supporter
		supporter = "No"
		if profile.early_supporter == True:
			supporter = "Yes"
		# Check if bot
		if not member.bot:
			bot = "No"
		else:
			bot = "Yes"
		# Highest role's color
		color = member.top_role.color
		embed=discord.Embed(title=f"{member.name}'s' informaion", colour=color)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_author(name=f"{member}", icon_url=member.avatar_url)
		embed.add_field(name="Name", value=member, inline=True)
		embed.add_field(name="Nickname", value=member.nick, inline=True)
		embed.add_field(name="ID", value=member.id, inline=True)
		embed.add_field(name="Joined on", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
		embed.add_field(name="Top role", value=f"<@&{member.top_role.id}>", inline=True)
		embed.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y"), inline=True)
		embed.add_field(name="Hypesquad", value=f"{hypesquad}")
		embed.add_field(name="Bot?", value=bot)
		embed.add_field(name="Early Supporter?", value=supporter)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)
	# Subcommand: avatar
	@cog_ext.cog_subcommand(base="info", name="avatar", description="Check the profile picture of a user")  
	async def _avatar(self, ctx: SlashContext, *,  avamember : discord.Member = None):
		if not avamember:
			avamember = ctx.author
		avatar = avamember.avatar_url
		member = avamember.name
		embed = discord.Embed(description=f"**Avatar**", color=random.randint(0, 0xFFFFFF))
		embed.set_author(name=member, icon_url=avatar)
		embed.set_image(url=avatar)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)
	# Subcommand: server
	@cog_ext.cog_subcommand(base="info", name="server", description="Check the infomation about the server")
	async def _server(self, ctx: SlashContext):
		name = str(ctx.guild.name)
		id = str(ctx.guild.id)
		memberCount = str(ctx.guild.member_count)
		# Check the number of real user (human) and bot
		memberer = 0
		for member in ctx.guild.members:
			if not member.bot:
				memberer += 1
			if ctx.invoked_subcommand is None:
				bots = sum(1 for member in ctx.guild.members if member.bot)
		icon = str(ctx.guild.icon_url)
		owner = ctx.guild.owner
		region = str(ctx.guild.region)
		created = str(ctx.guild.created_at.strftime("%B %d, %Y"))
		# Check the number of boost
		boost = ctx.guild.premium_subscription_count
		if boost <= 2:
			comment = "Level 0"
		if 2 <= boost < 15:
			comment = "Level 1"
		if 15 <= boost < 30:
			comment = "Level 2"
		if boost >= 30:
			comment = "Level 3"
		text_channel = len(ctx.guild.text_channels)
		voice_channel = len(ctx.guild.voice_channels)
		verify_level = ctx.guild.verification_level
		role_number = len(ctx.guild.roles)
		embed = discord.Embed(title=name, color=blue)
		embed.set_thumbnail(url=icon)
		embed.add_field(name="ID", value=id, inline=True)
		embed.add_field(name="Owner", value=f"<@{owner.id}>\nID: {owner}", inline=True)
		embed.add_field(name="Boost", value=f"Number: {boost}\n{comment}",inline=True)
		embed.add_field(name="Member", value=f"Total: {memberCount}\nHumans: {memberer}\nBOTs: {bots}", inline=True)
		embed.add_field(name="Channels", value=f"<:text_channel:873442091424944178>Text channels: {text_channel}\n<:voice_channel:873442207758159904>Voice channels: {voice_channel}")
		embed.add_field(name="Region", value=region, inline=True)
		embed.add_field(name="Created on", value=created, inline=True)
		embed.add_field(name="Verify level", value=f"Level: {verify_level}")
		embed.add_field(name="Roles", value=role_number)
		embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
		await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(Basic(bot))