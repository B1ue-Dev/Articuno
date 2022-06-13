"""
This module is for basic bot information commands.

(C) 2022 - Jimmy-Blue
"""

import platform
import datetime
import interactions
import psutil
from utils import cache
from utils import utils
from const import VERSION

load_time = datetime.datetime.now()


class Basic(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(name="ping", description="Ping Articuno")
    async def _ping(self, ctx: interactions.CommandContext):
        websocket = f"{self.client.latency * 1:.0f}"

        if int(websocket) < int(99):
            message = f"{websocket}ms <:Connection_Best:936294842286342204>"
        elif int(100) <= int(websocket) < int(199):
            message = f"{websocket}ms<:Connection_Stable:936294747516067841>"
        elif int(websocket) > int(200):
            message = f"{websocket}ms <:Connection_Bad:936294724954894436>"

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        embed = interactions.Embed(
            title=":ping_pong: Pong!",
            description=f"Websocket: {message}",
            color=0xFF8B00,
            footer=footer,
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="stats", description="Shows the stats of Articuno"
    )
    async def _stats(self, ctx: interactions.CommandContext):
        proc = psutil.Process()
        mems = proc.memory_full_info()
        cpus = psutil.cpu_percent()
        thread_counts = proc.num_threads()
        mem = f"{utils.natural_size(mems.rss)}\n{utils.natural_size(mems.vms)}"
        cpu = f"{cpus}%\n{thread_counts} Threads"
        version = VERSION
        latency = f"{self.client.latency * 1:.0f}ms"
        python = platform.python_version()
        os = str(platform.platform())
        uptime = f"<t:{round(load_time.timestamp())}:R>"
        _set_user_count: set = set()
        _set_guild_count: set = set()
        for guild in cache.__cached__:
            _set_guild_count.add(guild)
            for member in cache.__cached__[guild]:
                _set_user_count.add(member)
        user_count = len(_set_user_count)
        guild_count = len(_set_guild_count)

        github = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="GitHub",
            url="https://github.com/Articuno-org/Articuno",
        )

        fields = [
            interactions.EmbedField(name="Version", value=version, inline=True),
            interactions.EmbedField(name="Guilds", value=guild_count, inline=True),
            interactions.EmbedField(name="Users", value=user_count, inline=True),
            interactions.EmbedField(name="Latency", value=latency, inline=True),
            interactions.EmbedField(name="Python", value=python, inline=True),
            interactions.EmbedField(name="Uptime", value=uptime, inline=True),
            interactions.EmbedField(name="CPU", value=cpu, inline=True),
            interactions.EmbedField(name="Memory", value=mem, inline=True),
            interactions.EmbedField(name="System", value=os, inline=True),
        ]
        thumbnail = interactions.EmbedImageStruct(url=self.client.me.icon_url)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Articuno Stats",
            color=0x6AA4C1,
            thumbnail=thumbnail,
            footer=footer,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=[github])

    @interactions.extension_command(
        name="credits", description="Developers/Contributors to this project"
    )
    async def _credits(self, ctx: interactions.CommandContext):
        profile = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev/",
        )

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained, developed and improved by Blue#2095.",
            color=0x6AA4C1,
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
        ]

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="Click the button below to invite Articuno to your server.\n\nIf you have any questions, feel free to join the support server.",
            color=0x6AA4C1,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)


def setup(client):
    Basic(client)
