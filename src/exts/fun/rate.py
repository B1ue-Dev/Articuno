"""
Rate related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import re
import random
import time
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response


def get_user_id(string: str) -> str | None:
    """Gets the id from a user object string."""

    regex = r"<@!?(\d+)>"
    match = re.match(regex, string)
    if match:
        return match.group(1)
    else:
        return None


class Rate(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.user_regex = r"<@!?(\d+)>"

    @hybrid_slash_command(
        name="gay",
        description="Calculate the gay percentage of a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False,
            ),
        ],
    )
    async def gay(self, ctx: HybridContext, user: str = None) -> None:
        """Calculates the gay percentage of a user."""

        if not user:
            user = ctx.user.username
            random.seed(str(ctx.user.id) + str(int(time.time() / 300)))
        else:
            _user = get_user_id(user)
            if _user:
                random.seed(str(_user) + str(int(time.time() / 300)))
        perc: int = random.choice(range(0, 100))

        if perc > 80:
            _user = get_user_id(user)
            if _user:
                user = ctx.guild.get_member(_user)
                url: str = "https://api.some-random-api.com/canvas/overlay/gay"
                params: dict = {
                    "avatar": (
                        user.avatar.url
                        if user.guild_avatar is None
                        else user.guild_avatar.url
                    ),
                }
                resp: dict = await get_response(url, params)

                img = interactions.File(
                    file_name="image.png",
                    file=resp,
                )

                embed = interactions.Embed(
                    title="Gay measure tool",
                    description=f"**{user}** is {perc}% gay today.",
                    color=random.randint(0, 0xFFFFFF),
                )

                return await ctx.send(embeds=embed, file=img)

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay today.",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="clownrate",
        description="Reveal someone's clownery.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False,
            ),
        ],
        aliases=["clown"],
    )
    async def clownrate(self, ctx: HybridContext, user: str = None) -> None:
        """Reveal someone's clownery."""

        if not user:
            user = ctx.user.username
            random.seed(str(ctx.user.id) + str(int(time.time() / 300)))
        else:
            _user = get_user_id(user)
            if _user:
                random.seed(str(_user) + str(int(time.time() / 300)))
        perc: int = random.choice(range(0, 100))

        embed = interactions.Embed(
            title="Clown rate tool",
            description=f"**{user}** is {perc}% clown today. 🤡",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="sanitycheck",
        description="Calculate the sanity percentage of a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False,
            ),
        ],
        aliases=["sanity"],
    )
    async def sanitycheck(self, ctx: HybridContext, user: str = None) -> None:
        """Calculates the gay percentage of a user."""

        if not user:
            user = ctx.user.username
            random.seed(
                str(ctx.user.id)
                + str(int(time.time() / 300))
                + str(self.client.user.id)
            )
        else:
            _user = get_user_id(user)
            if _user:
                random.seed(
                    str(_user)
                    + str(int(time.time() / 300))
                    + str(self.client.user.id)
                )

        perc = int(random.randint(0, 100))

        embed = interactions.Embed(
            title="Sanity check tool",
            description=f"**{user}** is {perc}% sane today.",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    Rate(client)
    logging.info("Loaded Rate extension.")
