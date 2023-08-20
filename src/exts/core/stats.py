"""
/stats command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
import psutil
from src.utils import utils, jsk
from src.const import VERSION


class Stats(interactions.Extension):
    """Extension for /stats command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.button: list(interactions.Button) = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Site",
                url="https://blue.is-a.dev/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/B1ue-Dev/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/809084067446259722",
            ),
        ]

    @hybrid_slash_command(
        name="stats",
        description="Shows the stats of Articuno.",
    )
    async def stats(self, ctx: HybridContext) -> None:
        """Shows the stats of Articuno."""

        proc: "psutil.Process" = psutil.Process()
        mem: str = (
            f"{utils.natural_size(proc.memory_full_info().rss)}"
            f"\n{utils.natural_size(proc.memory_full_info().vms)}"
        )
        cpu: str = f"{psutil.cpu_percent()}%\n{proc.num_threads()} Threads"
        latency: str = f"{self.client.latency * 1000:.0f}ms"
        user_count: int = 0
        for guild in self.client.guilds:
            user_count += guild.member_count

        fields: list = [
            interactions.EmbedField(
                name="Version",
                value=f"```ansi\n[2;34m{VERSION}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Guilds",
                value=f"```\n{len(self.client.guilds)}\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Users", value=f"```\n{user_count}\n```", inline=True
            ),
            interactions.EmbedField(
                name="Latency", value=f"```\n{latency}\n```", inline=True
            ),
            interactions.EmbedField(
                name="Python",
                value=f"```ansi\n[2;33m{jsk._Jsk.py}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Uptime",
                value=f"```\n{utils.pretty_date(jsk._Jsk.uptime)}\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="CPU",
                value=f"```ansi\n[2;31m{cpu}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Memory",
                value=f"```ansi\n[2;36m{mem}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="System",
                value=f"```ansi\n[2;35m{jsk._Jsk.platf}[0m\n```",
                inline=True,
            ),
        ]
        thumbnail = interactions.EmbedAttachment(
            url=self.client.user.avatar.url
        )
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Articuno Stats",
            color=0x7CB7D3,
            url="https://blue.is-a.dev/Articuno",
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=self.button)


def setup(client) -> None:
    """Setup the extension."""
    Stats(client)
    logging.info("Loaded Stats extension.")
