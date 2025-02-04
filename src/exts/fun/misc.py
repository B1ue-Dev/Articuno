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


class Misc(interactions.Extension):
    """Extension for misc commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="jail",
        description="Jail a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def jail(
        self,
        ctx: HybridContext,
        user: interactions.Member,
    ) -> None:
        """Jail a user."""

        await ctx.defer()

        url: str = "https://some-random-api.com/canvas/jail"
        params: dict = {
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
        }

        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
        )
        await ctx.send(file=img)

    @hybrid_slash_command(
        name="tonikawa",
        description="Tonikawa a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def tonikawa(
        self,
        ctx: HybridContext,
        user: interactions.Member,
    ) -> None:
        """Tonikawa a user."""

        await ctx.defer()

        url: str = "https://some-random-api.com/canvas/tonikawa"
        params: dict = {
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
        }

        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
        )
        await ctx.send(file=img)

    @hybrid_slash_command(
        name="oogway",
        description="Oogway a quote.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="quote",
                description="The quote to process.",
                required=True,
                max_length=100,
            ),
        ],
        dm_permission=False,
    )
    async def oogway(
        self,
        ctx: HybridContext,
        *,
        quote: interactions.ConsumeRest[str],
    ) -> None:
        """Oogway a quote."""

        await ctx.defer()

        url: str = "https://some-random-api.com/canvas/oogway"
        params: dict = {"quote": str(quote)}

        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
        )
        await ctx.send(file=img)

    @hybrid_slash_command(
        name="trigger",
        description="Trigger a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def trigger(
        self,
        ctx: HybridContext,
        user: interactions.Member,
    ) -> None:
        """Trigger a user."""

        await ctx.defer()

        url: str = "https://some-random-api.com/canvas/triggered"
        params: dict = {
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
        }

        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.gif",
            file=resp,
        )
        await ctx.send(file=img)

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

        await ctx.defer()

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
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
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

        await ctx.defer()

        if len(user.user.username) >= 15:
            username = user.user.username[:12] + "..."
        else:
            username = user.user.username
        url = "https://some-random-api.com/canvas/youtube-comment"
        params = {
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
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
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="text",
                description="The custom text you want to set",
                required=False,
            ),
        ],
        dm_permission=False,
    )
    async def amogus(
        self, ctx: HybridContext, user: interactions.Member, text: str = None
    ) -> None:
        """Amogus."""

        await ctx.defer()

        if not text:
            text = f"""{user.user.username} was {"not" if str(random.choice(["true", "false"])) == "false" else ""} The Impostor"""
        url: str = "https://some-random-api.com/premium/amongus"
        params: dict = {
            "avatar": (
                user.avatar.url
                if user.guild_avatar is None
                else user.guild_avatar.url
            ),
            "username": user.user.username,
            "custom": text,
            "key": "hello",
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
