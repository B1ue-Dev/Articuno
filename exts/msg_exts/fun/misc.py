"""
This module is for misc commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import random
import interactions
from interactions.ext import molter
from utils.utils import get_response
from const import APIKEY as apikey


class Misc(molter.MolterExtension):
    """Extension for misc commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @molter.prefixed_command(name="hornycard")
    async def _hornycard(
        self, ctx: molter.MolterContext, user: interactions.Member = None
    ):
        """Sends a hornycard."""

        if user is None:
            user = ctx.member

        avatar_url = user.user.avatar_url
        url = "https://some-random-api.ml/canvas/horny"
        params = {
            "avatar": avatar_url,
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @molter.prefixed_command(name="simpcard")
    async def _simpcard(
        self, ctx: molter.MolterContext, user: interactions.Member = None
    ):
        """Sends a simpcard."""

        if user is None:
            user = ctx.member

        avatar_url = user.user.avatar_url
        url = "https://some-random-api.ml/canvas/simpcard"
        params = {"avatar": avatar_url}
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @molter.prefixed_command(name="tweet")
    async def _tweet(
        self,
        ctx: molter.MolterContext,
        user: interactions.Member,
        *,
        comment: str,
    ):
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
        url = "https://some-random-api.ml/canvas/tweet"
        params = {
            "avatar": user.user.avatar_url,
            "username": username,
            "displayname": nick,
            "comment": comment,
            "theme": "dark",
        }
        resp = await get_response(url, params)
        img = interactions.File(filename="image.png", fp=resp, description="Image")
        await ctx.send(files=img)

    @molter.prefixed_command(name="youtube")
    async def _youtube(
        self, ctx: molter.MolterContext, user: interactions.Member, *, comment: str
    ):
        """Sends a YouTube comment."""

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

    @molter.prefixed_command(name="amogus")
    async def _amogus(
        self, ctx: molter.MolterContext, user: interactions.Member
    ):
        """Amogus."""

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

    @molter.prefixed_command(name="pet")
    async def _pet(self, ctx: molter.MolterContext, user: interactions.Member):
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
