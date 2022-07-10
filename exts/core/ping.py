"""
Ping command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions


class Ping(interactions.Extension):
    """Extension for /ping command."""
    def __init__(self, client: interactions.Client) -> None:
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


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Ping(client)
    logging.debug("""[%s] Loaded Ping extension.""", log_time)
    print(f"[{log_time}] Loaded Ping extension.")
