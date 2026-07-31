"""
Root bot file.

(C) 2022-2026 - B1ue-Dev
"""

import sys
import asyncio
import logging
from datetime import datetime, timedelta, timezone, UTC
import aiohttp
import interactions
import interactions.models as models
import colorlog
from interactions.ext.prefixed_commands import setup as prefixed_setup
from interactions.ext.hybrid_commands import setup as hybrid_setup

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from beanie import init_beanie

from src.common.error_handler import debug_system
from src.const import TOKEN, VERSION, MONGO_DB_URL, LOG_CHANNEL
from src.common.utils import get_response
from src.common.models import (
    tags,
    hangman_saves,
    wtp_easy_saves,
    wtp_hard_saves,
)


class Init:
    """Init."""

    @classmethod
    def get_local_time(cls) -> datetime:
        """Returns latest UTC+7 time."""

        UTC_PLUS_7 = timezone(timedelta(hours=7))
        return datetime.now(tz=UTC_PLUS_7)


    @classmethod
    async def get_latest_release_version(cls, session: aiohttp.ClientSession) -> str:
        """Returns the latest version of Articuno on GitHub."""

        url = "https://api.github.com/repos/B1ue-Dev/Articuno/releases/latest"
        response: dict = await get_response(url, session)
        return response["tag_name"]

    @classmethod
    def logger_config(cls) -> logging.Logger:
        """Set up the logging environment."""

        class ErrorAndDebugFilter(logging.Filter):
            def filter(self, record):
                return record.levelno in (
                    logging.ERROR,
                    logging.DEBUG,
                    logging.CRITICAL,
                )

        class StdOutFilter(logging.Filter):
            def filter(self, record):
                return record.levelno not in (
                    logging.ERROR,
                    logging.DEBUG,
                    logging.CRITICAL,
                )

        log = logging.getLogger()
        logging.Formatter.converter = (
            lambda *args: Init.get_local_time().timetuple()
        )
        log.setLevel(logging.INFO)

        formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s"
            + "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "fg_bold_yellow",
                "ERROR": "fg_bold_red",
                "CRITICAL": "red",
            },
        )

        # Stream handler for sys.stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.addFilter(StdOutFilter())
        log.addHandler(stdout_handler)

        # Stream handler for sys.stderr
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(formatter)
        stderr_handler.addFilter(ErrorAndDebugFilter())
        log.addHandler(stderr_handler)

        return log


client = interactions.Client(
    sync_interactions=True,
    sync_ext=True,
    delete_unused_application_cmds=True,
    intents=interactions.Intents.GUILDS
    | interactions.Intents.GUILD_MESSAGES
    | interactions.Intents.MESSAGE_CONTENT
    | interactions.Intents.GUILD_MEMBERS,
    status=interactions.Status.IDLE,
    activity=interactions.Activity(
        name="$help 🦅",
        type=interactions.ActivityType.WATCHING,
    ),
    send_command_tracebacks=False,
    logger=Init.logger_config(),
    voice_state_cache=interactions.utils.NullCache(),
    role_cache=interactions.utils.NullCache(),
)
prefixed_setup(client, default_prefix="$")
hybrid_setup(client)
counted: bool = False
"""For stopping `GUILD_JOIN` spam on `STARTUP`"""


@client.listen("startup")
async def on_startup() -> None:
    """Fires up READY"""

    websocket = ""
    global counted
    if debug_system is True:
        logging.warning("Skipping latency check in debug mode.")
        await asyncio.sleep(10)
        counted = True
    else:
        logging.info(
            "Articuno is starting up. Please wait, this may take a while."
        )
        await asyncio.sleep(60)
        counted = True
        websocket = f"{client.latency * 1:.0f}"

    msg = f"""✅ Logged in as {client.user.username}. """
    msg += f"Latency: {websocket}ms." if websocket else ""

    if hasattr(client, "mongo_client"):
        db_name = client.mongo_db.name
        try:
            stats = await client.mongo_db.command("dbstats")
            size_in_mb = stats["dataSize"] / (1024 ** 2)
            logging.info(
                f"""Connected to MongoDB cluster.
                Database: {db_name}
                Collections: {stats['collections']}
                Objects: {stats['objects']}
                Data Size: {size_in_mb:.2f} MB"""
            )
        except Exception as e:
            logging.warning(f"Failed to get MongoDB stats: {e}")

    logging.info(msg)


