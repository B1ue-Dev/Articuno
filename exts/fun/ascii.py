"""
Turn image into ASCII art.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import json
import re
import interactions
import pyfiglet
import aiohttp
from PIL import Image


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
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def page_paginator(text: str) -> list[str]:
    """
    This function takes a string and splits it into chunks of 10 characters.

    :param text: The string to split.
    :type text: str
    :return: A list of strings.
    :rtype: list
    """

    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % 10 == 0:
            pages.append(text[last:curr] + "\n")
            last = curr
            appd_index = curr
    if appd_index != len(text)-1:
        pages.append(text[last:curr] + "\n")
    return list(filter(lambda a: a != '\n', pages))


class ASCII(interactions.Extension):
    """Extension for /ascii command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'´. "

    @interactions.extension_command(
        name="ascii",
        description="ASCII art command.",
    )
    async def _ascii(self, *args, **kwargs):
        ...

    @_ascii.subcommand(name="image")
    @interactions.option("Target user")
    @interactions.option("The URL of the image")
    async def _ascii_image(
        self,
        ctx: interactions.CommandContext,
        user: interactions.Member = None,
        url: str = None,
    ):
        """Turn an image into ASCII art."""

        if user is not None and url is not None:
            return await ctx.send("You can only choose between `user` or `url`.", ephemeral=True)
        elif user is None and url is None:
            return await ctx.send("Please choose 1 argument.", ephemeral=True)

        if user is None:
            pass
        elif url is None:
            url = user.user.avatar_url[:-4] + ".png"

        x = re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|png)", url)

        if not x:
            return await ctx.send("Invalid URL. (re)")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("Invalid URL. (status)")

                if resp.content_type not in {"image/png", "image/jpeg", "image/jpeg"}:
                    return await ctx.send("Invalid URL. (type)")

                image_bytes = io.BytesIO(await resp.read())
                img = Image.open(image_bytes)

        attempt = 100

        while True:
            WIDTH_LIMIT = attempt

            WIDTH_LIMIT = int(WIDTH_LIMIT/2)
            HEIGHT_LIMIT = int((WIDTH_LIMIT * img.size[1]) / img.size[0])

            WIDTH_LIMIT *= 2

            attempt -= 0.5

            if(WIDTH_LIMIT*HEIGHT_LIMIT+HEIGHT_LIMIT < 1000):
                break

        # saves all pixels of img
        pix = img.load()

        # calc range of gray
        minG = 265
        maxG = 0

        for y in range(HEIGHT_LIMIT):

            for x in range(WIDTH_LIMIT):

                gray = rgb2gray( pix[x*(img.size[0]/WIDTH_LIMIT), y*(img.size[1]/HEIGHT_LIMIT)] )

                if (gray > maxG):
                    maxG = gray

                if (gray < minG):
                    minG = gray

        final = ""

        # goes through the pixels of the img
        for y in range(HEIGHT_LIMIT):
            row = ""

            for x in range(WIDTH_LIMIT):

                # calc the gray value of the pixel
                gray = rgb2gray( pix[x*(img.size[0]/WIDTH_LIMIT), y*(img.size[1]/HEIGHT_LIMIT)] )

                letter = int(translate(gray, minG, maxG, 0, 69))

                # finds the matching ascii char
                row += self.ASCII_CHARS[letter]

            final += row+"\n"

        # print("("+str(WIDTH_LIMIT)+", "+str(HEIGHT_LIMIT)+")")
        # print(len(final))

        await ctx.send(
            content=f"```\n{final}\n```"
        )

    @_ascii.subcommand(name="text")
    @interactions.option("The text you want to convert")
    async def _ascii_text(self, ctx: interactions.CommandContext, text: str):
        """Turn texts into ASCII art word."""

        await ctx.defer()
        if len(text) > 100:
            return await ctx.send("Text too long.", ephemeral=True)
        if len(text) < 16:
            ascii_art = pyfiglet.figlet_format(text)
            return await ctx.send(f"```\n{ascii_art}```")

        s = ""
        text_split = page_paginator(text)
        for t in text_split:
            s += t

        if len(text) > 1999:
            return await ctx.send("Text too long.")

        ascii_art = pyfiglet.figlet_format(s)
        await ctx.send(f"```\n{ascii_art}```")


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    ASCII(client)
    logging.debug("""[%s] Loaded ASCII extension.""", log_time)
    print(f"[{log_time}] Loaded ASCII extension.")
