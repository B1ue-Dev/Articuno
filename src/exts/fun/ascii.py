"""
Turn image into ASCII art.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import textwrap
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
import pyfiglet
import aiohttp
from PIL import Image, ImageDraw


def rgb2gray(rgb: str) -> int:
    """
    Return the gray color from RGB color.

    :param rbg: The RGB color string.
    :type rgb: str
    :return: The gray color.
    :rtype: int
    """

    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def translate(value, leftMin, leftMax, rightMin, rightMax):
    """
    I have no idea what this works.
    """

    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)


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

        url = user.user.avatar.url[:-4] + ".png"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_bytes = io.BytesIO(await resp.read())
                img = Image.open(image_bytes)

        attempt = 100

        while True:
            WIDTH_LIMIT = attempt

            WIDTH_LIMIT = int(WIDTH_LIMIT / 2)
            HEIGHT_LIMIT = int((WIDTH_LIMIT * img.size[1]) / img.size[0])

            WIDTH_LIMIT *= 2

            attempt -= 0.5

            if WIDTH_LIMIT * HEIGHT_LIMIT + HEIGHT_LIMIT < 800:
                break

        pix = img.load()

        minG = 265
        maxG = 0

        for y in range(HEIGHT_LIMIT):
            for x in range(WIDTH_LIMIT):
                gray = rgb2gray(
                    pix[
                        x * (img.size[0] / WIDTH_LIMIT),
                        y * (img.size[1] / HEIGHT_LIMIT),
                    ]
                )

                if gray > maxG:
                    maxG = gray

                if gray < minG:
                    minG = gray

        final = ""

        for y in range(HEIGHT_LIMIT):
            row = ""

            for x in range(WIDTH_LIMIT):
                gray = rgb2gray(
                    pix[
                        x * (img.size[0] / WIDTH_LIMIT),
                        y * (img.size[1] / HEIGHT_LIMIT),
                    ]
                )

                letter = int(translate(gray, minG, maxG, 0, 69))

                row += self.ASCII_CHARS[letter]

            final += row + "\n"

        i = Image.new("RGB", (235, 290), color="black")
        z = ImageDraw.Draw(i)
        z.text((5, 5), final, fill=(34, 139, 34))
        with io.BytesIO() as out:
            i.save(out, "PNG")
            out.seek(0)
            file = interactions.File(file_name="image.jpg", file=out)

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
        text: str,
    ) -> None:
        """Turn texts into ASCII art word."""

        s = ""
        text_split = textwrap.wrap(
            text,
            width=45,
            break_long_words=True,
            break_on_hyphens=False,
            replace_whitespace=False,
        )
        for x, t in enumerate(text_split):
            if x != 0:
                s += "\n"
            s += t

        if len(text) > 1999:
            return await ctx.send("Text too long.")

        ascii_art = pyfiglet.figlet_format(s, width=1100)

        width, height = 1390, 90

        height *= len(text_split)

        img = Image.new("RGB", (width, height), color="black")
        i = ImageDraw.Draw(img)
        i.text((1, 1), ascii_art, fill=(102, 255, 0))
        with io.BytesIO() as out:
            img.save(out, format="JPEG")
            out.seek(0)
            file = interactions.File(file_name="image.jpg", file=out)
            await ctx.send(files=file)


def setup(client) -> None:
    """Setup the extension."""
    ASCII(client)
    logging.info("Loaded ASCII extension.")
