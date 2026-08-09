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

    with Image.open(buf_user) as _img_u:
        _user_icon = _img_u.convert("RGBA").resize((102, 102))
    _mask_user = Image.new("L", _user_icon.size, 0)
    _draw_user = ImageDraw.Draw(_mask_user)
    _draw_user.ellipse((0, 0) + _user_icon.size, fill=255)
    _user_icon_fit = ImageOps.fit(_user_icon, _mask_user.size, centering=(0, 0))
    _user_icon_fit.putalpha(_mask_user)
    _user_bg = Image.new("RGBA", _user_icon_fit.size, (255, 255, 255))
    _user_icon_final = Image.alpha_composite(_user_bg, _user_icon_fit)

    with Image.open(buf_author) as _img_a:
        _author_icon = _img_a.convert("RGBA").resize((102, 102))
    _mask_author = Image.new("L", _author_icon.size, 0)
    _draw_author = ImageDraw.Draw(_mask_author)
    _draw_author.ellipse((0, 0) + _author_icon.size, fill=255)
    _author_icon_fit = ImageOps.fit(_author_icon, _mask_author.size, centering=(0, 0))
    _author_icon_fit.putalpha(_mask_author)
    _author_bg = Image.new("RGBA", _author_icon_fit.size, (255, 255, 255))
    _author_icon_final = Image.alpha_composite(_author_bg, _author_icon_fit)

    mask = Image.new("L", _user_icon_final.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + _user_icon_final.size, fill=255)

    with Image.open("./src/assets/hug.png") as _bg_img:
        background = _bg_img.convert("RGBA")
        
    background.paste(_author_icon_final, (190, 90), mask=mask)
    background.paste(_user_icon_final, (285, 157), mask=mask)

    out = io.BytesIO()
    background.save(out, format="PNG")
    out.seek(0)

    _user_icon.close()
    _mask_user.close()
    _user_icon_fit.close()
    _user_bg.close()
    _user_icon_final.close()
    
    _author_icon.close()
    _mask_author.close()
    _author_icon_fit.close()
    _author_bg.close()
    _author_icon_final.close()
    
    mask.close()
    background.close()

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
    )
    async def hug(self, ctx: HybridContext, user: interactions.Member) -> None:
        """Hugs a user."""

        if int(ctx.user.id) == int(user.id):
            return await ctx.send("You cannot hug yourself.", ephemeral=True)

        buf_user, buf_author = await asyncio.gather(
            get_response(user.display_avatar.url, self.client.session),
            get_response(ctx.author.display_avatar.url, self.client.session),
        )

        if not buf_user or not buf_author:
            return await ctx.send("Failed to download avatars from Discord!", ephemeral=True)

        out = await asyncio.to_thread(make_hug_image, buf_user, buf_author)

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
