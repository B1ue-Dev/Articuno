"""
This module is for moderation commands.

(C) 2022 - Jimmy-Blue
"""

import datetime
import interactions
from utils.permission import Permissions, has_permission


class Admin(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_command(
        name="user",
        description="Moderation commands",
        default_member_permissions=interactions.Permissions.KICK_MEMBERS,
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
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="Reason",
                        required=False
                    )
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
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="Reason",
                        required=False
                    )
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
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="Reason",
                        required=False
                    )
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
                        required=True
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
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="minutes",
                        description="Timeout in how long (minutes). Default to 60 minutes",
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="Reason",
                        required=False
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
        ],
        dm_permission=False
    )
    async def _user(self, ctx: interactions.CommandContext, sub_command: str,
        user: interactions.Member = None,
        id: str = None,
        reason: str = None,
        minutes: int = None
    ):
        guild = await ctx.get_guild()

        if sub_command == "kick":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.KICK_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have kick permission.", ephemeral=True)

            if int(user.user.id) == int(ctx.member.id):
                return await ctx.send("You cannot kick yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.KICK_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="I do not have kick permission.", ephemeral=True)
            if reason is None:
                reason = "No reason provided."
            message = f"{user.user.username}#{user.user.discriminator} was kicked from the server.\nReason: {reason}"
            await user.kick(guild_id=ctx.guild_id, reason=reason)
            await ctx.send(message)


        elif sub_command == "ban":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have ban permission.", ephemeral=True)

            if int(user.user.id) == int(ctx.member.id):
                return await ctx.send("You cannot ban yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.BAN_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="I do not have ban permission.", ephemeral=True)

            if reason is None:
                reason = "No reason provided."
            message = f"{user.user.username}#{user.user.discriminator} was banned from the server.\nReason: {reason}"
            await user.ban(guild_id=ctx.guild_id, reason=reason)
            await ctx.send(message)


        elif sub_command == "hackban":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have ban permission.", ephemeral=True)

            if int(id) == int(ctx.member.id):
                return await ctx.send("You cannot ban yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.BAN_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="I do not have ban permission.", ephemeral=True)

            if reason is None:
                reason = "No reason provided."
            message = f"User with ID ``{id}`` was banned from the server.\nReason: {reason}"
            await self.bot._http.create_guild_ban(guild_id=ctx.guild_id, user_id=id, reason=reason)
            await ctx.send(message)


        elif sub_command == "unban":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have ban permission.", ephemeral=True)

            if int(id) == int(ctx.member.id):
                return await ctx.send("You cannot unban yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.BAN_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="I do not have ban permission.", ephemeral=True)

            message = f"User with ID ``{id}`` was unbanned from the server."
            await self.bot._http.remove_guild_ban(guild_id=ctx.guild_id, user_id=id)
            await ctx.send(message)


        elif sub_command == "timeout":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.MODERATE_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have timeout permission.", ephemeral=True)

            if int(user.user.id) == int(ctx.member.id):
                return await ctx.send("You cannot timeout yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.MODERATE_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have timeout permission.", ephemeral=True)

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


        elif sub_command == "untimeout":
            if not (
                has_permission(int(ctx.member.permissions), Permissions.MODERATE_MEMBERS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have timeout permission.", ephemeral=True)

            if int(user.user.id) == int(ctx.member.id):
                return await ctx.send("You cannot untimeout yourself.", ephemeral=True)

            bot = await guild.get_member(member_id=self.bot.me.id)
            role = bot.roles[0]
            role = await guild.get_role(role_id=role)
            perms = role.permissions
            if not (
                has_permission(int(perms), Permissions.MODERATE_MEMBERS) or
                has_permission(int(perms), Permissions.ADMINISTRATOR)
            ):
                return await ctx.send(content="You do not have timeout permission.", ephemeral=True)

            member = await guild.get_member(member_id=user.user.id)
            if member.communication_disabled_until is None:
                return await ctx.send(content="That user was not timed out.", ephemeral=True)

            message = f"{user.user.username}#{user.user.discriminator} was untimeout from the server."
            await member.modify(guild_id=ctx.guild_id, communication_disabled_until=None)
            await ctx.send(message)


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
    async def _channel(self, ctx: interactions.CommandContext, sub_command: str):
        if sub_command == "lock":
            channel = await ctx.get_channel()
            if not (
                has_permission(int(ctx.member.permissions), Permissions.MANAGE_CHANNELS) or
                has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
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
                #permission_overwrites.extend(channel.permissions)
                #await channel.modify(permission_overwrites=permission_overwrites)
                #await ctx.send(f"``{channel.name}`` is locked.")
                await ctx.send(f"{permission_overwrites}")
                await ctx.send(f"{channel.permissions}")
    """


    @interactions.extension_command(
        name="purge",
        description="(Admin only) Purge messages (default to 5 and max out of 20)",
        options=[
            interactions.Option(
                type=interactions.OptionType.INTEGER,
                name="amount",
                description="Amount of messages to purge",
                required=True
            )
        ],
        dm_permission=False
    )
    async def _purge(self, ctx: interactions.CommandContext, amount: int):
        if not (
            has_permission(int(ctx.member.permissions), Permissions.MANAGE_MESSAGES) or
            has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(content="You do not have manage messages permission.", ephemeral=True)

        if not amount:
            amount = int(5)
        if amount > 21:
            return await ctx.send(content="You cannot purge more than 20 messages.", ephemeral=True)

        await ctx.get_channel()
        await ctx.channel.purge(amount=amount, bulk=True)
        await ctx.send(f"Purged {amount} messages.", ephemeral=True)


def setup(bot):
    Admin(bot)
