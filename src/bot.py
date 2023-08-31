"""
Root bot file.

(C) 2022-2023 - B1ue-Dev
"""

import asyncio
import logging
import datetime
import aiohttp
import interactions
import colorlog
from interactions.ext.prefixed_commands import setup as prefixed_setup
from interactions.ext.hybrid_commands import setup as hybrid_setup
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from beanie import init_beanie
from src.const import TOKEN, VERSION, MONGO_DB_URL
from src.utils.utils import get_response, tags, get_local_time


async def get_latest_release_version() -> str:
    """Returns the latest version of Articuno on GitHub."""

    url = "https://api.github.com/repos/B1ue-Dev/Articuno/releases/latest"
    response = await get_response(url)
    return response["tag_name"]


def logger_config() -> logging.Logger:
    """Setup the logging environment."""

    log = logging.getLogger()
    logging.Formatter.converter = lambda *args: get_local_time().timetuple()
    log.setLevel(logging.INFO)
    format_str = (
        "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    )
    date_format = "%d/%m/%Y %H:%M:%S"
    cformat = "%(log_color)s" + format_str
    colors = {
        "DEBUG": "white",
        "INFO": "white",
        "WARNING": "fg_bold_yellow",
        "ERROR": "fg_bold_red",
        "CRITICAL": "red",
    }
    formatter = colorlog.ColoredFormatter(
        fmt=cformat,
        datefmt=date_format,
        log_colors=colors,
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log


client = interactions.Client(
    sync_interactions=True,
    sync_ext=True,
    delete_unused_application_cmds=True,
    activity=interactions.Activity(
        name=f"for {VERSION}",
        type=interactions.ActivityType.WATCHING,
    ),
    intents=interactions.Intents.DEFAULT
    | interactions.Intents.MESSAGE_CONTENT
    | interactions.Intents.GUILD_MEMBERS,
    status=interactions.Status.ONLINE,
    send_command_tracebacks=False,
    logger=logger_config(),
)
prefixed_setup(client, default_prefix="$")
hybrid_setup(client)
counted: bool = False
"""For stopping `GUILD_JOIN` spam on `STARTUP`"""


@client.listen(interactions.events.Startup)
async def on_startup() -> None:
    """Fires up READY"""

    global counted
    await asyncio.sleep(10)
    counted = True

    websocket = f"{client.latency * 1:.0f}"
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")

    print(
        "".join(
            [
                f"""[{log_time}] Logged in as {client.user.username}.""",
                f"""Latency: {websocket}ms.""",
            ],
        )
    )
    latest_release_version = await get_latest_release_version()
    if latest_release_version is not None and latest_release_version > VERSION:
        print(
            "".join(
                [
                    "This Articuno version is not up to date.",
                    f"Your Articuno version: {VERSION}\n",
                    f"Latest version: {latest_release_version}",
                ],
            )
        )
    else:
        print("You are on latest version. Enjoy using Articuno!")


@client.listen(interactions.events.GuildJoin)
async def on_guild_join(guild: interactions.events.GuildJoin) -> None:
    """Fires when bot joins a new guild."""

    global counted
    if not counted:
        return

    _guild = guild.guild
    _channel = client.get_channel(957090401418899526)
    current_time: float = round(
        datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    )

    embed = interactions.Embed(title=f"Joined {_guild.name}")
    embed.add_field(name="ID", value=f"{_guild.id}", inline=True)
    embed.add_field(
        name="Joined on",
        value=f"<t:{round(current_time)}:F>",
        inline=True,
    )
    embed.add_field(name="Member", value=f"{_guild.member_count}", inline=True)
    if _guild.icon:
        embed.set_thumbnail(url=f"{_guild.icon.url}")

    await _channel.send(embeds=embed)


@client.listen(interactions.events.GuildLeft)
async def on_guild_left(guild: interactions.events.GuildLeft) -> None:
    """Fires when bot leaves a guild."""

    _guild = guild.guild
    _channel = client.get_channel(957090401418899526)
    current_time: float = round(
        datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    )

    embed = interactions.Embed(title=f"Left {_guild.name}")
    embed.add_field(name="ID", value=f"{_guild.id}", inline=True)
    embed.add_field(
        name="Left on",
        value=f"<t:{round(current_time)}:F>",
        inline=True,
    )
    embed.add_field(name="Member", value=f"{_guild.member_count}", inline=True)
    if _guild.icon:
        embed.set_thumbnail(url=f"{_guild.icon.url}")

    await _channel.send(embeds=embed)


@client.listen(interactions.events.MessageCreate)
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
                    " to start using me. Alternatively, you can use ",
                    "`$help` or `/help` to see a list of available ",
                    "commands. Thank you for choosing Articuno. ^-^",
                ],
            ),
            color=0x6AA4C1,
        )
        await msg.channel.send(embeds=embed)


async def start() -> None:
    """Starts the bot."""

    mongo_client = AsyncIOMotorClient(MONGO_DB_URL, server_api=ServerApi("1"))
    try:
        mongo_client.admin.command("ping")
        logging.info("Successfully connected to MongoDB!")
    except Exception as e:
        logging.critical(e)
    await init_beanie(mongo_client["Articuno"], document_models=[tags])

    client.session = aiohttp.ClientSession()

    client.load_extension("src.utils.jsk")
    client.load_extension("src.utils.error_handler")
    client.load_extension("src.exts.core.__init__")
    client.load_extension("src.exts.fun.__init__")
    client.load_extension("src.exts.utils.__init__")

    try:
        await client.astart(TOKEN)
    finally:
        await client.session.close()
