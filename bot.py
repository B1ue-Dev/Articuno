"""
Root bot file.

(C) 2022-2023 - B1ue-Dev
"""

import sys
import logging
import time
import datetime
import interactions
from interactions.ext.prefixed_commands import setup, PrefixedHelpCommand
from const import TOKEN, VERSION
from utils.utils import get_response

def get_local_time() -> datetime:
    """Returns latest UTC+7 time."""

    utc_time = datetime.datetime.utcnow()
    local_time = utc_time + datetime.timedelta(hours=7)
    return local_time

async def get_latest_release_version() -> str:
    """Returns the latest version of Articuno on GitHub."""

    url = f"https://api.github.com/repos/B1ue-Dev/Articuno/releases/latest"
    response = await get_response(url)
    return response["tag_name"]

if __name__ == "__main__":
    logger = logging.getLogger()
    logging.Formatter.converter = lambda *args: get_local_time().timetuple()
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=0,
    )

    client = interactions.Client(
        activity=interactions.Activity(
            name=f"for {VERSION}",
            type=interactions.ActivityType.WATCHING,
        ),
        basic_logging=True,
        intents=interactions.Intents.DEFAULT
        | interactions.Intents.MESSAGE_CONTENT
        | interactions.Intents.GUILD_MEMBERS,
        status=interactions.Status.ONLINE,
        send_command_tracebacks=False,
    )

    setup(client, default_prefix="$")
    PrefixedHelpCommand(
        client,
        show_usage=True,
        embed_color=0x7CB7D3,
        not_found_message="Command `{cmd_name}` not found.",
    ).register()
    client.load_extension("exts.core.__init__")
    client.load_extension("exts.fun.__init__")
    client.load_extension("exts.server.__init__")
    client.load_extension("exts.utils.__init__")
    client.load_extension("utils.error")

    @client.listen(interactions.events.Startup)
    async def on_startup() -> None:
        """Fires up READY"""
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
            print("".join(
                [
                    "This Articuno version is not up to date.",
                    f"Your Articuno version: {VERSION}",
                    f"Latest version: {latest_release_version}",
                ],
            ))
        else:
            print(
                """                _   _                        
     /\        | | (_)                       
    /  \   _ __| |_ _  ___ _   _ _ __   ___  
   / /\ \ | '__| __| |/ __| | | | '_ \ / _ \ 
  / ____ \| |  | |_| | (__| |_| | | | | (_) |
 /_/    \_\_|   \__|_|\___|\__,_|_| |_|\___/ 
                                                              
                            - By B1ue-Dev - 
                            
You are on latest version. Enjoy using Articuno!"""
            )

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
                        f"I could not help much but noticed you mentioned me.",
                        f"You can type ``/`` and choose **{client.user.username}**",
                        f"to see a list of available commands.",
                    ],
                ),
                color=0x6AA4C1,
            )
            await msg.channel.send(embeds=embed)

    client.start(TOKEN)
