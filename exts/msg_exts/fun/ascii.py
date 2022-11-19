"""
Turn image into ASCII art.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import re
import string
import interactions
from interactions.ext import molter
import pyfiglet
import aiohttp
from PIL import Image, ImageDraw, ImageColor


def rgb2gray(rgb: str):
    """
    Return the gray color from RGB color.

    :param rbg: The RGB color string.
    :type rgb: str
    :return: The gray color.
    :rtype: int
    """
    try:
        r, g, b = rgb[0], rgb[1], rgb[2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    except TypeError:
        return 255


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

    words = [
        re.sub("^[{0}]+|[{0}]+$".format(string.punctuation), "", w)
        for w in text.split()
    ]
    pages = []
    s = ""
    for i in range(len(words)):
        if len(s) < 16:
            if i == len(words) - 1:
                s += f"{words[i]} "
                pages.append(s)
            else:
                s += f"{words[i]} "
        else:
            pages.append(s)
            s = ""
            if i == len(words) - 1:
                s += f"\n{words[i]} "
                pages.append(s)
            else:
                s += f"\n{words[i]} "
    return pages


class ASCII(molter.MolterExtension):
    """Extension for /ascii command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.ASCII_CHARS = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'´. "
        )

    @molter.prefixed_command(
        name="ascii",
    )
    async def _ascii(self, ctx: molter.MolterContext, text: str = None):
        ...

    @_ascii.subcommand(name="user")
    async def _ascii_image(self, ctx: interactions.CommandContext, param: str):
        """Turns a user profile picture into ASCII art."""

        # x = re.search("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?", url)

        # if not x:
        #     return await ctx.send("Invalid URL. (re)")
        user_obj = bool(re.match(r"<?([@!]|[@])(\d*)>", param))
        if user_obj is True:
            usr = re.compile("<?(\d*)>")
            parsed = usr.findall(param)
            try:
                url = await interactions.get(self.client, interactions.User, object_id=parsed[0])
                url = url.avatar_url[:-4] + ".png"
            except:
                return await ctx.send("Invalid param. Please check if it is a valid user.")
        elif param.isdigit() is True:
            try:
                url = await interactions.get(self.client, interactions.User, object_id=param)
                url = url.avatar_url[:-4] + ".png"
            except:
                return await ctx.send("Invalid param. Please check if it is a valid user.")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("Invalid URL. (status)")

                if resp.content_type not in {"image/png", "image/jpeg", "image/jpeg"}:
                    return await ctx.send(
                        "Invalid URL. (Supported format: png, jpeg, jpg)"
                    )

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

        # saves all pixels of img
        pix = img.load()

        # calc range of gray
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

        # goes through the pixels of the img
        for y in range(HEIGHT_LIMIT):
            row = ""

            for x in range(WIDTH_LIMIT):

                # calc the gray value of the pixel
                gray = rgb2gray(
                    pix[
                        x * (img.size[0] / WIDTH_LIMIT),
                        y * (img.size[1] / HEIGHT_LIMIT),
                    ]
                )

                letter = int(translate(gray, minG, maxG, 0, 69))

                # finds the matching ascii char
                row += self.ASCII_CHARS[letter]

            final += row + "\n"

        # print("("+str(WIDTH_LIMIT)+", "+str(HEIGHT_LIMIT)+")")
        # print(len(final))
        i = Image.new("RGB", (235, 290), color="black")
        I = ImageDraw.Draw(i)
        I.text((5, 5), final, fill=(34, 139, 34))
        with io.BytesIO() as out:
            i.save(out, format="JPEG")
            file = interactions.File(filename="image.jpg", fp=out.getvalue())

        await ctx.send(files=file)

    @_ascii.subcommand(name="text")
    async def _ascii_text(self, ctx: molter.MolterContext, *, text: str):
        """Turn texts into ASCII art word."""

        s = ""
        text_split = page_paginator(text)
        for t in text_split:
            s += t

        if len(text) > 1999:
            return await ctx.send("Text too long.")

        ascii_art = pyfiglet.figlet_format(s, width=600)

        width, height = 600, 90

        height *= len(text_split)

        img = Image.new("RGB", (width, height), color="black")
        i = ImageDraw.Draw(img)
        i.text(
            (1, 1),
            ascii_art,
            fill=(102, 255, 0)
        )
        with io.BytesIO() as out:
            img.save(out, format="JPEG")
            file = interactions.File(filename="image.jpg", fp=out.getvalue())
        await ctx.send(files=file)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    ASCII(client)
    logging.debug("""[%s] Loaded ASCII extension.""", log_time)
