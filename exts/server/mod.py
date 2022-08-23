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
        # default_member_permissions=interactions.Permissions.KICK_MEMBERS,
        dm_permission=False,
    )
    async def _mod(self, ctx: interactions.CommandContext, **kwargs):
        """Handles all moderation aspects."""
        ...


    @_mod.group(name="user")
    async def _user(self, *args, **kwargs):
        ...

    @_user.subcommand(name="kick")
    @interactions.option("The user you wish to kick")
    @interactions.option("The reason behind the kick")
    async def _user_kick(
        self,
        ctx: interactions.CommandContext,
        user: interactions.Member,
        reason: str = "N/A",
    ):
        """Kicks a member from the server."""

        if not (
            has_permission(int(ctx.member.permissions), Permissions.KICK_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have kick permission.", ephemeral=True
            )

        if int(user.user.id) == int(ctx.member.id):
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
            content=f"{user.user.username}#{user.user.discriminator} was kicked.\nReason: {reason}"
        )

    @_user.subcommand(name="ban")
    @interactions.option("The user you wish to kick")
    @interactions.option("The reason behind the ban")
    @interactions.option("The number of days to delete messages for (0-7)",
        choices=[
            interactions.Choice(name=f"{i} days", value=i)
            for i in range(0, 8)
        ],
        required=False,
    )
    async def _user_ban(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
        delete_message_days: int = 0,
    ):
        """Bans a member from the server."""

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

    @_user.subcommand(name="hackban")
    @interactions.option("The ID of the user you wish to ban")
    @interactions.option("The reason behind the ban")
    async def _user_hackban(
        self, ctx: interactions.CommandContext, id: str, reason: str = "N/A"
    ):
        """Banss a member who is not in the server."""
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

    @_user.subcommand(name="unban")
    @interactions.option("The user you wish to unban")
    @interactions.option("The reason behind the unban")
    async def _user_unban(
        self, ctx: interactions.CommandContext, id: str, reason: str = "N/A"
    ):
        """Unbans a member from the server."""

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

    @_user.subcommand(name="timeout")
    @interactions.option("The user you wish to timeout")
    @interactions.option("The reason behind the timeout")
    @interactions.option("How long the user should be timeouted in days")
    @interactions.option("How long the user should be timeouted in hours")
    @interactions.option("How long the user should be timeouted in minutes")
    @interactions.option("How long the user should be timeouted in seconds")
    async def _user_timeout(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ):
        """Timeouts a member from the server."""

        if not (
            has_permission(int(ctx.member.permissions), Permissions.MODERATE_MEMBERS)
            or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have moderate members permission.", ephemeral=True
            )

        if int(member.user.id) == int(ctx.member.id):
            return await ctx.send("You cannot timeout yourself.", ephemeral=True)

        if not days and not hours and not minutes and not seconds:
            return await ctx.send(
                content="Please indicate the length of the timeout.", ephemeral=True
            )

        time = datetime.datetime.utcnow()
        time += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

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

    @_user.subcommand(name="untimeout")
    @interactions.option("The user you wish to untimeout")
    @interactions.option("The reason behind the untimeout")
    async def _user_untimeout(
        self,
        ctx: interactions.CommandContext,
        member: interactions.Member,
        reason: str = "N/A",
    ):
        """Untimeouts a member from the server."""

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

    @_mod.group(name="channel")
    async def _channel(self, *args, **kwargs):
        ...

    @_channel.subcommand(name="purge")
    @interactions.option("The amount of message you want to purge")
    @interactions.option("The channel you wish to purge", channel_types=[interactions.ChannelType.GUILD_TEXT])
    @interactions.option("The reason behind the purge")
    async def _channel_purge(
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

    # TODO: Adding these once channel permissions can be get.
    # @_channel.subcommand(name="lock")
    # @interactions.option("The channel you wish to lock", channel_types=[interactions.ChannelType.GUILD_TEXT])
    # @interactions.option("The reason behind the lock")
    # async def _channel_lock(
    #     self,
    #     ctx: interactions.CommandContext,
    #     channel: interactions.Channel = None,
    #     reason: str = "N/A",
    # ):
    #     """Locks a channel in the server."""

    #     if not (
    #         has_permission(int(ctx.member.permissions), Permissions.MANAGE_CHANNELS)
    #         or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
    #     ):
    #         return await ctx.send(
    #             content="You do not have manage channels permission.", ephemeral=True
    #         )

    #     await ctx.defer()

    #     if not channel:
    #         channel = await ctx.get_channel()

    #     overwrites = channel.permission_overwrites

    #     for overwrite in overwrites:
    #         if int(overwrite.id) == int(ctx.guild_id):
    #             overwrite.deny |= interactions.Permissions.SEND_MESSAGES
    #             break
    #     else:
    #         overwrites.append(
    #             interactions.Overwrite(
    #                 id=str(ctx.guild_id),
    #                 deny=interactions.Permissions.SEND_MESSAGES,
    #                 type=0,
    #             )
    #         )
    #         print(channel.permissions)

    #     await channel.modify(reason=reason, permission_overwrites=overwrites)
    #     await ctx.send(content=f"{channel.mention} was locked.")

    # @_channel.subcommand(name="unlock")
    # @interactions.option("The channel you wish to unlock", channel_types=[interactions.ChannelType.GUILD_TEXT])
    # @interactions.option("The reason behind the unlock")
    # async def _channel_unlock(
    #     self,
    #     ctx: interactions.CommandContext,
    #     channel: interactions.Channel = None,
    #     reason: str = "N/A",
    # ):
    #     """Unlocks a channel in the server."""

    #     if not (
    #         has_permission(int(ctx.member.permissions), Permissions.MANAGE_CHANNELS)
    #         or has_permission(int(ctx.member.permissions), Permissions.ADMINISTRATOR)
    #     ):
    #         return await ctx.send(
    #             content="You do not have manage channels permission.", ephemeral=True
    #         )

    #     await ctx.defer()

    #     if not channel:
    #         channel = await ctx.get_channel()

    #     overwrites = channel.permission_overwrites

    #     for overwrite in overwrites:
    #         if int(overwrite.id) == int(ctx.guild_id):
    #             overwrite.deny &= ~interactions.Permissions.SEND_MESSAGES
    #             overwrite.allow |= interactions.Permissions.SEND_MESSAGES
    #             break
    #     else:
    #         overwrites.append(
    #             interactions.Overwrite(
    #                 id=str(ctx.guild_id),
    #                 allow=interactions.Permissions.SEND_MESSAGES,
    #                 type=0,
    #             )
    #         )

    #     await channel.modify(reason=reason, permission_overwrites=overwrites)
    #     await ctx.send(content=f"{channel.mention} was unlocked.")


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Mod(client)
    logging.debug("""[%s] Loaded Mod extension.""", log_time)
    print(f"[{log_time}] Loaded Mod extension.")
