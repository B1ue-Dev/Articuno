"""
Hug command.

(C) 2022-2023 - B1ue-Dev
"""

import io
import interactions
import aiohttp
from PIL import Image, ImageDraw, ImageOps


async def fixed_icon(user_id: str, user_avatar: str):
    """
    Return Image object from an icon link.

    :param user_id: The user ID.
    :type user_id: str
    :param user_avatar: The user icon hash.
    :type user_avatar: str
    :return: Image object.
    :rtype: Image
    """
    user_avatar = f"https://cdn.discordapp.com/avatars/{str(user_id)}/{str(user_avatar)}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(user_avatar) as _resp:
            if _resp.status == 200:
                _icon = Image.open(
                    io.BytesIO(await _resp.content.read())
                ).resize((102, 102))

                await session.close()

                _mask = Image.new("L", _icon.size, 0)
                _draw = ImageDraw.Draw(_mask)
                _draw.ellipse((0, 0) + _icon.size, fill=255)

                _icon = ImageOps.fit(_icon, _mask.size, centering=(0, 0))
                _icon.putalpha(_mask)

                _icon_background = Image.new(
                    "RGBA", _icon.size, (255, 255, 255)
                )
                icon = Image.alpha_composite(_icon_background, _icon)

                return icon


class Hug(interactions.Extension):
    """Extension for /hug command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
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
    async def hug(
        self, ctx: interactions.SlashContext, user: interactions.Member
    ) -> None:
        """Hugs a user."""

        if int(ctx.user.id) == int(user.id):
            return await ctx.send("You cannot hug yourself.", ephemeral=True)

        _user_icon = await fixed_icon(user.user.id, user.user.avatar.hash)
        _author_icon = await fixed_icon(ctx.author.id, ctx.author.avatar.hash)

        mask = Image.new("L", _user_icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + _user_icon.size, fill=255)

        background = Image.open("./img/hug.png")
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
            print(int(ctx.user.id) == int(self.client.user.id))
            await ctx.send(
                content="Hey, thanks for the hug. ^_^"
                if int(user.id) == int(self.client.user.id)
                else None,
                files=file,
            )
