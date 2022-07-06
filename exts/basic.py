"""
This module is for basic bot information command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import platform
import interactions
import psutil
from utils import cache, utils
from const import VERSION


class Basic(interactions.Extension):
    _uptime = datetime.datetime.now()
    """Extension for basic bot commands."""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="ping",
        description="Ping Articuno",
    )
    async def _ping(self, ctx: interactions.CommandContext):
        websocket = int(f"{self.client.latency * 1:.0f}")
        if websocket < 100:
            color = 0x3ba55d
        elif 100 <= websocket < 175:
            color = 0xcb8515
        elif 175 <= websocket:
            color = 0xed4245

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title=":ping_pong: Pong!",
            description=f"Websocket: {websocket}ms",
            color=color,
            footer=footer,
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="stats",
        description="Shows the stats of Articuno",
    )
    async def _stats(self, ctx: interactions.CommandContext):
        proc = psutil.Process()
        mem = f"{utils.natural_size(proc.memory_full_info().rss)}\n{utils.natural_size(proc.memory_full_info().vms)}"
        cpu = f"{psutil.cpu_percent()}%\n{proc.num_threads()} Threads"
        latency = f"{self.client.latency * 1:.0f}ms"
        python = platform.python_version()
        system = str(platform.platform())
        uptime = f"<t:{round(self._uptime.timestamp())}:R>"
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
            interactions.EmbedField(name="Python", value=python, inline=True),
            interactions.EmbedField(name="Uptime", value=uptime, inline=True),
            interactions.EmbedField(name="CPU", value=cpu, inline=True),
            interactions.EmbedField(name="Memory", value=mem, inline=True),
            interactions.EmbedField(name="System", value=system, inline=True),
        ]
        thumbnail = interactions.EmbedImageStruct(url=self.client.me.icon_url)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Articuno Stats",
            color=0x7cb7d3,
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=button)

    @interactions.extension_command(
        name="credits",
        description="Developers/Contributors to this project"
    )
    async def _credits(self, ctx: interactions.CommandContext):
        profile = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev/",
        )

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained, developed and improved by Blue#2095.",
            color=0x7cb7d3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=[profile])

    @interactions.extension_command(
        name="invite", description="Invite Articuno to your server"
    )
    async def _invite(self, ctx: interactions.CommandContext):
        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Add me to your server",
                url="https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=1644905889023&scope=bot%20applications.commands",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Support server",
                url="https://discord.gg/SPd5RNhwfY",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Vote me on Top.gg",
                url="https://top.gg/bot/809084067446259722/vote",
            ),
        ]

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="Click the button below to invite Articuno to your server.\n\nIf you have any questions, feel free to join the support server.",
            color=0x7cb7d3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)


def setup(client):
    """Loads the Basic extension."""
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
    Basic(client)
    logging.debug("""[%s] Loaded Basic extension.""", log_time)
    print(f"[{log_time}] Loaded Basic extension.")
