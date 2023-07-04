"""
Root bot file.

(C) 2022-2023 - B1ue-Dev
"""

import asyncio
import logging
from datetime import datetime, timedelta
import interactions
from interactions.ext.prefixed_commands import setup as prefixed_setup
from interactions.ext.hybrid_commands import setup as hybrid_setup
from const import TOKEN, VERSION
from utils.utils import get_response


def get_local_time() -> datetime:
    """Returns latest UTC+7 time."""

    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(hours=7)
    return local_time


async def get_latest_release_version() -> str:
    """Returns the latest version of Articuno on GitHub."""

    url = "https://api.github.com/repos/B1ue-Dev/Articuno/releases/latest"
    response = await get_response(url)
    return response["tag_name"]


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.Formatter.converter = lambda *args: get_local_time().timetuple()
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.INFO,
    )

    client = interactions.Client(
        activity=interactions.Activity(
            name=f"for {VERSION}",
            type=interactions.ActivityType.WATCHING,
        ),
        intents=interactions.Intents.DEFAULT
        | interactions.Intents.MESSAGE_CONTENT
        | interactions.Intents.GUILD_MEMBERS,
        status=interactions.Status.ONLINE,
        send_command_tracebacks=False,
    )
    prefixed_setup(client, default_prefix="$")
    hybrid_setup(client)
    counted: bool = False
    """For stopping `GUILD_JOIN` spam on `STARTUP`"""

    client.load_extension("exts.core.__init__")
    client.load_extension("exts.fun.__init__")
    client.load_extension("exts.server.__init__")
    client.load_extension("exts.utils.__init__")

    @interactions.listen(interactions.events.Startup)
    async def on_startup() -> None:
        """Fires up READY"""

        global counted
        await asyncio.sleep(10)
        counted = True

        websocket = f"{client.latency * 1:.0f}"
        log_time = (datetime.utcnow() + timedelta(hours=7)).strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        print(
            "".join(
                [
                    f"""[{log_time}] Logged in as {client.user.username}.""",
                    f"""Latency: {websocket}ms.""",
                ],
            )
        )
        latest_release_version = await get_latest_release_version()
        if (
            latest_release_version is not None
            and latest_release_version > VERSION
        ):
            print(
                "".join(
                    [
                        "This Articuno version is not up to date.",
                        f"Your Articuno version: {VERSION}",
                        f"Latest version: {latest_release_version}",
                    ],
                )
            )
        else:
            print("You are on latest version. Enjoy using Articuno!")

    @interactions.listen()
    async def on_guild_join(guild: interactions.events.GuildJoin) -> None:
        """Fires when bot joins a new guild."""

        global counted
        if not counted:
            return

        _guild = guild.guild
        _channel = client.get_channel(957090401418899526)

        embed = interactions.Embed(title=f"Joined {_guild.name}")
        embed.add_field(name="ID", value=f"{_guild.id}", inline=True)
        embed.add_field(
            name="Joined on",
            value=f"{_guild.joined_at}",
            inline=True,
        )
        embed.add_field(
            name="Member", value=f"{_guild.member_count}", inline=True
        )
        embed.set_thumbnail(url=f"{_guild.icon.url}")

        await _channel.send(embeds=embed)

    @interactions.listen()
    async def on_guild_left(guild: interactions.events.GuildLeft) -> None:
        """Fires when bot leaves a guild."""

        _guild = guild.guild
        _channel = client.get_channel(957090401418899526)
        current_time: float = (
            datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        ).timestamp()

        embed = interactions.Embed(title=f"Left {_guild.name}")
        embed.add_field(name="ID", value=f"{_guild.id}", inline=True)
        embed.add_field(
            name="Left on",
            value=f"<t:{round(current_time)}:F>",
            inline=True,
        )
        embed.add_field(
            name="Member", value=f"{_guild.member_count}", inline=True
        )
        embed.set_thumbnail(url=f"{_guild.icon.url}")

        await _channel.send(embeds=embed)

    @interactions.listen(interactions.events.MessageCreate)
    async def bot_mentions(_msg: interactions.events.MessageCreate) -> None:
        """Check for bot mentions."""
        msg = _msg.message
        if (
            f"@{client.user.id}" in msg.content
            or f"<@{client.user.id}>" in msg.content
        ):
            embed = interactions.Embed(
                title="It seems like you mentioned me",
                description="".join(
                    [
                        "I could not help much but noticed you mentioned me.",
                        f"You can type ``/`` and choose **{client.user.username}**",
                        "to start using me. Alternatively, you can use ",
                        "`$help` or `/help` to see a list of available ",
                        "commands. Thank you for choosing Articuno. ^-^",
                    ],
                ),
                color=0x6AA4C1,
            )
            await msg.channel.send(embeds=embed)

    client.start(TOKEN)
