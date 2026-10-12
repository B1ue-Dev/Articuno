"""
Snipe command.

(C) 2022-2026 - B1ue-Dev
"""

import logging
from datetime import datetime

import interactions
from interactions.ext.hybrid_commands import (
    HybridContext,
    hybrid_slash_command,
)

from src.common.task import start_task
from src.common.utils import handle_username


class Snipe(interactions.Extension):
    """Extension for /snipe command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self._cached: dict[str, list[dict[str, str]]] = {}
        self._cache_task = start_task("snipe-cache", self.clear_cache, 60)

    def drop(self, **kwargs) -> None:
        self._cache_task.cancel()
        super().drop(**kwargs)

    async def clear_cache(self) -> None:
        current_time = datetime.now().timestamp()
        for channel_id in list(self._cached.keys()):
            self._cached[channel_id] = [
                msg
                for msg in self._cached[channel_id]
                if current_time - float(msg["timestamp"]) < 300
            ]
            if not self._cached[channel_id]:
                self._cached.pop(channel_id, None)

    @interactions.listen(interactions.events.MessageDelete)
    async def on_message_delete(
        self, msg: interactions.events.MessageDelete
    ) -> None:
        """Listen to MESSAGE_DELETE and write to cache."""

        message: interactions.Message = msg.message
        if not isinstance(message, interactions.Message):
            return

        if message.author.bot:
            return

        _channel_id = str(message.channel.id)

        if not self._cached.get(_channel_id, None):
            self._cached[_channel_id] = []

        if len(self._cached[_channel_id]) >= 5:
            self._cached[_channel_id].pop(0)

        self._cached[_channel_id].append(
            {
                "content": message.content,
                "author_id": str(message.author.id),
                "timestamp": str(round(datetime.now().timestamp())),
            }
        )

    @hybrid_slash_command(
        name="snipe",
        description="Snipes the last deleted message from the current channel.",
        contexts=[0],
    )
    async def snipe(self, ctx: HybridContext) -> None:
        """Snipes the last deleted message from the current channel."""

        channel_id = str(ctx.channel_id)
        if not self._cached.get(channel_id, None):
            return await ctx.send("No message to snipe.")

        embed = interactions.Embed(
            title="Deleted Messages History",
            footer=interactions.EmbedFooter(
                text=f"Requested by {handle_username(ctx.author.user.username, ctx.author.user.discriminator)}",
                icon_url=ctx.author.avatar_url,
            ),
            description="",
        )
        for i in self._cached[channel_id]:
            content = i["content"][:300] + (
                "…" if len(i["content"]) > 300 else ""
            )
            embed.description += f"""<@{i["author_id"]}>: {content} - <t:{i["timestamp"]}:R>\n"""  # type: ignore

        await ctx.send(embed=embed)


def setup(client) -> None:
    """Setup the extension."""
    Snipe(client)
    logging.info("Loaded Snipe extension.")
