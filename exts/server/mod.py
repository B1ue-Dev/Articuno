"""
Moderation commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from utils.permission import Permissions, has_permission


class Mod(interactions.Extension):
    """Extension for /mod commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="mod",
        description="Moderation commands for moderating a member",
        default_member_permissions=interactions.Permissions.KICK_MEMBERS,
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="kick",
                description="Kicks a user from the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user you wish to kick",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the kick",
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="ban",
                description="Bans a user from the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user you wish to ban",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the ban",
                        required=False,
                    ),
                    interactions.Option(
                        name="delete_message_days",
                        type=interactions.OptionType.INTEGER,
                        description="The number of days to delete messages for (0-7)",
                        choices=[
                            interactions.Choice(name=f"{i} days", value=i)
                            for i in range(0, 8)
                        ],
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="hackban",
                description="Bans a user that is not in the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="id",
                        description="The ID of the user you wish to ban",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the ban",
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="unban",
                description="Unbans a user from the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="id",
                        description="The ID of the user you wish to unban",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the unban",
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="timeout",
                description="Timeouts a user from the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user you wish to timeout (Default to 1 hour)",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="days",
                        description="Days to timeout the user for (Default to 0)",
                        required=False,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="hours",
                        description="Hours to timeout the user for (Default to 1)",
                        required=False,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="minutes",
                        description="Minutes to timeout the user for (Default to 0)",
                        required=False,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="seconds",
                        description="Seconds to timeout the user for (Default to 0)",
                        required=False,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the timeout",
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="untimeout",
                description="Untimeouts a user from the server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user you wish to untimeout",
                        required=True,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the untimeout",
                        required=False,
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="purge",
                description="Purges a number of messages from a channel",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.INTEGER,
                        name="amount",
                        description="The number of messages to purge (Default to 5)",
                        required=False,
                    ),
                    interactions.Option(
                        type=interactions.OptionType.CHANNEL,
                        name="channel",
                        description="The channel to purge messages from (Default to the current channel)",
                        required=False,
                        channel_types=[interactions.ChannelType.GUILD_TEXT],
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason behind the purge",
                        required=False,
                    ),
                ],
            ),
        ],
        dm_permission=False,
    )
    async def _user(
        self,
        ctx: interactions.CommandContext,
        sub_command: str,
        user: interactions.Member = None,
        id: str = None,
        reason: str = "N/A",
        delete_message_days: int = 0,
        amount: int = 5,
        channel: interactions.Channel = None,
        **kwargs,
    ):
        match sub_command:
            case "kick":
                await self._kick_member(ctx, user, reason)
            case "ban":
                await self._ban_member(ctx, user, reason, delete_message_days)
            case "hackban":
                await self._hackban_member(ctx, id, reason)
            case "unban":
                await self._unban_member(ctx, id, reason)
            case "timeout":
                await self._timeout_member(ctx, user, reason, **kwargs)
            case "untimeout":
                await self._untimeout_member(ctx, user, reason)
            case "purge":
                await self._purge_channel(ctx, amount, channel, reason)

    async def _kick_member(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
    ):
        """Kick a member from the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.KICK_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have kick permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot kick yourself.", ephemeral=True)

        try:
            await member.kick(guild_id=int(ctx.guild_id), reason=reason)
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator} was not kicked.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to kick the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{member.user.username}#{member.user.discriminator} was kicked.\nReason: {reason}"
        )

    async def _ban_member(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
        delete_message_days: int = 0,
    ):
        """Ban a member from the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot ban yourself.", ephemeral=True)

        try:
            await member.ban(
                guild_id=int(ctx.guild_id),
                reason=reason,
                delete_message_days=delete_message_days,
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator} was not banned.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to ban the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{member.user.username}#{member.user.discriminator} was banned.\nReason: {reason}"
        )

    async def _hackban_member(
        self, ctx: interactions.CommandContext, id: str, reason: str = "N/A"
    ):
        """Ban a member who is not in the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(id) == int(ctx.member.id):
            return await ctx.send("You cannot ban yourself.", ephemeral=True)

        try:
            user = interactions.User(
                **await self.client._http.get_user(user_id=int(id)),
                _client=self.client._http,
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="Unknown User. Please check the ID again.", ephemeral=True
            )

        try:
            await self.client._http.create_guild_ban(
                guild_id=int(ctx.guild_id), user_id=int(id), reason=reason
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{user.username}#{user.discriminator} ({user.id}) was not banned.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to ban the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{user.username}#{user.discriminator} ({user.id}) was banned.\nReason: {reason}"
        )

    async def _unban_member(
        self, ctx: interactions.CommandContext, id: str, reason: str = "N/A"
    ):
        """Unban a member from the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.BAN_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(id) == int(ctx.member.id):
            return await ctx.send("You cannot unban yourself.", ephemeral=True)

        try:
            user = interactions.User(
                **await self.client._http.get_user(user_id=int(id)),
                _client=self.client._http,
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="Unknown User. Please check the ID again.", ephemeral=True
            )

        try:
            await self.client._http.remove_guild_ban(
                guild_id=int(ctx.guild_id), user_id=int(id), reason=reason
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{id} was not unbanned.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to ban the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{user.username}#{user.discriminator} ({user.id}) was unbanned."
        )

    async def _timeout_member(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
        hours: int = 1,
        **kwargs: dict,
    ):
        """Timeout a member from the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.MODERATE_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have timeout permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot timeout yourself.", ephemeral=True)

        time = datetime.datetime.utcnow()
        if kwargs:
            time += datetime.timedelta(**kwargs)
        else:
            time += datetime.timedelta(hours=hours)

        try:
            await member.modify(
                guild_id=int(ctx.guild_id),
                communication_disabled_until=time.isoformat(),
                reason=reason,
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator} was not timed out.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to timeout the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{member.user.username}#{member.user.discriminator} was timed out.\nReason: {reason}"
        )

    async def _untimeout_member(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
    ):
        """Untimeout a member from the server."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.MODERATE_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have timeout permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot untimeout yourself.", ephemeral=True)

        if member.communication_disabled_until is None:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator} was not timed out.",
                    ]
                ),
                ephemeral=True,
            )

        try:
            await member.modify(
                guild_id=int(ctx.guild_id),
                communication_disabled_until=None,
                reason=reason,
            )
        except interactions.LibraryException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator} time-out was not removed.\n",
                        "Please check whenever I am higher than the user's role or I have enough ",
                        "permissions to untimeout the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content=f"{member.user.username}#{member.user.discriminator} time-out was removed.\nReason: {reason}"
        )

    async def _purge_channel(
        self,
        ctx: interactions.CommandContext,
        amount: int = 5,
        channel: interactions.Channel = None,
        reason: str = "N/A",
    ):
        """Purges an amount of messages from a channel."""
        if not (
            has_permission(int(ctx.member.permissions), Permissions.MANAGE_MESSAGES)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have manage messages permission.", ephemeral=True
            )

        if amount > 21:
            return await ctx.send(
                content="You cannot purge more than 20 messages.", ephemeral=True
            )

        if not channel:
            channel = await ctx.get_channel()

        await channel.purge(amount=amount, bulk=True, reason=reason)
        await ctx.send(f"Purged {amount} messages in #{channel.name}.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Mod(client)
    logging.debug("""[%s] Loaded Mod extension.""", log_time)
    print(f"[{log_time}] Loaded Mod extension.")
