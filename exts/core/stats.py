"""
Stats command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import platform
import interactions
import psutil
from utils import cache, utils
from const import VERSION


class Stats(interactions.Extension):
    """Extension for /stats command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.uptime = f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        self.python = platform.python_version()
        self.system = str(platform.platform())

    @interactions.extension_command(
        name="stats",
        description="Shows the stats of Articuno",
    )
    async def _stats(self, ctx: interactions.CommandContext):
        proc = psutil.Process()
        mem = f"""{utils.natural_size(proc.memory_full_info().rss)}
            {utils.natural_size(proc.memory_full_info().vms)}"""
        cpu = f"{psutil.cpu_percent()}%\n{proc.num_threads()} Threads"
        latency = f"{self.client.latency * 1:.0f}ms"
        guild_count = len(cache.Storage().get_all_guilds())
        user_count = cache.Storage().get_all_users()

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Articuno-org/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/809084067446259722",
            ),
        ]

        fields = [
            interactions.EmbedField(name="Version", value=VERSION, inline=True),
            interactions.EmbedField(name="Guilds", value=guild_count, inline=True),
            interactions.EmbedField(name="Users", value=user_count, inline=True),
            interactions.EmbedField(name="Latency", value=latency, inline=True),
            interactions.EmbedField(name="Python", value=self.python, inline=True),
            interactions.EmbedField(name="Uptime", value=self.uptime, inline=True),
            interactions.EmbedField(name="CPU", value=cpu, inline=True),
            interactions.EmbedField(name="Memory", value=mem, inline=True),
            interactions.EmbedField(name="System", value=self.system, inline=True),
        ]
        thumbnail = interactions.EmbedImageStruct(url=self.client.me.icon_url)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
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
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Stats(client)
    logging.debug("""[%s] Loaded Stats extension.""", log_time)
    print(f"[{log_time}] Loaded Stats extension.")
