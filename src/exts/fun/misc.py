"""
Miscellaneous commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import random
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response
from src.const import SOME_RANDOM_API


class Misc(interactions.Extension):
    """Extension for misc commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="tweet",
        description="Sends a Twitter tweet.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="comment",
                description="Comment",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def tweet(
        self,
        ctx: HybridContext,
        user: interactions.Member,
        comment: interactions.ConsumeRest[str],
    ) -> None:
        """Sends a Twitter tweet."""

        if len(user.user.username) >= 15:
            username = user.user.username[:12] + "..."
        else:
            username = user.user.username
        if user.nick is not None:
            if len(user.nick) >= 32:
                nick = user.nick[:29] + "..."
            else:
                nick = user.nick
        else:
            nick = username
        url: str = "https://some-random-api.com/canvas/tweet"
        params: dict = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "username": username,
            "displayname": nick,
            "comment": comment,
            "theme": "dark",
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
            description=f"{user.username} tweet.",
        )
        await ctx.send(file=img)

    @hybrid_slash_command(
        name="youtube",
        description="Sends a YouTube comment.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="comment",
                description="Comment",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def youtube(
        self,
        ctx: HybridContext,
        user: interactions.Member,
        comment: interactions.ConsumeRest[str],
    ) -> None:
        """Sends a YouTube comment."""

        if len(user.user.username) >= 15:
            username = user.user.username[:12] + "..."
        else:
            username = user.user.username
        url = "https://some-random-api.com/canvas/youtube-comment"
        params = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "username": username,
            "comment": comment,
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
            description=f"{user.username} YouTube comment.",
        )
        await ctx.send(file=img)

    @hybrid_slash_command(
        name="amogus",
        description="Amogus.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            )
        ],
        dm_permission=False,
    )
    async def amogus(
        self, ctx: HybridContext, user: interactions.Member
    ) -> None:
        """Amogus."""

        await ctx.defer()
        url: str = "https://some-random-api.com/premium/amongus"
        params: dict = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "username": user.user.username,
            "key": SOME_RANDOM_API,
            "imposter": str(random.choice(["true", "false"])),
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.gif",
            file=resp,
            description="Amogus.",
        )
        await ctx.send(file=img)


def setup(client) -> None:
    """Setup the extension."""
    Misc(client)
    logging.info("Loaded Misc extension.")
