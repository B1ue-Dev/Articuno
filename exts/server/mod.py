"""
Moderation commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import datetime
import interactions
from utils.permission import has_permission, Permissions


class Mod(interactions.Extension):
    """Extension for /mod commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="mod",
        description="Handles all moderation aspects.",
        dm_permission=False,
    )
    async def mod(self, ctx: interactions.SlashContext) -> None:
        """Handles all moderation aspects."""
        ...

    user = mod.group(
        name="user",
        description="All user moderation aspects.",
    )

    @user.subcommand()
    @interactions.slash_option(
        name="member",
        description="The user you wish to kick",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the kick",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def kick(
        self,
        ctx: interactions.SlashContext,
        member: interactions.Member,
        reason: str = "N/A",
    ) -> None:
        """Kicks a member from the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.KICK_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have kick permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot kick yourself.", ephemeral=True)

        try:
            await member.kick(reason=reason)
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator}",
                        " was not kicked.\nPlease check whenever I am higher",
                        " than the user's role or I have enough ",
                        "permissions to kick the user.",
                    ],
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{member.user.username}#{member.user.discriminator}",
                    f" was kicked.\nReason: {reason}",
                ],
            ),
        )

    @user.subcommand()
    @interactions.slash_option(
        name="member",
        description="The user you wish to ban",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the ban",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    @interactions.slash_option(
        name="delete_message_days",
        description="The number of days to delete messages for (0-7)",
        opt_type=interactions.OptionType.INTEGER,
        choices=[
            interactions.SlashCommandChoice(
                name=f"{i} days",
                value=i,
            )
            for i in range(0, 8)
        ],
        required=False,
    )
    async def ban(
        self,
        ctx: interactions.SlashContext,
        member: interactions.Member,
        reason: str = "N/A",
        delete_message_days: int = 0,
    ) -> None:
        """Bans a member from the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.BAN_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot ban yourself.", ephemeral=True)

        try:
            await member.ban(
                reason=reason,
                delete_message_days=delete_message_days,
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator}",
                        " was not banned.\nPlease check whenever I am higher",
                        " than the user's role or I have enough ",
                        "permissions to ban the user.",
                    ],
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{member.user.username}#{member.user.discriminator}",
                    f" was banned.\nReason: {reason}",
                ],
            ),
        )

    @user.subcommand()
    @interactions.slash_option(
        name="id",
        description="The ID of user you wish to ban",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the ban",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def hackban(
        self, ctx: interactions.SlashContext, id: str, reason: str = "N/A"
    ):
        """Bans a member who is not in the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.BAN_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(id) == int(ctx.member.id):
            return await ctx.send("You cannot ban yourself.", ephemeral=True)

        try:
            user = await self.client.get_user(id)
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="Unknown user. Please check the ID again.",
                ephemeral=True,
            )

        try:
            await self.client.http.create_guild_ban(
                guild_id=int(ctx.guild_id), user_id=int(id), reason=reason
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{user.username}#{user.discriminator} ({user.id})",
                        " was not banned.\nPlease check whenever I am higher",
                        " than the user's role or I have enough ",
                        "permissions to ban the user.",
                    ],
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{user.username}#{user.discriminator} ({user.id})",
                    f" was banned.\nReason: {reason}",
                ],
            ),
        )

    @user.subcommand()
    @interactions.slash_option(
        name="id",
        description="The ID of user you wish to unban",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the unban",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def unban(
        self, ctx: interactions.SlashContext, id: str, reason: str = "N/A"
    ):
        """Unbans a member from the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.BAN_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have ban permission.", ephemeral=True
            )

        if int(id) == int(ctx.member.id):
            return await ctx.send("You cannot unban yourself.", ephemeral=True)

        user: interactions.User = None
        try:
            user = await self.client.get_user(id)
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="Unknown user. Please check the ID again.",
                ephemeral=True,
            )

        try:
            await self.client.http.remove_guild_ban(
                guild_id=int(ctx.guild_id), user_id=int(id), reason=reason
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{id} was not unbanned.\nPlease check whenever",
                        " I am higher than the user's role or I have",
                        "enough permissions to ban the user.",
                    ],
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{user.username}#{user.discriminator}",
                    f" ({user.id}) was unbanned.",
                ],
            ),
        )

    @user.subcommand()
    @interactions.slash_option(
        name="member",
        description="The user you wish to timeout",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the timeout",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    @interactions.slash_option(
        name="days",
        description="How long the user should be timeouted in days",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    @interactions.slash_option(
        name="hours",
        description="How long the user should be timeouted in hours",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    @interactions.slash_option(
        name="minutes",
        description="How long the user should be timeouted in minutes",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    @interactions.slash_option(
        name="seconds",
        description="How long the user should be timeouted in seconds",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    async def timeout(
        self,
        ctx: interactions.SlashContext,
        member: interactions.Member,
        reason: str = "N/A",
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ):
        """Timeouts a member from the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.MODERATE_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have moderate members permission.",
                ephemeral=True,
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send(
                "You cannot timeout yourself.", ephemeral=True
            )

        if not days and not hours and not minutes and not seconds:
            return await ctx.send(
                content="Please indicate the length of the timeout.",
                ephemeral=True,
            )

        if days > 28:
            return await ctx.send(
                content="".join(
                    [
                        "The maximum is 27 days. Please try again. ",
                        "[Learn more](<https://support.discord.com/h",
                        "c/en-us/articles/4413305239191-Time-Out-FAQ>)",
                    ],
                ),
                ephemeral=True,
            )

        time = datetime.datetime.utcnow()
        time += datetime.timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        )

        try:
            await member.timeout(
                communication_disabled_until=time.isoformat(),
                reason=reason,
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator}",
                        " was not timed out.\nPlease check whenever I am ",
                        "higher than the user's role or I have enough ",
                        "permissions to timeout the user.",
                    ],
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{member.user.username}#{member.user.discriminator}",
                    f" was timed out.\nReason: {reason}",
                ],
            ),
        )

    @user.subcommand()
    @interactions.slash_option(
        name="member",
        description="The user you wish to untimeout",
        opt_type=interactions.OptionType.USER,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the untimeout",
        opt_type=interactions.OptionType.STRING,
    )
    async def untimeout(
        self,
        ctx: interactions.SlashContext,
        member: interactions.Member,
        reason: str = "N/A",
    ):
        """Untimeouts a member from the server."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.MODERATE_MEMBERS
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have timeout permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send(
                "You cannot untimeout yourself.", ephemeral=True
            )

        if member.communication_disabled_until is None:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator}",
                        " was not timed out.",
                    ]
                ),
                ephemeral=True,
            )

        try:
            await member.timeout(
                communication_disabled_until=None,
                reason=reason,
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        f"{member.user.username}#{member.user.discriminator}",
                        "time-out was not removed.\nPlease check whenever I ",
                        "am higher than the user's role or I have enough ",
                        "permissions to untimeout the user.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            content="".join(
                [
                    f"{member.user.username}#{member.user.discriminator}",
                    f" time-out was removed.\nReason: {reason}",
                ],
            )
        )

    channel = mod.group(
        name="channnel",
        description="All channel moderation aspects.",
    )

    @channel.subcommand()
    @interactions.slash_option(
        name="amount",
        description="The amount of message you want to purge",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    @interactions.slash_option(
        name="channel",
        description="The channel you wish to purge",
        opt_type=interactions.OptionType.CHANNEL,
        channel_types=[interactions.ChannelType.GUILD_TEXT],
        required=False,
    )
    @interactions.slash_option(
        name="reason",
        description="The reason behind the purge",
        opt_type=interactions.OptionType.STRING,
    )
    async def purge(
        self,
        ctx: interactions.SlashContext,
        amount: int = 5,
        channel: interactions.GuildText = None,
        reason: str = "N/A",
    ):
        """Purges an amount of messages from a channel."""

        if not (
            has_permission(
                int(ctx.member.guild_permissions), Permissions.MANAGE_MESSAGES
            )
            or has_permission(
                int(ctx.member.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have manage messages permission.",
                ephemeral=True,
            )

        if amount > 21:
            return await ctx.send(
                content="You cannot purge more than 20 messages.",
                ephemeral=True,
            )

        if not channel:
            channel = ctx.channel

        try:
            await channel.purge(deletion_limit=amount, reason=reason)
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="".join(
                    [
                        "Failed to purge message.\n Please check ",
                        "whenever I have `MANAGE_MESSAGES` permission",
                        " to purge the message.",
                    ]
                ),
                ephemeral=True,
            )

        await ctx.send(
            f"Purged {amount} messages in #{channel.name}.", ephemeral=True
        )


def setup(client) -> None:
    """Setup the extension."""
    Mod(client)
    logging.info("Loaded Mod extension.")
