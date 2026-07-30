"""
Rate related commands.

(C) 2022-2026 - B1ue-Dev
"""

import asyncio
import logging
import re
import random
import time
from io import BytesIO
from PIL import Image
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.common.utils import get_response


def lerp_color(color1, color2, factor):

    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))


def overlay_gay(buf) -> BytesIO:

    img = Image.open(buf).convert("RGBA")
    w, h = img.size

    colors = [
        (228, 3, 3),    # Red
        (255, 140, 0),  # Orange
        (255, 237, 0),  # Yellow
        (0, 128, 38),   # Green
        (0, 76, 255),   # Blue
        (115, 41, 130)  # Violet
    ]

    gradient_1d = Image.new("RGBA", (1, h))
    pixels = gradient_1d.load()

    alpha_value = int(255 * 0.35)
    num_segments = len(colors) - 1

    for y in range(h):
        relative_y = y / (h - 1) if h > 1 else 0

        segment = relative_y * num_segments
        index = int(segment)

        if index >= num_segments:
            current_color = colors[-1]
        else:
            local_factor = segment - index
            current_color = lerp_color(colors[index], colors[index + 1], local_factor)

        pixels[0, y] = current_color + (alpha_value, )

    gradient_overlay = gradient_1d.resize((w, h))
    final_img = Image.alpha_composite(img, gradient_overlay)

    fp = BytesIO()
    final_img.convert("RGB").save(fp, format="PNG")
    fp.seek(0)

    return fp


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

        img: interactions.File | None  = None
        perc: int = random.choice(range(0, 100))

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay today.",
            color=random.randint(0, 0xFFFFFF),
        )

        if perc > 80:
            _user = get_user_id(user)
            if _user:
                await ctx.defer()
                try:
                    user = ctx.guild.get_member(_user)
                except:
                    user = await ctx.client.fetch_user(_user)

                user_avatar = await get_response(user.display_avatar.url, self.client.session)
                if not user_avatar:
                    return await ctx.send(embed=embed)
                res = await asyncio.to_thread(overlay_gay, user_avatar)

                img = interactions.File(
                    file_name="image.png",
                    file=res,
                )
        if img:
            embed.set_image("attachment://image.png")
        await ctx.send(embed=embed, file=img)

        from src.common.utils import send_promote

        await send_promote(ctx, "easy")

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
        from src.common.utils import send_promote

        await send_promote(ctx, "easy")

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
        from src.common.utils import send_promote

        await send_promote(ctx, "easy")


def setup(client) -> None:
    """Setup the extension."""
    Rate(client)
    logging.info("Loaded Rate extension.")
