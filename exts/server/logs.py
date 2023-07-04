"""
Handle all logging aspects.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import datetime
import random
import interactions


class Logs(interactions.Extension):
    """Extension for logs."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen(interactions.events.MessageDelete)
    async def on_message_delete(
        self, msg: interactions.events.MessageDelete
    ) -> None:
        """MESSAGE_DELETE gateway event."""

        message = msg.message
        if not message:
            return

        author = interactions.EmbedAuthor(
            name=f"{message.author.username}#{message.author.discriminator}",
            icon_url=message.author.avatar.url
            if message.author.avatar
            else None,
        )
        footer = interactions.EmbedFooter(text=f"Message ID: {message.id}")
        fields = [
            interactions.EmbedField(
                name="Member",
                value=f"{message.author.mention}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Channel",
                value=f"<#{message.channel.id}>",
                inline=True,
            ),
        ]
        embed = interactions.Embed(
            title="Deleted message content",
            description=message.content[-4096:]
            if message.content
            else "No content found. (Maybe it is not cached)",
            color=0xE03C3C,
            author=author,
            footer=footer,
            timestamp=datetime.datetime.utcnow(),
            fields=fields,
        )
        if message.attachments:
            embed.add_field(
                name="Attachment",
                value="\n".join(
                    attachment.url for attachment in message.attachments
                ),
                inline=False,
            )

        for channel in msg.message.guild.channels:
            if channel.name == "logs" and int(channel.type) == 0:
                try:
                    await channel.send(embeds=embed)
                    break
                except interactions.errors.HTTPException:
                    break

    @interactions.listen(interactions.events.MessageUpdate)
    async def on_message_update(
        self, msg: interactions.events.MessageUpdate
    ) -> None:
        """MESSAGE_UPDATE gateway event."""

        before: interactions.Message = msg.before
        after: interactions.Message = msg.after

        if before and after and before.content == after.content:
            return

        author = interactions.EmbedAuthor(
            name=f"{after.author.username}#{after.author.discriminator}",
            icon_url=after.author.avatar.url if after.author.avatar else None,
        )
        footer = interactions.EmbedFooter(text=f"Message ID: {after.id}")
        fields = [
            interactions.EmbedField(
                name="Member",
                value=f"{after.author.mention}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Channel",
                value=f"<#{after.channel.id}>",
                inline=True,
            ),
        ]
        embed = interactions.Embed(
            color=0xE03C3C,
            author=author,
            footer=footer,
            timestamp=datetime.datetime.utcnow(),
            fields=fields,
        )
        embed.add_field(
            name="Message before edit",
            value=before.content[-1024:] if before else "N/A",
        )
        embed.add_field(
            name="Message after edit",
            value=after.content[-1024:] if after.content != [] else "N/A",
        )

        for channel in after.guild.channels:
            if channel.name == "logs" and int(channel.type) == 0:
                try:
                    await channel.send(embeds=embed)
                    break
                except interactions.errors.HTTPException:
                    break

    @interactions.listen(interactions.events.MemberAdd)
    async def on_guild_member_add(
        self, _member: interactions.events.MemberAdd
    ) -> None:
        """GUILD_MEMBER_ADD gateway event."""

        member = _member.member
        welcome_message: list[str] = [
            "We hope you have a good time here.",
            "We glad to have you here.",
            "It is good to see you here.",
        ]
        embed = interactions.Embed(
            title="Welcome! 🥳",
            description="".join(
                [
                    f"Welcome to {member.guild.name}, ",
                    f"**{member.user.username}#{member.user.discriminator}**",
                    f"! {random.choice(welcome_message)}",
                ],
            ),
            color=random.randint(0, 0xFFFFFF),
            timestamp=member.joined_at,
            footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
            thumbnail=interactions.EmbedAttachment(
                url=member.user.avatar.url if member.user.avatar else None,
            ),
        )

        if int(member.guild.id) == 859030372783751168:
            channel = self.client.get_channel(859077501589913610)
            await channel.send(embeds=embed)
            await member.add_role(role=859034544270344192)
        else:
            for channel in member.guild.channels:
                if (
                    channel.name == "welcome-goodbye"
                    and int(channel.type) == 0
                ):
                    await channel.send(embeds=embed)

    @interactions.listen(interactions.events.MemberRemove)
    async def on_guild_member_remove(
        self, _member: interactions.events.MemberRemove
    ) -> None:
        """GUILD_REMOVE gateway event."""

        if _member.member.guild:
            member = _member.member
            embed = interactions.Embed(
                title="Goodbye! 😢",
                description="".join(
                    [
                        f"Goodbye **{member.username}#{member.discriminator}**!",
                        f" Thanks for joining {member.guild.name}.",
                    ],
                ),
                color=random.randint(0, 0xFFFFFF),
                timestamp=datetime.datetime.utcnow(),
                footer=interactions.EmbedFooter(text=f"ID: {member.id}"),
                thumbnail=interactions.EmbedAttachment(
                    url=member.user.avatar.url if member.user.avatar else None
                ),
            )

            for channel in member.guild.channels:
                if (
                    channel.name == "welcome-goodbye"
                    and int(channel.type) == 0
                ):
                    await channel.send(embeds=embed)

    @interactions.listen(interactions.events.BanCreate)
    async def on_guild_ban_add(
        self, ban: interactions.events.BanCreate
    ) -> None:
        """GUILD_BAN_CREATE gateway event."""

        user: interactions.BaseUser = ban.user
        reason: str = None
        moderator: str = None
        try:
            _ban = (
                await ban.guild.fetch_audit_log(
                    action_type=interactions.AuditLogEventType.MEMBER_BAN_ADD,
                    limit=1,
                )
            ).to_dict()
            reason: str = _ban.get("entries")[0].get("reason")
            moderator: int = _ban.get("entries")[0].get("user_id")
        except interactions.errors.HTTPException:
            pass

        embed = interactions.Embed(
            title="User banned!",
            timestamp=datetime.datetime.utcnow(),
            color=0xE03C3C,
            footer=interactions.EmbedFooter(text=f"ID: {user.id}"),
            author=interactions.EmbedAuthor(
                name=f"{user.username}#{user.discriminator}",
                icon_url=user.avatar.url if user.avatar else None,
            ),
            fields=[
                interactions.EmbedField(
                    name="User", value=user.mention, inline=True
                ),
                interactions.EmbedField(
                    name="Moderator",
                    value="".join(f"<@{moderator}>" if moderator else "N/A"),
                    inline=True,
                ),
                interactions.EmbedField(
                    name="Reason",
                    value=reason if reason else "N/A",
                    inline=False,
                ),
            ],
        )

        for channel in ban.guild.channels:
            if channel.name == "logs" and int(channel.type) == 0:
                await channel.send(embeds=embed)
                break

    @interactions.listen(interactions.events.BanRemove)
    async def on_guild_ban_remove(
        self, ban: interactions.events.BanRemove
    ) -> None:
        """GUILD_BAN_REMOVE gateway event."""

        user: interactions.BaseUser = ban.user
        reason: str = None
        moderator: str = None
        try:
            _ban = (
                await ban.guild.fetch_audit_log(
                    action_type=interactions.AuditLogEventType.MEMBER_BAN_ADD,
                    limit=1,
                )
            ).to_dict()
            reason: str = _ban.get("entries")[0].get("reason")
            moderator: int = _ban.get("entries")[0].get("user_id")
        except interactions.errors.HTTPException:
            pass

        embed = interactions.Embed(
            title="User unbanned!",
            timestamp=datetime.datetime.utcnow(),
            color=0xE03C3C,
            footer=interactions.EmbedFooter(text=f"ID: {user.id}"),
            author=interactions.EmbedAuthor(
                name=f"{user.username}#{user.discriminator}",
                icon_url=user.avatar.url if user.avatar else None,
            ),
            fields=[
                interactions.EmbedField(
                    name="User", value=user.mention, inline=True
                ),
                interactions.EmbedField(
                    name="Moderator",
                    value="".join(f"<@{moderator}>" if moderator else "N/A"),
                    inline=True,
                ),
                interactions.EmbedField(
                    name="Reason",
                    value=reason if reason else "N/A",
                    inline=False,
                ),
            ],
        )

        for channel in ban.guild.channels:
            if channel.name == "logs" and int(channel.type) == 0:
                await channel.send(embeds=embed)
                break


def setup(client) -> None:
    """Setup the extension."""
    Logs(client)
    logging.info("Loaded Logs extension.")
