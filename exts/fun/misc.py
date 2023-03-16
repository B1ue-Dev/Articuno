"""
Miscellaneous commands.

(C) 2022-2023 - B1ue-Dev
"""

import random
import interactions
from utils.utils import get_response
from const import APIKEY as apikey


class Misc(interactions.Extension):
    """Extension for misc commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="hornycard",
        description="Sends a hornycard.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=False,
            )
        ],
    )
    async def hornycard(
        self,
        ctx: interactions.SlashContext,
        user: interactions.Member = None,
    ) -> None:
        """Sends a hornycard."""

        if user is None:
            user = ctx.member

        avatar_url = (
            user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url
        )
        url = "https://some-random-api.ml/canvas/horny"
        params = {
            "avatar": avatar_url,
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
            description=f"{user.username} hornycard.",
        )
        await ctx.send(file=img)

    @interactions.slash_command(
        name="simpcard",
        description="Sends a simpcard.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=False,
            )
        ],
    )
    async def simpcard(
        self,
        ctx: interactions.SlashContext,
        user: interactions.Member = None,
    ) -> None:
        """Sends a simpcard."""

        if user is None:
            user = ctx.member

        avatar_url = (
            user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url
        )
        url = "https://some-random-api.ml/canvas/simpcard"
        params = {"avatar": avatar_url}
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
            description=f"{user.username} simpcard.",
        )
        await ctx.send(file=img)

    @interactions.slash_command(
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
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="background",
                description="Background of the Tweet",
                required=False,
                choices=[
                    interactions.SlashCommandChoice(
                        name="Light", value="light"
                    ),
                    interactions.SlashCommandChoice(
                        name="Dim", value="dim"
                    ),
                    interactions.SlashCommandChoice(
                        name="Dark", value="dark"
                    ),
                ],
            ),
        ],
        dm_permission=False,
    )
    async def tweet(
        self,
        ctx: interactions.SlashContext,
        user: interactions.Member,
        comment: str,
        background: str = "dark",
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
        url = "https://some-random-api.ml/canvas/tweet"
        params = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "username": username,
            "displayname": nick,
            "comment": comment,
            "theme": background,
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.png",
            file=resp,
            description=f"{user.username} tweet.",
        )
        await ctx.send(file=img)

    @interactions.slash_command(
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
        ctx: interactions.SlashContext,
        user: interactions.Member,
        comment: str,
    ) -> None:
        """Sends a YouTube comment."""

        if len(user.user.username) >= 15:
            username = user.user.username[:12] + "..."
        else:
            username = user.user.username
        url = "https://some-random-api.ml/canvas/youtube-comment"
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

    @interactions.slash_command(
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
        self, ctx: interactions.SlashContext, user: interactions.Member
    ) -> None:
        """Amogus."""

        await ctx.defer()
        url = "https://some-random-api.ml/premium/amongus"
        params = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "username": user.user.username,
            "key": apikey,
            "imposter": str(random.choice(["true", "false"])),
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.gif",
            file=resp,
            description="Amogus.",
        )
        await ctx.send(file=img)

    @interactions.slash_command(
        name="pet",
        description="Pet someone.",
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
    async def pet(
        self, ctx: interactions.SlashContext, user: interactions.Member
    ) -> None:
        """Pet someone."""

        url = "https://some-random-api.ml/premium/petpet"
        params = {
            "avatar": user.avatar.url
            if user.guild_avatar is None
            else user.guild_avatar.url,
            "key": apikey,
        }
        resp = await get_response(url, params)
        img = interactions.File(
            file_name="image.gif",
            file=resp,
            description="PetPet",
        )
        await ctx.send(file=img)
