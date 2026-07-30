"""
Hug command.

(C) 2022-2026 - B1ue-Dev
"""

import logging
import asyncio
import io
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from PIL import Image, ImageDraw, ImageOps

from src.common.utils import get_response


def make_hug_image(buf_user, buf_author):

    _user_icon = Image.open(buf_user).convert("RGBA").resize((102, 102))
    _mask_user = Image.new("L", _user_icon.size, 0)
    _draw_user = ImageDraw.Draw(_mask_user)
    _draw_user.ellipse((0, 0) + _user_icon.size, fill=255)
    _user_icon = ImageOps.fit(_user_icon, _mask_user.size, centering=(0, 0))
    _user_icon.putalpha(_mask_user)
    _user_bg = Image.new("RGBA", _user_icon.size, (255, 255, 255))
    _user_icon = Image.alpha_composite(_user_bg, _user_icon)

    _author_icon = Image.open(buf_author).convert("RGBA").resize((102, 102))
    _mask_author = Image.new("L", _author_icon.size, 0)
    _draw_author = ImageDraw.Draw(_mask_author)
    _draw_author.ellipse((0, 0) + _author_icon.size, fill=255)
    _author_icon = ImageOps.fit(_author_icon, _mask_author.size, centering=(0, 0))
    _author_icon.putalpha(_mask_author)
    _author_bg = Image.new("RGBA", _author_icon.size, (255, 255, 255))
    _author_icon = Image.alpha_composite(_author_bg, _author_icon)

    mask = Image.new("L", _user_icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + _user_icon.size, fill=255)

    background = Image.open("./src/assets/hug.png")
    background.paste(_author_icon, (190, 90), mask=mask)
    background.paste(_user_icon, (285, 157), mask=mask)

    out = io.BytesIO()
    background.save(out, format="PNG")
    out.seek(0)

    return out


class Hug(interactions.Extension):
    """Extension for /hug command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="hug",
        description="Hugs a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="The user you wish to hug",
                required=True,
            )
        ],
        dm_permission=False,
    )
    async def hug(self, ctx: HybridContext, user: interactions.Member) -> None:
        """Hugs a user."""

        if int(ctx.user.id) == int(user.id):
            return await ctx.send("You cannot hug yourself.", ephemeral=True)

        _user_icon = await fixed_icon(user.user.id, user.user.avatar.hash)
        _author_icon = await fixed_icon(ctx.author.id, ctx.author.avatar.hash)

        mask = Image.new("L", _user_icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + _user_icon.size, fill=255)

        background = Image.open("./src/assets/hug.png")
        background.paste(_author_icon, (190, 90), mask=mask)
        background.paste(_user_icon, (285, 157), mask=mask)
        with io.BytesIO() as out:
            background.save(out, format="PNG")
            out.seek(0)
            file = interactions.File(
                file_name="image.png",
                file=out,
                description=f"{ctx.user.username} hugs {user.username}",
            )

            await ctx.send(
                content=(
                    "Hey, thanks for the hug. ^_^"
                    if int(user.id) == int(self.client.user.id)
                    else None
                ),
                files=file,
            )


def setup(client) -> None:
    """Setup the extension."""
    Hug(client)
    logging.info("Loaded Hug extension.")
