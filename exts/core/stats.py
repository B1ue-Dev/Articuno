"""
Stats command.

(C) 2022-2023 - Jimmy-Blue
"""

import logging
import datetime
import platform
import interactions
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)
import psutil
from utils import utils
from const import VERSION


class Stats(interactions.Extension):
    """Extension for /stats command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.uptime: int = int(round(datetime.datetime.now().timestamp()))
        self.python: str = platform.python_version()
        self.system: str = str(platform.platform())

    @interactions.slash_command(
        name="stats",
        description="Shows the stats of Articuno.",
    )
    async def stats(self, ctx: interactions.InteractionContext) -> None:
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

        button: list = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/809084067446259722",
            ),
        ]

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
                value=f"```ansi\n[2;33m{self.python}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Uptime",
                value=f"```\n{utils.pretty_date(self.uptime)}\n```",
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
                value=f"```ansi\n[2;35m{self.system}[0m\n```",
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
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=button)

    @prefixed_command(name="stats")
    async def _stats(self, ctx: PrefixedContext) -> None:
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

        button: list = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/809084067446259722",
            ),
        ]

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
                value=f"```ansi\n[2;33m{self.python}[0m\n```",
                inline=True,
            ),
            interactions.EmbedField(
                name="Uptime",
                value=f"```\n{utils.pretty_date(self.uptime)}\n```",
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
                value=f"```ansi\n[2;35m{self.system}[0m\n```",
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
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=button)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Stats(client)
    logging.debug("""[%s] Loaded Stats extension.""", log_time)
