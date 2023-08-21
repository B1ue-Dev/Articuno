"""
Truth n Dare command.

(C) 2023 - B1ue-Dev
"""

import logging
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response, handle_username


def _buttons() -> "list[interactions.Button]":
    """
    :return: The button list for the command.
    :rtype: list[interactions.Button]
    """

    return [
        interactions.Button(
            style=interactions.ButtonStyle.SUCCESS,
            label="TRUTH",
            custom_id="/truth",
        ),
        interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="DARE",
            custom_id="/dare",
        ),
        interactions.Button(
            style=interactions.ButtonStyle.PRIMARY,
            label="Would you rather...",
            custom_id="/wyr",
        ),
        interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label="Paranoia",
            custom_id="/paranoia",
        ),
    ]


class TruthDare(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.base_url: str = "https://api.truthordarebot.xyz/v1"

    @hybrid_slash_command(
        name="truth_dare",
        description="Starts a Truth or Dare game.",
        aliases=["td"],
    )
    async def truth_dare(self, ctx: HybridContext) -> None:
        """Starts a Truth or Dare game."""

        await ctx.send(
            "Select one of the topic to get started.", components=_buttons()
        )

    @interactions.component_callback("/truth")
    async def _truth(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /truth."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x2D7D46,
            author=interactions.EmbedAuthor(
                name=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
                icon_url=ctx.user.avatar.url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: TRUTH  •  ID: {_id}  •  Rating: PG"
            ),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.component_callback("/dare")
    async def _dare(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /dare."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0xD83C3E,
            author=interactions.EmbedAuthor(
                name=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
                icon_url=ctx.user.avatar.url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: DARE  •  ID: {_id}  •  Rating: PG"
            ),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.component_callback("/wyr")
    async def _wyr(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /wyr."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x5865F2,
            author=interactions.EmbedAuthor(
                name=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
                icon_url=ctx.user.avatar.url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: Would you rather...  •  ID: {_id}  •  Rating: PG"
            ),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.component_callback("/paranoia")
    async def _paranoia(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /paranoia."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x4F545C,
            author=interactions.EmbedAuthor(
                name=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
                icon_url=ctx.user.avatar.url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: Paranoia  •  ID: {_id}  •  Rating: PG"
            ),
        )
        await ctx.send(embeds=embed, components=_buttons())


def setup(client) -> None:
    """Setup the extension."""
    TruthDare(client)
    logging.info("Loaded TruthDare extension.")
