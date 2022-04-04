import interactions
from interactions import Option, OptionType, CommandContext, User, Member
from interactions import extension_command as command
from interactions import extension_component as component
from interactions import extension_listener as listener
import os
from dotenv import load_dotenv
from utils.permission import Permissions, has_permission

load_dotenv()
scope = int(os.getenv("SCOPE"))





class Admin(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	

	@command(
		name="user",
		description="Moderation commands",
		scope=scope,
		options=[
			Option(
				type=OptionType.SUB_COMMAND,
				name="kick",
				description="(Admin only) Kick a user from the server",
				options=[
					Option(
						type=OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					),
					Option(
						type=OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					),
				]
			),
			Option(
				type=OptionType.SUB_COMMAND,
				name="ban",
				description="(Admin only) Ban a user from the server",
				options=[
					Option(
						type=OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					),
					Option(
						type=OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					),
				]
			),
			Option(
				type=OptionType.SUB_COMMAND,
				name="hackban",
				description="(Admin only) Ban a user that is not in the server",
				options=[
					Option(
						type=OptionType.STRING,
						name="id",
						description="Targeted user's ID",
						required=True,
					),
					Option(
						type=OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
						),
				]
			),
		]
	)
	async def user(self, ctx: CommandContext, sub_command: str,
		user: Member = None,
		id: str = None,
		reason: str = None,
	):
		guild = interactions.Guild(**await self.bot._http.get_guild(ctx.guild_id), _client=self.bot._http)
		if sub_command == "kick":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.KICK_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have kick permission.", ephemeral=True)
				return
			else:
				if int(user.user.id) == int(ctx.author.id):
					await ctx.send("You cannot kick yourself.", ephemeral=True)
					return
				else:
					bot = await guild.get_member(member_id=self.bot.me.id)
					role = bot.roles[0]
					role = await guild.get_role(role_id=role)
					perms = role.permissions
					if not (
						has_permission(int(perms), Permissions.KICK_MEMBERS) or
						has_permission(int(perms), Permissions.ADMINISTRATOR)
					):
						await ctx.send(content="You do not have kick permission.", ephemeral=True)
						return
					else:
						if reason is None:
							reason = "No reason provided."
						message = f"{user.user.username}#{user.user.discriminator} was kicked from the server.\nReason: {reason}"
						await user.kick(guild_id=ctx.guild_id, reason=reason)
						await ctx.send(message)
			return
		elif sub_command == "ban":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.BAN_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have ban permission.", ephemeral=True)
				return
			else:
				if int(user.user.id) == int(ctx.author.id):
					await ctx.send("You cannot ban yourself.", ephemeral=True)
					return
				else:
					bot = await guild.get_member(member_id=self.bot.me.id)
					role = bot.roles[0]
					role = await guild.get_role(role_id=role)
					perms = role.permissions
					if not (
						has_permission(int(perms), Permissions.BAN_MEMBERS) or
						has_permission(int(perms), Permissions.ADMINISTRATOR)
					):
						await ctx.send(content="You do not have ban permission.", ephemeral=True)
						return
					else:
						if reason is None:
							reason = "No reason provided."
						message = f"{user.user.username}#{user.user.discriminator} was banned from the server.\nReason: {reason}"
						await user.ban(guild_id=ctx.guild_id, reason=reason)
						await ctx.send(message)
			return
		elif sub_command == "hackban":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.BAN_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have ban permission.", ephemeral=True)
				return
			else:
				if reason is None:
					reason = "No reason provided."
				message = f"User with ID ``{id}`` was banned from the server.\nReason: {reason}"
				await self.bot._http.create_guild_ban(guild_id=ctx.guild_id, user_id=id, reason=reason)
				await ctx.send(message)
			return
		









def setup(bot):
	Admin(bot)
