"""
/ping command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions


class Ping(interactions.Extension):
    """Extension for /ping command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="ping",
        description="Ping Articuno.",
    )
    async def ping(self, ctx: interactions.SlashContext) -> None:
        """Ping Articuno."""

        websocket: int = int(f"{self.client.latency * 1000:.0f}")
        color: int = 0
        if websocket < 100:
            color = 0x3BA55D
        elif 100 <= websocket < 175:
            color = 0xCB8515
        elif 175 <= websocket:
            color = 0xED4245

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
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
    Ping(client)
    logging.info("Loaded Ping extension.")
