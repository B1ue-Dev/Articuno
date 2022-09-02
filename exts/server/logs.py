"""
This module is for message logs.

(C) 2022 - Jimmy-Blue
"""

import asyncio
import logging
import datetime
import interactions
from utils import cache


class Logs(interactions.Extension):
    """Extension for logs."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_message_delete")
    async def on_message_delete(self, message: interactions.Message):
        """on_message_delete gateway event."""

        if not message:
            return

        author = interactions.EmbedAuthor(
            name=f"{message.author.username}#{message.author.discriminator}",
            icon_url=message.author.avatar_url,
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
                value=f"<#{message.channel_id}>",
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
        if message.content:
            embed.add_field(
                name="Deleted message content",
                value=f"{message.content}",
                inline=False,
            )
        if message.attachments:
            embed.add_field(
                name="Attachment",
                value="\n".join(attachment.url for attachment in message.attachments),
                inline=False,
            )

        if (
            str(message.guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(message.guild_id)] is not None
        ):
            try:
                _channel = interactions.Channel(
                    **await self.client._http.get_channel(
                        cache.Storage()._logs[str(message.guild_id)]
                    ),
                    _client=self.client._http,
                )

                if _channel.name == "logs":
                    await _channel.send(embeds=embed)
                else:
                    guild = interactions.Guild(
                        **await self.client._http.get_guild(str(message.guild_id)),
                        _client=self.client._http,
                    )
                    channels = await guild.get_all_channels()
                    _var = 0

                    for channel in channels:
                        if str(channel.name) == "logs":
                            _var = 1
                            await channel.send(embeds=embed)
                            break
                        else:
                            continue

                    if _var == 0:
                        cache.Storage()._logs[str(guild.id)] = None
                    elif _var == 1:
                        cache.Storage().add_logs(str(guild.id), str(channel.id))

            except AttributeError:
                cache.Storage()._logs[str(guild.id)] = None

        elif (
            str(message.guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(message.guild_id)] is None
        ):
            pass

        else:
            guild = interactions.Guild(
                **await self.client._http.get_guild(str(message.guild_id)),
                _client=self.client._http,
            )
            channels = await guild.get_all_channels()
            _var = 0

            for channel in channels:
                if str(channel.name) == "logs":
                    _var = 1
                    await channel.send(embeds=embed)
                    break
                else:
                    continue

            if _var == 0:
                cache.Storage()._logs[str(guild.id)] = None
            elif _var == 1:
                cache.Storage().add_logs(str(guild.id), str(channel.id))

    @interactions.extension_listener()
    async def on_message_update(
        self, before: interactions.Message, after: interactions.Message
    ):
        """on_message_update gateway event."""

        author = interactions.EmbedAuthor(
            name=f"{after.author.username}#{after.author.discriminator}",
            icon_url=after.author.avatar_url,
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
                value=f"<#{after.channel_id}>",
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
            name="Message before edit", value=before.content if before else "N/A"
        )
        embed.add_field(name="Message after edit", value=after.content)

        if (
            str(after.guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(after.guild_id)] is not None
        ):
            try:
                _channel = interactions.Channel(
                    **await self.client._http.get_channel(
                        cache.Storage()._logs[str(after.guild_id)]
                    ),
                    _client=self.client._http,
                )

                if _channel.name == "logs":
                    await _channel.send(embeds=embed)
                else:
                    guild = interactions.Guild(
                        **await self.client._http.get_guild(str(after.guild_id)),
                        _client=self.client._http,
                    )
                    channels = await guild.get_all_channels()
                    _var = 0

                    for channel in channels:
                        if str(channel.name) == "logs":
                            _var = 1
                            await channel.send(embeds=embed)
                            break
                        else:
                            continue

                    if _var == 0:
                        cache.Storage()._logs[str(guild.id)] = None
                    elif _var == 1:
                        cache.Storage().add_logs(str(guild.id), str(channel.id))

            except AttributeError:
                cache.Storage()._logs[str(guild.id)] = None

        elif (
            str(after.guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(after.guild_id)] is None
        ):
            pass

        else:
            guild = interactions.Guild(
                **await self.client._http.get_guild(str(after.guild_id)),
                _client=self.client._http,
            )
            channels = await guild.get_all_channels()
            _var = 0

            for channel in channels:
                if str(channel.name) == "logs":
                    _var = 1
                    await channel.send(embeds=embed)
                    break
                else:
                    continue

            if _var == 0:
                cache.Storage()._logs[str(guild.id)] = None
            elif _var == 1:
                cache.Storage().add_logs(str(guild.id), str(channel.id))

    # @interactions.extension_listener(name="on_guild_member_add")
    # async def on_guild_member_add(self, member: interactions.GuildMember):
    #     cache.Storage().add_user(str(member.guild_id), str(member.user.id))
    #     guild = interactions.Guild(
    #         **await self.client._http.get_guild(int(member.guild_id)),
    #         _client=self.client._http,
    #     )
    #     cache.Storage()._special_guilds[guild].append(member.user)
    #     embed = interactions.Embed(
    #         title="Welcome! 🥳",
    #         description=f"Welcome to {guild.name}, **{member.user.username}#{member.user.discriminator}**! We hope you have a good time here.",
    #         color=random.randint(0, 0xFFFFFF),
    #         timestamp=member.joined_at,
    #         footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
    #         thumbnail=interactions.EmbedImageStruct(
    #             url=member.user.avatar_url
    #         ),
    #     )

    #     if int(member.guild_id) == 859030372783751168:
    #         channel = interactions.Channel(
    #             **await self.client._http.get_channel(859077501589913610),
    #             _client=self.client._http,
    #         )
    #         await channel.send(embeds=embed)
    #         await guild.add_member_role(
    #             role=859034544270344192, member_id=int(member.user.id)
    #         )

    #     elif (
    #         str(member.guild_id) in cache.Storage()._welcome_goodbye
    #         and cache.Storage()._welcome_goodbye[str(member.guild_id)]
    #         is not None
    #     ):
    #         try:
    #             channel = interactions.Channel(
    #                 **await self.client._http.get_channel(
    #                     cache.Storage()._welcome_goodbye[
    #                         str(member.guild_id)
    #                     ]
    #                 ),
    #                 _client=self.client._http,
    #             )
    #             if channel.name == "welcome-goodbye":
    #                 await channel.send(embeds=embed)
    #             else:
    #                 guild = interactions.Guild(
    #                     **await self.client._http.get_guild(
    #                         str(member.guild_id)
    #                     ),
    #                     _client=self.client._http,
    #                 )
    #                 channels = await guild.get_all_channels()
    #                 _var = 0

    #                 for channel in channels:
    #                     if str(channel.name) == "welcome-goodbye":
    #                         _var = 1
    #                         await channel.send(embeds=embed)
    #                         break
    #                     else:
    #                         continue

    #                 if _var == 0:
    #                     cache.Storage()._welcome_goodbye[
    #                         str(guild.id)
    #                     ] = None
    #                 elif _var == 1:
    #                     cache.Storage().add_welcome_goodbye(
    #                         str(guild.id), str(channel.id)
    #                     )

    #         except AttributeError:
    #             cache.Storage()._welcome_goodbye[
    #                 str(member.guild_id)
    #             ] = None

    #     elif (
    #         str(member.guild_id) in cache.Storage()._welcome_goodbye
    #         and cache.Storage()._welcome_goodbye[str(member.guild_id)]
    #         is None
    #     ):
    #         pass

    #     else:
    #         guild = interactions.Guild(
    #             **await self.client._http.get_guild(str(member.guild_id)),
    #             _client=self.client._http,
    #         )
    #         channels = await guild.get_all_channels()
    #         _var = 0

    #         for channel in channels:
    #             if str(channel.name) == "welcome-goodbye":
    #                 _var = 1
    #                 await channel.send(embeds=embed)
    #                 break
    #             else:
    #                 continue

    #         if _var == 0:
    #             cache.Storage()._welcome_goodbye[str(guild.id)] = None
    #         elif _var == 1:
    #             cache.Storage().add_welcome_goodbye(
    #                 str(guild.id), str(channel.id)
    #             )

    # @interactions.extension_listener(name="on_guild_member_remove")
    # async def on_guild_member_remove(
    #     self, member: interactions.GuildMember
    # ):
    #     cache.Storage().remove_user(
    #         str(member.guild_id), str(member.user.id)
    #     )
    #     guild = interactions.Guild(
    #         **await self.client._http.get_guild(int(member.guild_id)),
    #         _client=self.client._http,
    #     )
    #     cache.Storage()._special_guilds[guild].remove(member.user)
    #     embed = interactions.Embed(
    #         title="Goodbye! 😢",
    #         description=f"Goodbye **{member.user.username}#{member.user.discriminator}**! Thanks for joining {guild.name}.",
    #         color=random.randint(0, 0xFFFFFF),
    #         timestamp=datetime.datetime.utcnow(),
    #         footer=interactions.EmbedFooter(text=f"ID: {member.user.id}"),
    #         thumbnail=interactions.EmbedImageStruct(
    #             url=member.user.avatar_url
    #         ),
    #     )

    #     if int(member.guild_id) == 859030372783751168:
    #         channel = interactions.Channel(
    #             **await self.client._http.get_channel(859077501589913610),
    #             _client=self.client._http,
    #         )
    #         await channel.send(embeds=embed)

    #     elif (
    #         str(member.guild_id) in cache.Storage()._welcome_goodbye
    #         and cache.Storage()._welcome_goodbye[str(member.guild_id)]
    #         is not None
    #     ):
    #         try:
    #             channel = interactions.Channel(
    #                 **await self.client._http.get_channel(
    #                     cache.Storage()._welcome_goodbye[
    #                         str(member.guild_id)
    #                     ]
    #                 ),
    #                 _client=self.client._http,
    #             )
    #             if channel.name == "welcome-goodbye":
    #                 await channel.send(embeds=embed)
    #             else:
    #                 guild = interactions.Guild(
    #                     **await self.client._http.get_guild(
    #                         str(member.guild_id)
    #                     ),
    #                     _client=self.client._http,
    #                 )
    #                 channels = await guild.get_all_channels()
    #                 _var = 0

    #                 for channel in channels:
    #                     if str(channel.name) == "welcome-goodbye":
    #                         _var = 1
    #                         await channel.send(embeds=embed)
    #                         break
    #                     else:
    #                         continue

    #                 if _var == 0:
    #                     cache.Storage()._welcome_goodbye[
    #                         str(guild.id)
    #                     ] = None
    #                 elif _var == 1:
    #                     cache.Storage().add_welcome_goodbye(
    #                         str(guild.id), str(channel.id)
    #                     )

    #         except AttributeError:
    #             cache.Storage()._welcome_goodbye[
    #                 str(member.guild_id)
    #             ] = None

    #     elif (
    #         str(member.guild_id) in cache.Storage()._welcome_goodbye
    #         and cache.Storage()._welcome_goodbye[str(member.guild_id)]
    #         is None
    #     ):
    #         pass

    #     else:
    #         guild = interactions.Guild(
    #             **await self.client._http.get_guild(str(member.guild_id)),
    #             _client=self.client._http,
    #         )
    #         channels = await guild.get_all_channels()
    #         _var = 0

    #         for channel in channels:
    #             if str(channel.name) == "welcome-goodbye":
    #                 _var = 1
    #                 await channel.send(embeds=embed)
    #                 break
    #             else:
    #                 continue

    #         if _var == 0:
    #             cache.Storage()._welcome_goodbye[str(guild.id)] = None
    #         elif _var == 1:
    #             cache.Storage().add_welcome_goodbye(
    #                 str(guild.id), str(channel.id)
    #             )

    @interactions.extension_listener(name="on_guild_ban_add")
    async def on_guild_ban_add(self, guild: interactions.GuildBan):
        guild_id = str(guild.guild_id)
        await asyncio.sleep(1)
        _ban = await self.client._http.get_guild_auditlog(
            guild_id=guild_id, action_type=22, limit=1
        )
        reason = _ban.get("audit_log_entries")[0].get("reason")
        moderator = _ban.get("audit_log_entries")[0].get("user_id")
        embed = interactions.Embed(
            title="User banned!",
            timestamp=datetime.datetime.utcnow(),
            color=0xE03C3C,
            footer=interactions.EmbedFooter(text=f"ID: {guild.user.id}"),
            author=interactions.EmbedAuthor(
                name=f"{guild.user.username}#{guild.user.discriminator}",
                icon_url=guild.user.avatar_url,
            ),
            fields=[
                interactions.EmbedField(
                    name="User", value=guild.user.mention, inline=True
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

        if (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is not None
        ):
            try:
                _channel = interactions.Channel(
                    **await self.client._http.get_channel(
                        cache.Storage()._logs[str(guild_id)]
                    ),
                    _client=self.client._http,
                )

                if _channel.name == "logs":
                    await _channel.send(embeds=embed)
                else:
                    _guild = interactions.Guild(
                        **await self.client._http.get_guild(str(guild_id)),
                        _client=self.client._http,
                    )
                    channels = await _guild.get_all_channels()
                    _var = 0

                    for channel in channels:
                        if str(channel.name) == "logs":
                            _var = 1
                            await channel.send(embeds=embed)
                            break
                        else:
                            continue

                    if _var == 0:
                        cache.Storage()._logs[str(_guild.id)] = None
                    elif _var == 1:
                        cache.Storage().add_logs(str(_guild.id), str(channel.id))

            except AttributeError:
                cache.Storage()._logs[str(_guild.id)] = None

        elif (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is None
        ):
            pass

        else:
            _guild = interactions.Guild(
                **await self.client._http.get_guild(str(guild_id)),
                _client=self.client._http,
            )
            channels = await _guild.get_all_channels()
            _var = 0

            for channel in channels:
                if str(channel.name) == "logs":
                    _var = 1
                    await channel.send(embeds=embed)
                    break
                else:
                    continue

            if _var == 0:
                cache.Storage()._logs[str(_guild.id)] = None
            elif _var == 1:
                cache.Storage().add_logs(str(_guild.id), str(channel.id))

    @interactions.extension_listener(name="on_guild_ban_remove")
    async def on_guild_ban_remove(self, guild: interactions.GuildBan):
        guild_id = str(guild.guild_id)
        await asyncio.sleep(1)
        _ban = await self.client._http.get_guild_auditlog(
            guild_id=guild_id, action_type=23, limit=1
        )
        reason = _ban.get("audit_log_entries")[0].get("reason")
        moderator = _ban.get("audit_log_entries")[0].get("user_id")
        embed = interactions.Embed(
            title="User unbanned!",
            timestamp=datetime.datetime.utcnow(),
            color=0xE03C3C,
            footer=interactions.EmbedFooter(text=f"ID: {guild.user.id}"),
            author=interactions.EmbedAuthor(
                name=f"{guild.user.username}#{guild.user.discriminator}",
                icon_url=guild.user.avatar_url,
            ),
            fields=[
                interactions.EmbedField(
                    name="User", value=guild.user.mention, inline=True
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

        if (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is not None
        ):
            try:
                _channel = interactions.Channel(
                    **await self.client._http.get_channel(
                        cache.Storage()._logs[str(guild_id)]
                    ),
                    _client=self.client._http,
                )

                if _channel.name == "logs":
                    await _channel.send(embeds=embed)
                else:
                    _guild = interactions.Guild(
                        **await self.client._http.get_guild(str(guild_id)),
                        _client=self.client._http,
                    )
                    channels = await _guild.get_all_channels()
                    _var = 0

                    for channel in channels:
                        if str(channel.name) == "logs":
                            _var = 1
                            await channel.send(embeds=embed)
                            break
                        else:
                            continue

                    if _var == 0:
                        cache.Storage()._logs[str(_guild.id)] = None
                    elif _var == 1:
                        cache.Storage().add_logs(str(_guild.id), str(channel.id))

            except AttributeError:
                cache.Storage()._logs[str(_guild.id)] = None

        elif (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is None
        ):
            pass

        else:
            _guild = interactions.Guild(
                **await self.client._http.get_guild(str(guild_id)),
                _client=self.client._http,
            )
            channels = await _guild.get_all_channels()
            _var = 0

            for channel in channels:
                if str(channel.name) == "logs":
                    _var = 1
                    await channel.send(embeds=embed)
                    break
                else:
                    continue

            if _var == 0:
                cache.Storage()._logs[str(_guild.id)] = None
            elif _var == 1:
                cache.Storage().add_logs(str(_guild.id), str(channel.id))

    @interactions.extension_listener(name="on_guild_member_update")
    async def on_guild_member_update(
        self, before: interactions.GuildMember, after: interactions.GuildMember
    ):
        guild_id = str(after.guild_id)
        embed: interactions.Embed = None
        if after.communication_disabled_until is not None:
            await asyncio.sleep(1)
            _timeout = await self.client._http.get_guild_auditlog(
                guild_id=guild_id, action_type=24, limit=1
            )
            reason = _timeout.get("audit_log_entries")[0].get("reason")
            moderator = _timeout.get("audit_log_entries")[0].get("user_id")
            embed = interactions.Embed(
                title="User timed out!",
                timestamp=datetime.datetime.utcnow(),
                color=0xFDFF7A,
                footer=interactions.EmbedFooter(text=f"ID: {after.user.id}"),
                author=interactions.EmbedAuthor(
                    name=f"{after.user.username}#{after.user.discriminator}",
                    icon_url=after.user.avatar_url,
                ),
                fields=[
                    interactions.EmbedField(
                        name="User", value=after.user.mention, inline=True
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
                    interactions.EmbedField(
                        name="Duration",
                        value=f"<t:{round(after.communication_disabled_until.timestamp())}:R>",
                        inline=False,
                    ),
                ],
            )
        elif after.communication_disabled_until is None:
            await asyncio.sleep(1)
            _timeout = await self.client._http.get_guild_auditlog(
                guild_id=guild_id, action_type=24, limit=1
            )
            reason = _timeout.get("audit_log_entries")[0].get("reason")
            moderator = _timeout.get("audit_log_entries")[0].get("user_id")
            embed = interactions.Embed(
                title="User time-out removed!",
                timestamp=datetime.datetime.utcnow(),
                color=0xFDFF7A,
                footer=interactions.EmbedFooter(text=f"ID: {after.user.id}"),
                author=interactions.EmbedAuthor(
                    name=f"{after.user.username}#{after.user.discriminator}",
                    icon_url=after.user.avatar_url,
                ),
                fields=[
                    interactions.EmbedField(
                        name="User", value=after.user.mention, inline=True
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

        if (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is not None
        ):
            try:
                _channel = interactions.Channel(
                    **await self.client._http.get_channel(
                        cache.Storage()._logs[str(guild_id)]
                    ),
                    _client=self.client._http,
                )

                if _channel.name == "logs":
                    await _channel.send(embeds=embed)
                else:
                    _guild = interactions.Guild(
                        **await self.client._http.get_guild(str(guild_id)),
                        _client=self.client._http,
                    )
                    channels = await _guild.get_all_channels()
                    _var = 0

                    for channel in channels:
                        if str(channel.name) == "logs":
                            _var = 1
                            await channel.send(embeds=embed)
                            break
                        else:
                            continue

                    if _var == 0:
                        cache.Storage()._logs[str(_guild.id)] = None
                    elif _var == 1:
                        cache.Storage().add_logs(str(_guild.id), str(channel.id))

            except AttributeError:
                cache.Storage()._logs[str(_guild.id)] = None

        elif (
            str(guild_id) in cache.Storage()._logs
            and cache.Storage()._logs[str(guild_id)] is None
        ):
            pass

        else:
            _guild = interactions.Guild(
                **await self.client._http.get_guild(str(guild_id)),
                _client=self.client._http,
            )
            channels = await _guild.get_all_channels()
            _var = 0

            for channel in channels:
                if str(channel.name) == "logs":
                    _var = 1
                    await channel.send(embeds=embed)
                    break
                else:
                    continue

            if _var == 0:
                cache.Storage()._logs[str(_guild.id)] = None
            elif _var == 1:
                cache.Storage().add_logs(str(_guild.id), str(channel.id))


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Logs(client)
    logging.debug("""[%s] Loaded Logs extension.""", log_time)
