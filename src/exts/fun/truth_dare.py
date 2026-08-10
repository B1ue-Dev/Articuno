"""
Truth n Dare command.

(C) 2023-2026 - B1ue-Dev
"""

import logging
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.common.utils import get_response, handle_username


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

        await TruthDare.send_message(
            self, self.base_url + ctx.custom_id, ctx, "Truth"
        )

    @interactions.component_callback("/dare")
    async def _dare(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /dare."""

        await TruthDare.send_message(
            self, self.base_url + ctx.custom_id, ctx, "Dare"
        )

    @interactions.component_callback("/wyr")
    async def _wyr(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /wyr."""

        await TruthDare.send_message(
            self, self.base_url + ctx.custom_id, ctx, "Would you rather"
        )

    @interactions.component_callback("/paranoia")
    async def _paranoia(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /paranoia."""

        await TruthDare.send_message(
            self, self.base_url + ctx.custom_id, ctx, "Paranoia"
        )

    async def send_message(
        self, url: str, ctx: interactions.ComponentContext, type_text: str
    ) -> None:
        """Send message handler."""

        resp: dict = await get_response(
            url, session=self.client.session, params={"rating": "PG"}
        )
        if not resp:
            return await ctx.send(
                "Unavailable at the moment. Please try again later",
                ephemeral=True,
            )
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"## {_question}",
            color=0x4F545C,
            author=interactions.EmbedAuthor(
                name=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
                icon_url=ctx.user.avatar.url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: {type_text}  •  ID: {_id}  •  Rating: PG"
            ),
        )
        await ctx.send(embeds=embed, components=_buttons())


def setup(client) -> None:
    """Setup the extension."""
    TruthDare(client)
    logging.info("Loaded TruthDare extension.")
