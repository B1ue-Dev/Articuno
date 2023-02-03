"""
/truth_dare command.

(C) 2023 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from utils.utils import get_response

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

    @interactions.extension_command(
        name="truth_dare",
        description="NaN.",
    )
    async def truth_dare(self, ctx: interactions.CommandContext) -> None:
        """NaN."""

        await ctx.send("Select one of the topic to get started.", components=_buttons())

    @interactions.extension_component("/truth")
    async def _truth(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /truth."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x2d7d46,
            author=interactions.EmbedAuthor(
                name=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=ctx.user.avatar_url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: TRUTH  •  ID: {_id}  •  Rating: PG"
            ),
            timestamp=datetime.datetime.utcnow(),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.extension_component("/dare")
    async def _dare(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /dare."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0xd83c3e,
            author=interactions.EmbedAuthor(
                name=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=ctx.user.avatar_url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: DARE  •  ID: {_id}  •  Rating: PG"
            ),
            timestamp=datetime.datetime.utcnow(),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.extension_component("/wyr")
    async def _wyr(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /wyr."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x5865f2,
            author=interactions.EmbedAuthor(
                name=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=ctx.user.avatar_url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: Would you rather...  •  ID: {_id}  •  Rating: PG"
            ),
            timestamp=datetime.datetime.utcnow(),
        )
        await ctx.send(embeds=embed, components=_buttons())

    @interactions.extension_component("/paranoia")
    async def _paranoia(self, ctx: interactions.ComponentContext) -> None:
        """Callback for /paranoia."""

        url: str = self.base_url + ctx.custom_id
        resp: dict = await get_response(url=url, params={"rating": "PG"})
        _question: str = resp["question"]
        _id: str = resp["id"]

        embed = interactions.Embed(
            description=f"```\n{_question}\n```",
            color=0x4f545c,
            author=interactions.EmbedAuthor(
                name=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=ctx.user.avatar_url,
            ),
            footer=interactions.EmbedFooter(
                text=f"Type: Paranoia  •  ID: {_id}  •  Rating: PG"
            ),
            timestamp=datetime.datetime.utcnow(),
        )
        await ctx.send(embeds=embed, components=_buttons())


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    TruthDare(client)
    logging.debug("""[%s] Loaded TruthDare extension.""", log_time)
