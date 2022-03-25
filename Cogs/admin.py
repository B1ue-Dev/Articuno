import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash import error as error_cog
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import InteractionContext
from discord_slash.utils.manage_commands import create_option, create_choice
import os, json
from dotenv import load_dotenv
load_dotenv()

guild_ids = os.getenv("GUILD_IDS")
with open ("./data/config.json") as f:
	data = json.load(f)
	blocked_guild = data['BLOCKED_GUILD']


# Excuse me but I am lazy
slash = cog_ext.cog_slash
subcommand = cog_ext.cog_subcommand


# Colors
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868





# Main file
class Admin(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@subcommand(base="user",
				name="kick",
				description="(Admin only) Kick a user from the server",
				options=[
					create_option(name="user",
						description="Targeted user",
						option_type=6,
						required=True),
					create_option(name="reason",
						description="Reason",
						option_type=3,
						required=False)
					]
				)
	async def _kick(self, ctx: SlashContext, user: str, reason: str = None):
		# Get the message
		channel_message = f"{user} was kicked from the server.\nReason: {reason}"
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.kick_members):
				await ctx.send("You do not have permission to do this.", hidden=True)
				return
			else:
				if user == ctx.author:
					await ctx.send("You cannot kick yourself.", hidden=True)
					return
				else:
					try:
						await user.kick(reason=reason)
						await ctx.send(channel_message)
					except discord.Forbidden:
						await ctx.send("I do not have permission to do this.", hidden=True)
						return
	

	@subcommand(base="user",
				name="ban",
				description="(Admin only) Ban a user from the server",
				options=[
					create_option(name="user",
						description="Targeted user",
						option_type=6,
						required=True),
					create_option(name="reason",
						description="Reason",
						option_type=3,
						required=False)
					]
				)
	async def _ban(self, ctx: SlashContext, user: str, reason: str = None):
		# Get the message
		channel_message = f"{user} was banned from the server.\nReason: {reason}"
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.ban_members):
				await ctx.send("You do not have permission to do this.", hidden=True)
				return
			else:
				if user == ctx.author:
					await ctx.send("You cannot ban yourself.", hidden=True)
					return
				else:
					try:
						await user.ban(reason=reason)
						await ctx.send(channel_message)
					except discord.Forbidden:
						await ctx.send("I do not have permission to do this.", hidden=True)
						return
	

	@subcommand(base="user",
				name="hackban",
				description="(Admin only) Ban a user that is not in the current server",
				options=[
					create_option(name="id",
						description="Targeted user ID",
						option_type=3,
						required=True),
					create_option(name="reason",
						description="Reason",
						option_type=3,
						required=False)
					]
				)
	async def _hackban(self, ctx: SlashContext, id: str, reason: str = None):
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.ban_members):
				await ctx.send("You do not have permission to do this.", hidden=True)
			else:
				if id == ctx.author.id:
					await ctx.send("You cannot ban yourself.", hidden=True)
					return
				else:
					try:
						await self.bot.http.ban(id, int(ctx.guild.id), 0, reason=reason)
						await ctx.send(f'User with ID ``{id}`` was banned from the server.')
					except discord.NotFound:
						await ctx.send(f'I cannot find any user with the ID ``{id}``.', hidden=True)
					except discord.errors.Forbidden:
						await ctx.send(f"I do not have permission to do this.", hidden=True)
	

	@subcommand(base="user",
				name="unban",
				description="(Admin only) Unban a user from the server",
				options=[
					create_option(name="id",
						description="Targeted user ID",
						option_type=3,
						required=True)
					]
				)
	async def _unban(self, ctx: SlashContext, id: str):
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.ban_members):
				await ctx.send("You do not have permission to do this.", hidden=True)
			else:
				if id == ctx.author.id:
					await ctx.send("You cannot unban yourself.", hidden=True)
					return
				else:
					try:
						await self.bot.http.unban(ctx.guild.id, id)
						await ctx.send(f'User with ID ``{id}`` was unbanned from the server.')
					except discord.NotFound:
						await ctx.send(f'I cannot find any user with the ID ``{id}``.', hidden=True)
					except discord.errors.Forbidden:
						await ctx.send(f"I do not have permission to do this.", hidden=True)
	

	@subcommand(base="user",
				name="mute",
				guild_ids=[859030372783751168],
				description="(Admin only) Mute a user from the server",
				options=[
					create_option(name="user",
						description="Targeted user",
						option_type=6,
						required=True),
					create_option(name="reason",
						description="Reason",
						option_type=3,
						required=False)
					]
				)
	async def _mute(self, ctx: SlashContext, user: str, reason: str = None):
		# Get the mute role
		mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
		# Get the user permissions
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.manage_messages):
			await ctx.send("You do not have permission to do this.", hidden=True)
		else:
			if user == ctx.author:
				await ctx.send("You cannot mute yourself.", hidden=True)
			else:
				try:
					await user.add_roles(mute_role)
					await ctx.send(f'{user} was muted.\nReason: {reason}')
				except discord.Forbidden:
					await ctx.send("I do not have permission to do this.", hidden=True)


	@subcommand(base="user",
				name="unmute",
				guild_ids=[859030372783751168],
				description="(Admin only) Unmute a user from the server",
				options=[
					create_option(name="user",
						description="Targeted user",
						option_type=6,
						required=True)
					]
				)
	async def _unmute(self, ctx: SlashContext, user: str):
		# Get the mute role
		mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
		# Get the user permissions
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.manage_messages):
			await ctx.send("You do not have permission to do this.", hidden=True)
		else:
			if user == ctx.author:
				await ctx.send("You cannot unmute yourself.", hidden=True)
			else:
				try:
					await user.remove_roles(mute_role)
					await ctx.send(f'{user} was unmuted.')
				except discord.Forbidden:
					await ctx.send("I do not have permission to do this.", hidden=True)


	@slash(name="lock",
		description="(Admin only) Lock a channel",
		options=[
			create_option(
				name="channel",
				description="Targeted channel",
				option_type=7,
				required=False)
			]
		)
	async def _lock(self, ctx: SlashContext, channel: str = None):
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			if channel is None:
				channel = ctx.channel
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.manage_messages):
				await ctx.send("You do not have permission to do this.", hidden=True)
				return
			else:
				channel = channel or ctx.channel
				overwrite = channel.overwrites_for(ctx.guild.default_role)
				overwrite.send_messages = False
				try:
					await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
					await ctx.send(f'``{channel}`` was locked.')
				except discord.Forbidden:
					await ctx.send("I do not have permission to do this.", hidden=True)
					return


	@slash(name="unlock",
		description="(Admin only) Unlock a channel",
		options=[
			create_option(
				name="channel",
				description="Targeted channel",
				option_type=7,
				required=True)
			]
		)
	async def _unlock(self, ctx: SlashContext, channel: str = None):
		if int(ctx.guild.id) in blocked_guild:
			return
		else:
			if channel is None:
				channel = ctx.channel
			# Get the user permissions
			perms = ctx.author.guild_permissions
			if not (perms.administrator or perms.manage_messages):
				await ctx.send("You do not have permission to do this.", hidden=True)
				return
			else:
				channel = channel or ctx.channel
				overwrite = channel.overwrites_for(ctx.guild.default_role)
				overwrite.send_messages = True
				try:
					await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
					await ctx.send(f"``{channel}`` was unlocked.")
				except discord.Forbidden:
					await ctx.send("I do not have permission to do this.", hidden=True)
					return




def setup(bot):
	bot.add_cog(Admin(bot))
