"""
Petpet command.

(C) 2023 - B1ue-Dev
"""

import logging
from io import BytesIO
from PIL import Image
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response


class Petpet(interactions.Extension):
    """Extension for petpet commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
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
    )
    async def pet(self, ctx: HybridContext, user: interactions.Member) -> None:
        """Pet someone."""

        await ctx.defer()

        _hash: str = ""
        if isinstance(user, interactions.User):
            _hash = user.avatar.hash
        elif isinstance(user, interactions.Member):
            _hash = (
                user.avatar.hash
                if user.guild_avatar is None
                else user.guild_avatar.hash
            )

        if _hash.isdigit():
            _url: str = f"https://cdn.discordapp.com/embed/avatars/{_hash}.png"
        else:
            _url: str = (
                f"https://cdn.discordapp.com/avatars/{str(user.user.id)}/{_hash}.png"
            )

        member_avatar = Image.open(await get_response(_url)).convert("RGBA")
        member_avatar = member_avatar.resize(
            (75, 75), Image.Resampling.LANCZOS
        )
        # base canvas
        sprite = Image.open("./src/img/sprite.png", mode="r").convert("RGBA")

        # pasting the pfp
        images = []
        resolution = (100, 100)
        for i in range(5):
            squeeze = i if i < 5 / 2 else 5 - i
            width = 0.8 + squeeze * 0.02
            height = 0.8 - squeeze * 0.05
            offsetX = (1 - width) * 0.5 + 0.1
            offsetY = (1 - height) - 0.08
            im = Image.new("RGBA", (100, 100), None)
            im.paste(
                member_avatar.resize(
                    (
                        round(width * resolution[0]),
                        round(height * resolution[1]),
                    )
                ),
                (
                    round(offsetX * resolution[0]),
                    round(offsetY * resolution[1]),
                ),
            )
            im.paste(sprite, (0 - (112 * i), 0), sprite)
            images.append(im)
        sprite.close()
        member_avatar.close()

        fp = BytesIO()
        images[0].save(
            fp,
            "GIF",
            save_all=True,
            append_images=images[1:],
            loop=0,
            disposal=2,
        )
        fp.seek(0)
        for im in images:
            im.close()
        _file = interactions.File(file=fp, file_name="petpet.gif")

        if int(user.id) == int(self.client.user.id):
            return await ctx.send(
                file=_file, content="Aww, thanks for the pet. ^^"
            )

        await ctx.send(file=_file)


def setup(client) -> None:
    """Setup the extension."""
    Petpet(client)
    logging.info("Loaded Petpet extension.")
