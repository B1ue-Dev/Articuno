"""
Edited command with full version history.

(C) 2022-2026 - B1ue-Dev
"""

import logging
from datetime import datetime
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.common.utils import handle_username


class Edited(interactions.Extension):
    """Extension for /edited command with full edit history."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        # channel_id -> message_id -> list of versions
        self._cached: dict[str, dict[str, list[dict[str, str]]]] = {}
        self.clear_cache.start()

    @interactions.Task.create(interactions.IntervalTrigger(seconds=60))
    async def clear_cache(self) -> None:
        current_time = datetime.now().timestamp()
        for channel_id in list(self._cached.keys()):
            for message_id in list(self._cached[channel_id].keys()):
                versions = self._cached[channel_id][message_id]
                if (
                    versions
                    and current_time - float(versions[-1]["timestamp"]) >= 300
                ):
                    self._cached[channel_id].pop(message_id, None)
            if not self._cached[channel_id]:
                self._cached.pop(channel_id, None)

    @interactions.listen(interactions.events.MessageUpdate)
    async def on_message_edit(
        self, msg: interactions.events.MessageUpdate
    ) -> None:
        """Track all versions of an edited message."""

        before = msg.before
        after = msg.after

        if not isinstance(before, interactions.Message) or not after:
            return

        if before.author.bot:
            return

        if before.content == after.content:
            return

        channel_id = str(before.channel.id)
        message_id = str(before.id)

        if channel_id not in self._cached:
            self._cached[channel_id] = {}

        if message_id not in self._cached[channel_id]:
            if len(self._cached[channel_id]) >= 5:
                oldest_message_id = list(self._cached[channel_id].keys())[0]
                self._cached[channel_id].pop(oldest_message_id)

            # First version is the original
            self._cached[channel_id][message_id] = [
                {
                    "content": before.content,
                    "timestamp": str(round(before.timestamp.timestamp()))
                    if hasattr(before, "timestamp") and before.timestamp
                    else str(round(datetime.now().timestamp())),
                    "author_id": str(before.author.id),
                }
            ]

        if len(self._cached[channel_id][message_id]) >= 5:
            self._cached[channel_id][message_id].pop(1)

        # Add the new version (after edit)
        self._cached[channel_id][message_id].append(
            {
                "content": after.content,
                "timestamp": str(round(datetime.now().timestamp())),
                "author_id": str(before.author.id),
            }
        )

    @hybrid_slash_command(
        name="edited",
        description="Shows all versions of edited messages in this channel.",
        contexts=[0],
    )
    async def edited(self, ctx: HybridContext) -> None:
        """Send embed with full edit history per message."""

        channel_id = str(ctx.channel_id)
        if channel_id not in self._cached or not self._cached[channel_id]:
            return await ctx.send("No edited messages to snipe.")

        embed = interactions.Embed(
            title="Edited Messages (History)",
            footer=interactions.EmbedFooter(
                text=f"Requested by {handle_username(ctx.author.user.username, ctx.author.user.discriminator)}",
                icon_url=ctx.author.avatar_url,
            ),
            description="",
        )

        shown = 0
        for message_id, versions in reversed(self._cached[channel_id].items()):
            if shown >= 3:
                break

            author_id = versions[0]["author_id"]

            msg_desc = (
                f"<@{author_id}> edited a message (ID: `{message_id}`):\n"
            )

            for i, version in enumerate(versions):
                label = "Original" if i == 0 else f"Edit {i}"
                content = version["content"][:300] + (
                    "…" if len(version["content"]) > 300 else ""
                )
                msg_desc += (
                    f"**{label}:** {content} (<t:{version['timestamp']}:R>)\n"
                )

            msg_desc += "\n"

            if len(embed.description) + len(msg_desc) > 4096:
                break

            embed.description += msg_desc
            shown += 1

        await ctx.send(embed=embed)


def setup(client) -> None:
    """Setup the extension."""
    Edited(client)
    logging.info("Loaded Edited extension with full history.")
