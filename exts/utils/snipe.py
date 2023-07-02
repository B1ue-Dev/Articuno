"""
Snipe command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import interactions

_snipe_message_author = {}
_snipe_message_author_id = {}
_snipe_message_author_avatar_url = {}
_snipe_message_content = {}
_snipe_message_content_id = {}
# TODO: Actually store the message object
# and being able to store more messages.


class Snipe(interactions.Extension):
    """Extension for /snipe command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen(interactions.events.MessageDelete)
    async def on_message_delete(
        self, msg: interactions.events.MessageDelete
    ) -> None:
        """Listen to MESSAGE_DELETE and write to cache."""

        message: interactions.Message = msg.message
        _channel_id = int(message.channel.id)

        _snipe_message_author[_channel_id] = str(
            f"{message.author.username}#{message.author.discriminator}"
        )
        _snipe_message_author_id[_channel_id] = int(message.author.id)
        _snipe_message_author_avatar_url[_channel_id] = str(
            message.author.avatar.url
        )
        _snipe_message_content[_channel_id] = str(message.content)
        _snipe_message_content_id[_channel_id] = int(message.id)
        await asyncio.sleep(120)
        del _snipe_message_author[_channel_id]
        del _snipe_message_author_id[_channel_id]
        del _snipe_message_author_avatar_url[_channel_id]
        del _snipe_message_content[_channel_id]
        del _snipe_message_content_id[_channel_id]

    @interactions.slash_command(
        name="snipe",
        description="Snipes the last deleted message from the current channel.",
        dm_permission=False,
    )
    async def snipe(self, ctx: interactions.SlashContext) -> None:
        """Snipes the last deleted message from the current channel."""

        channel_id = int(ctx.channel_id)
        try:
            author = interactions.EmbedAuthor(
                name=_snipe_message_author[channel_id],
                icon_url=_snipe_message_author_avatar_url[channel_id],
            )
            footer = interactions.EmbedFooter(
                text="".join(
                    [
                        f"Requested by {ctx.author.user.username}",
                        f"#{ctx.author.user.discriminator}",
                    ],
                ),
                icon_url=ctx.author.user.avatar.url,
            )
            embed = interactions.Embed(
                description="".join(
                    [
                        f"<@{_snipe_message_author_id[channel_id]}> said: ",
                        f"{_snipe_message_content[channel_id]}",
                    ],
                ),
                author=author,
                footer=footer,
            )
            await ctx.send(embeds=embed)

        except KeyError:
            await ctx.send("No message to snipe.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    Snipe(client)
    logging.info("Loaded Snipe extension.")
