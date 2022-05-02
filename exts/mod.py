import interactions
from interactions import extension_command as command
from interactions import extension_component as component
from interactions import extension_listener as listener
import os, datetime
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
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="kick",
				description="(Admin only) Kick a user from the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					),
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="ban",
				description="(Admin only) Ban a user from the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					),
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="hackban",
				description="(Admin only) Ban a user that is not in the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="id",
						description="Targeted user ID",
						required=True,
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					),
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="unban",
				description="(Admin only) Unban a user from the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="id",
						description="Targeted user ID",
						required=True,
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="timeout",
				description="(Admin only) Timeout a user from the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					),
					interactions.Option(
						type=interactions.OptionType.INTEGER,
						name="minutes",
						description="Timeout in how long (minutes). Default to 60 minutes",
						required=True,
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="reason",
						description="Reason",
						required=False,
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="untimeout",
				description="(Admin only) Untimeout a user from the server",
				options=[
					interactions.Option(
						type=interactions.OptionType.USER,
						name="user",
						description="Targeted user",
						required=True,
					)
				]
			)
		]
	)
	async def _user(self, ctx: interactions.CommandContext, sub_command: str,
		user: interactions.Member = None,
		id: str = None,
		reason: str = None,
		minutes: int = None
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
						await ctx.send(content="I do not have kick permission.", ephemeral=True)
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
						await ctx.send(content="I do not have ban permission.", ephemeral=True)
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
				if int(id) == int(ctx.author.id):
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
						await ctx.send(content="I do not have ban permission.", ephemeral=True)
						return
					else:
						if reason is None:
							reason = "No reason provided."
						message = f"User with ID ``{id}`` was banned from the server.\nReason: {reason}"
						await self.bot._http.create_guild_ban(guild_id=ctx.guild_id, user_id=id, reason=reason)
						await ctx.send(message)
			return

		elif sub_command == "unban":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.BAN_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have ban permission.", ephemeral=True)
				return
			else:
				if int(id) == int(ctx.author.id):
					await ctx.send("You cannot unban yourself.", ephemeral=True)
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
						await ctx.send(content="I do not have ban permission.", ephemeral=True)
						return
					else:
						message = f"User with ID ``{id}`` was unbanned from the server."
						await self.bot._http.remove_guild_ban(guild_id=ctx.guild_id, user_id=id)
						await ctx.send(message)
			return
		
		elif sub_command == "timeout":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.MODERATE_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have timeout permission.", ephemeral=True)
				return
			else:
				if int(user.user.id) == int(ctx.author.id):
					await ctx.send("You cannot timeout yourself.", ephemeral=True)
					return
				else:
					bot = await guild.get_member(member_id=self.bot.me.id)
					role = bot.roles[0]
					role = await guild.get_role(role_id=role)
					perms = role.permissions
					if not (
						has_permission(int(perms), Permissions.MODERATE_MEMBERS) or
						has_permission(int(perms), Permissions.ADMINISTRATOR)
					):
						await ctx.send(content="You do not have timeout permission.", ephemeral=True)
						return
					else:
						member = await guild.get_member(member_id=user.user.id)
						if reason is None:
							reason = "No reason provided."
						if minutes is None:
							minutes = 60
						time = datetime.datetime.utcnow()
						time += datetime.timedelta(minutes=minutes)
						message = f"{user.user.username}#{user.user.discriminator} was timed out from the server.\nReason: {reason}"
						await member.modify(guild_id=ctx.guild_id, communication_disabled_until=time.isoformat())
						await ctx.send(message)
						return
		
		elif sub_command == "untimeout":
			if not (
				has_permission(int(ctx.author.permissions), Permissions.MODERATE_MEMBERS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have timeout permission.", ephemeral=True)
				return
			else:
				if int(user.user.id) == int(ctx.author.id):
					await ctx.send("You cannot untimeout yourself.", ephemeral=True)
					return
				else:
					bot = await guild.get_member(member_id=self.bot.me.id)
					role = bot.roles[0]
					role = await guild.get_role(role_id=role)
					perms = role.permissions
					if not (
						has_permission(int(perms), Permissions.MODERATE_MEMBERS) or
						has_permission(int(perms), Permissions.ADMINISTRATOR)
					):
						await ctx.send(content="You do not have timeout permission.", ephemeral=True)
						return
					else:
						member = await guild.get_member(member_id=user.user.id)
						if member.communication_disabled_until is None:
							await ctx.send(content="That user was not timed out.", ephemeral=True)
							return
						else:
							message = f"{user.user.username}#{user.user.discriminator} was untimeout from the server."
							await member.modify(guild_id=ctx.guild_id, communication_disabled_until=None)
							await ctx.send(message)
							return
	

	"""
	@command(
		name="channel",
		description="Channel moderation commands",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="lock",
				description="(Admin only) Lock a channel",
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="unlock",
				description="(Admin only) Unlock a channel",
			)
		]
	)
	async def channel(self, ctx: interactions.CommandContext, sub_command: str):
		if sub_command == "lock":
			channel = await ctx.get_channel()
			if not (
				has_permission(int(ctx.author.permissions), Permissions.MANAGE_CHANNELS) or
				has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
			):
				await ctx.send(content="You do not have channel permission.", ephemeral=True)
				return
			else:
				permission_overwrites = [
					interactions.Overwrite(
						id=int(ctx.guild_id),
						type=0,
						deny=interactions.Permissions.SEND_MESSAGES
					),
				]
				print(channel.permission_overwrites)
				permission_overwrites.extend(interactions.Overwrite())
				await channel.modify(permission_overwrites=permission_overwrites)
				await ctx.send(f"``{channel.name}`` is locked.")
	"""





def setup(bot):
	Admin(bot)
