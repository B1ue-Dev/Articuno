"""
Snipe command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
from datetime import datetime
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.common.utils import handle_username


class Snipe(interactions.Extension):
    """Extension for /snipe command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self._cached: dict[str, str] = {}

    @interactions.listen(interactions.events.MessageDelete)
    async def on_message_delete(
        self, msg: interactions.events.MessageDelete
    ) -> None:
        """Listen to MESSAGE_DELETE and write to cache."""

        message: interactions.Message = msg.message
        if not isinstance(message, interactions.Message):
            return

        _channel_id = str(message.channel.id)

        if not self._cached.get(_channel_id, None):
            self._cached[_channel_id] = []

        if len(self._cached[_channel_id]) == 5:
            self._cached[_channel_id].pop(0)

        self._cached[_channel_id].append(
            {
                "content": message.content,
                "author_id": str(message.author.id),
                "timestamp": str(round(datetime.now().timestamp())),
            }
        )

        async def delete_message():
            try:
                _item = self._cached[_channel_id][-1:][0]
                await asyncio.sleep(300)
                self._cached[_channel_id].remove(_item)
            except ValueError:
                pass

            if len(self._cached[_channel_id]) == 0:
                self._cached.pop(_channel_id)

        asyncio.create_task(delete_message())

    @hybrid_slash_command(
        name="snipe",
        description="Snipes the last deleted message from the current channel.",
        dm_permission=False,
    )
    async def snipe(self, ctx: HybridContext) -> None:
        """Snipes the last deleted message from the current channel."""

        channel_id = str(ctx.channel_id)
        if not self._cached.get(channel_id, None):
            return await ctx.send("No message to snipe.")

        embed = interactions.Embed(
            title="Deleted Messages (History)",
            footer=interactions.EmbedFooter(
                text=f"Requested by {handle_username(ctx.author.user.username, ctx.author.user.discriminator)}",
                icon_url=ctx.author.avatar.url,
            ),
            description="",
        )
        for i in self._cached[channel_id]:
            embed.description += f"""<@{i["author_id"]}>: {i["content"]} - <t:{i["timestamp"]}:R>\n"""  # type: ignore

        await ctx.send(embed=embed)


def setup(client) -> None:
    """Setup the extension."""
    Snipe(client)
    logging.info("Loaded Snipe extension.")
