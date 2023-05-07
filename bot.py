"""
Root bot file.

(C) 2022-2023 - B1ue-Dev
"""

import datetime
import interactions
from interactions.ext.prefixed_commands import setup, PrefixedHelpCommand
from const import TOKEN, VERSION


if __name__ == "__main__":

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
        print("".join(
            [
                f"""[{log_time}] Logged in as {client.user.username}.""",
                f"""Latency: {websocket}ms.""",
            ],
        ))

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
