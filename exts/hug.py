"""
This module is for hug command.

(C) 2022 - Jimmy-Blue
"""

import io
import interactions
from interactions import extension_command as command
import requests
from PIL import Image, ImageDraw, ImageOps


def _fixed_icon(user_id: str, user_avatar: str):
    """
    Return Image object from an icon link

    :param user_id: The user ID
    :type user_id: str
    :param user_avatar: The user icon hash
    :type user_avatar: str
    :param size: The size of the image (default to (102, 102) if None)
    :type size: tuple
    :return Image object
    :rtype Image
    """
    _user_avatar = f"https://cdn.discordapp.com/avatars/{str(user_id)}/{str(user_avatar)}.png"
    _resp = requests.get(_user_avatar)
    if _resp.status_code == 200:
        _icon = Image.open(io.BytesIO(_resp.content)).resize((102, 102))

        _mask = Image.new("L", _icon.size, 0)
        _draw = ImageDraw.Draw(_mask)
        _draw.ellipse((0, 0) + _icon.size, fill=255)

        _icon = ImageOps.fit(_icon, _mask.size, centering=(0, 0))
        _icon.putalpha(_mask)

        _icon_background = Image.new("RGBA", _icon.size, (255, 255, 255))
        icon = Image.alpha_composite(_icon_background, _icon)

        return icon


class Hug(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="hug",
        description="Hugs someone",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="User to hug",
                required=True
            )
        ],
        dm_permission=False
    )
    async def _hug(self, ctx: interactions.CommandContext, user: interactions.Member):
        _user_icon = _fixed_icon(user.user.id, user.user.avatar)
        _author_icon = _fixed_icon(ctx.author.id, ctx.author.avatar)

        mask = Image.new('L', _user_icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + _user_icon.size, fill=255)

        background = Image.open("./background.png")
        background.paste(_author_icon, (190, 90), mask=mask)
        background.paste(_user_icon, (285, 157), mask=mask)
        with io.BytesIO() as out:
            background.save(out, format="PNG")
            _io = out.getvalue()
            file = interactions.File(filename="image.png", fp=_io)
            await ctx.send(files=file)


def setup(bot):
    Hug(bot)
