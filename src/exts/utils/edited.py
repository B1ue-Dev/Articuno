"""
Edited command with full version history.

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
from src.utils.utils import handle_username


class Edited(interactions.Extension):
    """Extension for /edited command with full edit history."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        # channel_id -> message_id -> list of versions
        self._cached: dict[str, dict[str, list[dict[str, str]]]] = {}

    @interactions.listen(interactions.events.MessageUpdate)
    async def on_message_edit(
        self, msg: interactions.events.MessageUpdate
    ) -> None:
        """Track all versions of an edited message."""

        before = msg.before
        after = msg.after

        if not isinstance(before, interactions.Message) or not after:
            return

        channel_id = str(before.channel.id)
        message_id = str(before.id)

        if channel_id not in self._cached:
            self._cached[channel_id] = {}

        if message_id not in self._cached[channel_id]:
            # First version is the original
            self._cached[channel_id][message_id] = [
                {
                    "content": before.content,
                    "timestamp": str(round(datetime.now().timestamp())),
                    "author_id": str(before.author.id),
                }
            ]

        # Add the new version (after edit)
        self._cached[channel_id][message_id].append(
            {
                "content": after.content,
                "timestamp": str(round(datetime.now().timestamp())),
                "author_id": str(before.author.id),
            }
        )

        async def delete_history():
            await asyncio.sleep(300)
            try:
                self._cached[channel_id].pop(message_id)
                if not self._cached[channel_id]:
                    self._cached.pop(channel_id)
            except KeyError:
                pass

        asyncio.create_task(delete_history())

    @hybrid_slash_command(
        name="edited",
        description="Shows all versions of edited messages in this channel.",
        dm_permission=False,
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
                icon_url=ctx.author.avatar.url,
            ),
            description="",
        )

        shown = 0
        for message_id, versions in reversed(self._cached[channel_id].items()):
            if shown >= 3:
                break

            author_id = versions[0]["author_id"]
            embed.description += (
                f"<@{author_id}> edited a message (ID: `{message_id}`):\n"
            )
            for i, version in enumerate(versions):
                label = "Original" if i == 0 else f"Edit {i}"
                embed.description += (
                    f"**{label}:** {version['content']} "
                    f"(<t:{version['timestamp']}:R>)\n"
                )
            embed.description += "\n"
            shown += 1

        await ctx.send(embed=embed)


def setup(client) -> None:
    """Setup the extension."""
    Edited(client)
    logging.info("Loaded Edited extension with full history.")
