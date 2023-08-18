"""
Turn image into ASCII art.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
import pyfiglet
import aiohttp
from PIL import Image, ImageDraw


class ASCII(interactions.Extension):
    """Extension for /ascii command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'´. "

    @hybrid_slash_subcommand(
        base="ascii",
        base_description="ASCII art command.",
        name="user",
        description="Turns a user profile picture into ASCII text art.",
    )
    @interactions.slash_option(
        name="user",
        description="Target user",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    async def user(
        self,
        ctx: HybridContext,
        user: interactions.Member,
    ) -> None:
        """Turns a user profile picture into ASCII art."""
        await ctx.defer()

        def translate(value, leftMin, leftMax, rightMin, rightMax):
            leftSpan = leftMax - leftMin
            rightSpan = rightMax - rightMin
            valueScaled = float(value - leftMin) / float(leftSpan)
            return rightMin + (valueScaled * rightSpan)

        url = user.user.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_bytes = io.BytesIO(await resp.read())
                img = Image.open(image_bytes)
                img = img.convert("L")

        WIDTH_LIMIT = 169
        HEIGHT_LIMIT = 68
        img = img.resize((WIDTH_LIMIT, HEIGHT_LIMIT))

        pix = img.load()
        minG = 265
        maxG = 0
        for y in range(HEIGHT_LIMIT):
            for x in range(WIDTH_LIMIT):
                gray = pix[x, y]
                if gray > maxG:
                    maxG = gray
                if gray < minG:
                    minG = gray

        final = ""
        for y in range(HEIGHT_LIMIT):
            row = ""
            for x in range(WIDTH_LIMIT):
                gray = pix[x, y]
                letter = int(translate(gray, minG, maxG, 0, 69))
                row += self.ASCII_CHARS[letter]
            final += row + "\n"

        i = Image.new("RGB", (1024, 1024), color="black")
        z = ImageDraw.Draw(i)
        z.text((5, 5), final, fill=(34, 139, 34))
        with io.BytesIO() as out:
            i.save(out, "PNG")
            out.seek(0)
            file = interactions.File(file_name="image.png", file=out)

            await ctx.send(files=file)

    @hybrid_slash_subcommand(
        base="ascii",
        base_description="ASCII art command.",
        name="text",
        description="Turn texts into ASCII art word.",
    )
    @interactions.slash_option(
        name="text",
        description="The text you want to convert",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def text(
        self,
        ctx: HybridContext,
        *,
        text: interactions.ConsumeRest[str],
    ) -> None:
        """Turn texts into ASCII art word."""

        await ctx.defer()

        i = Image.new("RGB", (2000, 1000))
        img = ImageDraw.Draw(i)
        ascii_text = pyfiglet.figlet_format(text, width=150)
        print(ascii_text)
        size = img.textbbox((1, 1), ascii_text)
        text_width, text_height = (size[2] - size[0], size[3] - size[1])
        imgs = Image.new("RGB", (text_width + 30, text_height))
        ii = ImageDraw.Draw(imgs)
        ii.text((5, 5), ascii_text, fill=(0, 255, 0))
        final = io.BytesIO()
        imgs.save(final, "png")
        final.seek(0)
        file = interactions.File(file=final, file_name="unknown.png")
        await ctx.send(file=file)


def setup(client) -> None:
    """Setup the extension."""
    ASCII(client)
    logging.info("Loaded ASCII extension.")
