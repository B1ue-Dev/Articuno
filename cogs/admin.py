import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
import random
import json
import time
import asyncio




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



class Admin(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	guild_ids = [833886728259239968, 859030372783751168, 738938246574374913]


	@cog_ext.cog_subcommand(base="user", name="info", description="(Admin only) Check the information about a user")
	async def _info(self, ctx: SlashContext, member: discord.Member):
		profile = member.public_flags
		# Check hypesquad
		hypesquad = "None"
		if profile.hypesquad_bravery == True:
			hypesquad = "Bravery"
		if profile.hypesquad_brilliance == True:  
			hypesquad = "Brilliance"        
		if profile.hypesquad_balance == True:
			hypesquad = "Ballance"
        # Check if early supporter
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
        # Message
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
		# Check permission
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.kick_members):
			await ctx.send("You don't have permission to use this command.", hidden=True)
            # hidden = True is hiding the message that only the user can see the output (message)
		else:
			await ctx.send(embed=embed, hidden=True)


	@cog_ext.cog_subcommand(base="user", name="kick", description="(Admin only) Kick a member")
	async def _kick(self, ctx: SlashContext, member: discord.Member, reason = None):
		# Message to kicked member
		member_message = discord.Embed(title=f"You have been kicked in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)
		# Message in channel
		channel_message = discord.Embed(title=f"{member} is kicked", description=f"Reason: {reason}", color=red)
        # Check permission
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.kick_members):
			await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			if member == ctx.author:
				await ctx.send("You cannot kick yourself.", hidden=True)
			else:
				try:
					await member.send(embed=member_message)
				except:
                    # pass if member has Direct Message closed
					pass
				await member.kick(reason=reason)
				await ctx.send(embed=channel_message)


	@cog_ext.cog_subcommand(base="user", name="ban", description="(Admin only) Ban a user")
	async def _ban(self, ctx: SlashContext, member: discord.Member, reason = None):
		# Message to banned member
		member_message = discord.Embed(title=f"You have been banned in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)
		# Message in channel
		channel_message = discord.Embed(title=f"{member} is banned.", description=f"Reason: {reason}", color=red)
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.ban_members):
			await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			if member == ctx.author:
				await ctx.send("You cannot ban yourself.", hidden=True)
			else:
				try:
					await member.send(embed=member_message)
				except:
					pass
				await member.ban(reason=reason, delete_message_days=0)
                # delete_message_days = 0 is for not deleting any previous message when banning the member
                # usually, messages within 1 day will be deleted. You can choose to delete with a range from 0 to 7 days
				await ctx.send(embed=channel_message)


	@cog_ext.cog_subcommand(base="user", name="unban", description="(Admin only) Unban a user")
	async def _unban(self, ctx: SlashContext, id):
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.ban_members):
			await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			user = await self.bot.fetch_user(id)
			await ctx.guild.unban(user)
			embed = discord.Embed(description="Member is unbanned.", color=yellow)
			await ctx.send(embed=embed)


	@cog_ext.cog_slash(name="lock", description="(Admin only) Lock the current channel")
	async def _lock(self, ctx: SlashContext, channel : discord.TextChannel):
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.manage_messages):
			await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			channel = channel or ctx.channel
			overwrite = channel.overwrites_for(ctx.guild.default_role)
			overwrite.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
			await ctx.send(f'``{channel}`` is locked.')


	@cog_ext.cog_slash(name="unlock", description="(Admin only) Unlock the current channel")
	async def _unlock(self, ctx: SlashContext, channel : discord.TextChannel):
		perms = ctx.author.guild_permissions
		if not (perms.administrator or perms.manage_messages):
			await ctx.send("You don't have permission to do this.", hidden=True)
		else:
			channel = channel or ctx.channel
			overwrite = channel.overwrites_for(ctx.guild.default_role)
			overwrite.send_messages = True
			message = await ctx.send(f'``{channel}`` is being unlocked.')
			await asyncio.sleep(2)
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
			await message.edit(content=f"``{channel}`` is unlocked.")


	@cog_ext.cog_slash(name="clean", description="(Admin only) Purge an amount of messages (default: 5)")
	async def _clean(self, ctx: SlashContext, amount = int(5)):
		perms = ctx.author.guild_permissions
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





def setup(bot):
	bot.add_cog(Admin(bot))