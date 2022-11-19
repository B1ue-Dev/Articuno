"""
This module is for hug command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import interactions
from interactions.ext import molter
import aiohttp
from PIL import Image, ImageDraw, ImageOps


async def _fixed_icon(user_id: str, user_avatar: str):
    """
    Return Image object from an icon link.

    :param user_id: The user ID.
    :type user_id: str
    :param user_avatar: The user icon hash.
    :type user_avatar: str
    :return: Image object.
    :rtype: Image
    """
    _user_avatar = (
        f"https://cdn.discordapp.com/avatars/{str(user_id)}/{str(user_avatar)}.png"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(_user_avatar) as _resp:
            if _resp.status == 200:

                _icon = Image.open(io.BytesIO(await _resp.content.read())).resize(
                    (102, 102)
                )

                await session.close()

                _mask = Image.new("L", _icon.size, 0)
                _draw = ImageDraw.Draw(_mask)
                _draw.ellipse((0, 0) + _icon.size, fill=255)

                _icon = ImageOps.fit(_icon, _mask.size, centering=(0, 0))
                _icon.putalpha(_mask)

                _icon_background = Image.new("RGBA", _icon.size, (255, 255, 255))
                icon = Image.alpha_composite(_icon_background, _icon)

                return icon


class Hug(molter.MolterExtension):
    """Extension for /hug command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @molter.prefixed_command(name="hug")
    async def _hug(self, ctx: molter.MolterContext, user: interactions.Member):
        """Hugs a user."""

        if int(ctx.user.id) == int(user.id):
            return await ctx.send("You cannot hug yourself.")

        _user_icon = await _fixed_icon(user.user.id, user.user.avatar)
        _author_icon = await _fixed_icon(ctx.author.id, ctx.author.avatar)

        mask = Image.new("L", _user_icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + _user_icon.size, fill=255)

        background = Image.open("./img/hug.png")
        background.paste(_author_icon, (190, 90), mask=mask)
        background.paste(_user_icon, (285, 157), mask=mask)
        with io.BytesIO() as out:
            background.save(out, format="PNG")
            _io = out.getvalue()
            file = interactions.File(filename="image.png", fp=_io)
            await ctx.send(files=file)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Hug(client)
    logging.debug("""[%s] Loaded Hug extension.""", log_time)
