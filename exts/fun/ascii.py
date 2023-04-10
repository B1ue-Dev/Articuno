"""
Turn image into ASCII art.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import datetime
import io
import re
import textwrap
import interactions
import pyfiglet
import aiohttp
from PIL import Image, ImageDraw, ImageColor


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

    @interactions.slash_command(
        name="ascii",
        description="ASCII art command.",
    )
    async def ascii(self, *args, **kwargs) -> None:
        """For everything related to /ascii command."""
        ...

    @ascii.subcommand(
        sub_cmd_name="user",
        sub_cmd_description="Turns a user profile picture into ASCII text art.",
    )
    @interactions.slash_option(
        name="user",
        description="Target user",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    async def user(
        self,
        ctx: interactions.InteractionContext,
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
        I = ImageDraw.Draw(i)
        I.text((5, 5), final, fill=(34, 139, 34))
        with io.BytesIO() as out:
            i.save(out, "PNG")
            out.seek(0)
            file = interactions.File(file_name="image.jpg", file=out)

            await ctx.send(files=file)

    @ascii.subcommand(
        sub_cmd_name="text",
        sub_cmd_description="Turn texts into ASCII art word.",
    )
    @interactions.slash_option(
        name="text",
        description="The text you want to convert",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="color",
        description="The color of the text (hex code)",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def text(
        self,
        ctx: interactions.InteractionContext,
        text: str,
        color: str = None,
    ) -> None:
        """Turn texts into ASCII art word."""

        custom_color = None
        if color is None:
            pass
        else:
            match = re.search(r"^(?:[0-9a-fA-F]{3}){1,2}$", color)
            if not match:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid hex code. Please try again.\n",
                            "In case you do not know about hex code, have a look at the [gif](https://cdn.discordapp.com/attachments/862636687226044436/1014917397519552703/guide.gif) ",
                            "below and use [this site](<https://www.w3schools.com/colors/colors_picker.asp>) ",
                            "to get the color hex code.",
                        ]
                    ),
                    ephemeral=True,
                )
            custom_color = ImageColor.getcolor(
                color if color.startswith("#") else "#" + color, "RGB"
            )

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
        i.text(
            (1, 1),
            ascii_art,
            fill=(102, 255, 0)
            if color is None
            else (custom_color[0], custom_color[1], custom_color[2]),
        )
        with io.BytesIO() as out:
            img.save(out, format="JPEG")
            out.seek(0)
            file = interactions.File(file_name="image.jpg", file=out)
            await ctx.send(files=file)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    ASCII(client)
    logging.debug("""[%s] Loaded ASCII extension.""", log_time)
