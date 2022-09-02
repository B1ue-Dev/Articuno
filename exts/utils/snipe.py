"""
This module is for snipe command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import asyncio
import interactions

_snipe_message_author = {}
_snipe_message_author_id = {}
_snipe_message_author_avatar_url = {}
_snipe_message_content = {}
_snipe_message_content_id = {}
_snipe_message_attachments = {}


class Snipe(interactions.Extension):
    """Extension for /snipe command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_message_delete")
    async def _message_delete(self, message: interactions.Message):
        _channel_id = int(message.channel_id)

        _snipe_message_author[_channel_id] = str(
            f"{message.author}#{message.author.discriminator}"
        )
        _snipe_message_author_id[_channel_id] = int(message.author.id)
        _snipe_message_author_avatar_url[_channel_id] = str(message.author.avatar_url)
        _snipe_message_content[_channel_id] = str(message.content)
        _snipe_message_content_id[_channel_id] = int(message.id)
        if message.attachments == []:
            _snipe_message_attachments[_channel_id] = None
        else:
            _snipe_message_attachments[_channel_id] = str(message.attachments[0].url)
        await asyncio.sleep(120)
        del _snipe_message_author[_channel_id]
        del _snipe_message_author_id[_channel_id]
        del _snipe_message_author_avatar_url[_channel_id]
        del _snipe_message_content[_channel_id]
        del _snipe_message_content_id[_channel_id]
        del _snipe_message_attachments[_channel_id]

    @interactions.extension_command(
        name="snipe",
        description="Snipe the last deleted message from the current channel.",
        dm_permission=False,
    )
    async def _snipe(self, ctx: interactions.CommandContext):
        """Snipe the last deleted message from the current channel."""

        channel_id = int(ctx.channel_id)
        try:
            author = interactions.EmbedAuthor(
                name=_snipe_message_author[channel_id],
                icon_url=_snipe_message_author_avatar_url[channel_id],
            )
            footer = interactions.EmbedFooter(
                name=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
                icon_url=ctx.author.user.avatar_url,
            )
            embed = interactions.Embed(
                description=f"<@{_snipe_message_author_id[channel_id]}> said: {_snipe_message_content[channel_id]}",
                author=author,
                footer=footer,
            )
            if str(_snipe_message_attachments[int(ctx.channel_id)]) is not None:
                embed.set_thumbnail(url=_snipe_message_attachments[int(ctx.channel_id)])
            await ctx.send(embeds=embed)

        except KeyError:
            await ctx.send("No message to snipe.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Snipe(client)
    logging.debug("""[%s] Loaded Snipe extension.""", log_time)
