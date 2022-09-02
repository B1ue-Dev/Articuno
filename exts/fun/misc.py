"""
This module is for misc commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import random
import interactions
from utils.utils import get_response
from const import APIKEY as apikey


class Misc(interactions.Extension):
    """Extension for misc commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="hornycard",
        description="Send a hornycard.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=False,
            )
        ],
    )
    async def _hornycard(
        self, ctx: interactions.CommandContext, user: interactions.Member = None
    ):
        """Send a hornycard."""

        if user is None:
            user = ctx.user.user

        avatar_url = user.avatar_url
        url = "https://some-random-api.ml/canvas/horny"
        params = {
            "avatar": avatar_url,
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @interactions.extension_command(
        name="simpcard",
        description="Send a simpcard.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=False,
            )
        ],
    )
    async def _simpcard(
        self, ctx: interactions.CommandContext, user: interactions.Member = None
    ):
        """Send a simpcard."""

        if user is None:
            user = ctx.user

        avatar_url = user.avatar_url
        url = "https://some-random-api.ml/canvas/simpcard"
        params = {"avatar": avatar_url}
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @interactions.extension_command(
        name="tweet",
        description="Send a Twitter tweet.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="comment",
                description="Comment",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="background",
                description="Background of the Tweet",
                required=False,
                choices=[
                    interactions.Choice(name="Light", value="light"),
                    interactions.Choice(name="Dim", value="dim"),
                    interactions.Choice(name="Dark", value="dark"),
                ],
            ),
        ],
        dm_permission=False,
    )
    async def _tweet(
        self,
        ctx: interactions.CommandContext,
        user: interactions.Member,
        comment: str,
        background: str = "dark",
    ):
        """/tweet command."""
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
        url = "https://some-random-api.ml/canvas/tweet"
        params = {
            "avatar": user.user.avatar_url,
            "username": username,
            "displayname": nick,
            "comment": comment,
            "theme": background,
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @interactions.extension_command(
        name="youtube",
        description="Send a YouTube comment.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="comment",
                description="Comment",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def _youtube(
        self, ctx: interactions.CommandContext, user: interactions.Member, comment: str
    ):
        """Send a YouTube comment."""

        if len(user.user.username) >= 15:
            username = user.user.username[:12] + "..."
        else:
            username = user.user.username
        url = "https://some-random-api.ml/canvas/youtube-comment"
        params = {
            "avatar": user.user.avatar_url,
            "username": username,
            "comment": comment,
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @interactions.extension_command(
        name="amogus",
        description="Amogus.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            )
        ],
        dm_permission=False,
    )
    async def _amogus(
        self, ctx: interactions.CommandContext, user: interactions.Member
    ):
        """Amogus."""
        await ctx.defer()
        url = "https://some-random-api.ml/premium/amongus"
        params = {
            "avatar": user.user.avatar_url,
            "username": user.user.username,
            "key": apikey,
            "imposter": str(random.choice(["true", "false"])),
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.gif", fp=resp, description="Image")
        await ctx.send(files=img)

    @interactions.extension_command(
        name="pet",
        description="Pet someone.",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
        ],
        dm_permission=False,
    )
    async def _pet(self, ctx: interactions.CommandContext, user: interactions.Member):
        """Pet someone."""

        url = "https://some-random-api.ml/premium/petpet"
        params = {
            "avatar": user.user.avatar_url,
            "key": apikey,
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.gif", fp=resp, description="Image")
        await ctx.send(files=img)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Misc(client)
    logging.debug("""[%s] Loaded Misc extension.""", log_time)