@client.listen()
async def on_guild_join(guild: interactions.events.GuildJoin) -> None:
    """Fires when bot joins a guild."""

    global counted
    if not counted:
        return

    await join_leave_msg(action="join", client=client, guild=guild)


@client.listen(event_name=interactions.events.GuildLeft)
async def on_guild_left(guild: interactions.events.GuildLeft) -> None:
    """Fires when bot leaves a guild."""

    await join_leave_msg(action="left", client=client, guild=guild)


@client.listen(event_name=interactions.events.Disconnect)
async def on_disconnect() -> None:
    """Handle bot disconnection."""

    logging.error("Disconnected! Terminating...")
    await client.stop()
    sys.exit(1)


@client.listen("message_create")
async def on_bot_mentions(_msg: interactions.events.MessageCreate) -> None:
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
                    "commands. Thank you for choosing Articuno.",
                ],
            ),
            color=0x6AA4C1,
        )
        await msg.channel.send(embeds=embed)


async def start() -> None:
    """Starts the bot."""

    client.session = aiohttp.ClientSession()

    if debug_system is True:
        logging.warning("Debug mode for Articuno is enabled.")
    else:
        latest_release_version = await Init.get_latest_release_version(client.session)
        if (
            latest_release_version is not None
            and latest_release_version > VERSION
        ):
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

    try:
        mongo_client = AsyncMongoClient(
            MONGO_DB_URL,
            server_api=ServerApi("1"),
            uuidRepresentation="standard",
        )
        client.mongo_client = mongo_client
        client.mongo_db = mongo_client["Articuno"]
        await mongo_client.admin.command("ping")
        logging.info("Successfully connected to MongoDB!")
        await init_beanie(
            client.mongo_db,
            document_models=[tags, hangman_saves, wtp_easy_saves, wtp_hard_saves],
        )
    except Exception as e:
        logging.error("Failed to connect to MongoDB: %s", e)
        return

    try:
        client.load_extension("src.common.jsk")
        client.load_extension("src.common.error_handler")
        client.load_extension("src.exts.core.__init__")
        client.load_extension("src.exts.fun.__init__")
        client.load_extension("src.exts.utils.__init__")

        await client.astart(TOKEN)
    except aiohttp.ClientError as e:
        logging.error("AIOHTTP Client Error: %s", e)
        sys.exit(1)
    except Exception as e:
        logging.error("An error occurred during bot startup: %s", e)
        sys.exit(1)
    finally:
        if client.session:
            await client.session.close()


async def join_leave_msg(
    action: str,
    client: interactions.Client,
    guild: interactions.events.GuildJoin | interactions.events.GuildLeft,
) -> None:
    _guild = guild.guild
    current_time: float = round(datetime.now(UTC).timestamp())
    function_name: str = ""

    if action == "join":
        function_name = "Joined"
    elif action == "left":
        function_name = "Left"

    embed = interactions.Embed(title=f"{function_name} {_guild.name}")
    embed.add_field(name="ID", value=f"{_guild.id}", inline=True)
    embed.add_field(
        name=f"{function_name} on",
        value=f"<t:{round(current_time)}:F>",
        inline=True,
    )
    embed.add_field(
        name="Member",
        value=f"{_guild.member_count}",
        inline=True,
    )
    if _guild.icon:
        embed.set_thumbnail(url=f"{_guild.icon.url}")

    payload: dict = models.discord.message.process_message_payload(
        embeds=embed
    )
    await client.http.create_message(channel_id=LOG_CHANNEL, payload=payload)
