"""
Turn image into ASCII art.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io

import interactions
from interactions import Message
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
import pyfiglet
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from src.utils.ascii import (
    image_to_ascii,
    ascii_to_image,
    base_font,
    sizeof as ascii_sizeof,
)


class ASCII(interactions.Extension):
    """Extension for /ascii command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

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
    @interactions.slash_option(
        name="color",
        description="Choose a predefined color",
        opt_type=interactions.OptionType.STRING,
        required=False,
        choices=[
            {"name": "red", "value": "255,0,0"},
            {"name": "blue", "value": "0,0,255"},
            {"name": "green", "value": "0,255,0"},
            {"name": "yellow", "value": "255,255,0"},
            {"name": "cyan", "value": "0,255,255"},
            {"name": "magenta", "value": "255,0,255"},
            {"name": "white", "value": "255,255,255"},
        ],
    )
    @interactions.slash_option(
        name="size",
        description="Custom size for the result. Bigger size results in longer render time",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    @interactions.slash_option(
        name="sharpness",
        description="Custom sharpness for the result. Integer to increase (5) and float to decrease (0.2)",
        opt_type=interactions.OptionType.NUMBER,
        required=False,
    )
    @interactions.slash_option(
        name="brightness",
        description="Custom brightness for the result. Integer to increase (5) and float to decrease (0.2)",
        opt_type=interactions.OptionType.NUMBER,
        required=False,
    )
    @interactions.slash_option(
        name="text_file",
        description="Select this if you want to have the text file",
        opt_type=interactions.OptionType.BOOLEAN,
        required=False,
    )
    @interactions.slash_option(
        name="font",
        description="Custom font used for the render. It should be a monospaced font",
        opt_type=interactions.OptionType.ATTACHMENT,
        required=False,
    )
    @interactions.slash_option(
        name="font_size",
        description="The size of the custom font. Only use if you have a custom font",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
    )
    async def user(
        self,
        ctx: HybridContext,
        user: interactions.Member,
        text_file: bool = False,
        font: interactions.Attachment = None,
        font_size: int = None,
        color: str = "0,255,255",
        size: int = 124,
        sharpness: float = 1,
        brightness: float = 1,
    ) -> Message | None:
        """Turns a user profile picture into ASCII art."""
        await ctx.defer()

        if font and not font_size or font_size and not font:
            return await ctx.send(
                "You are using custom font/size. Please specify both of them.",
                ephemeral=True,
            )

        url = user.user.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_bytes = io.BytesIO(await resp.read())
                img = Image.open(image_bytes)

        font_stream = None
        if font:
            async with aiohttp.ClientSession() as session:
                async with session.get(font.url) as response:
                    if response.status == 200:
                        font_data = await response.read()
                        font_stream = io.BytesIO(font_data)
                    else:
                        return await ctx.send(
                            "Failed to get the font.", ephemeral=True
                        )

        ascii_art_txt = image_to_ascii(
            img, size=(size, size), sharpness=sharpness, brightness=brightness
        )
        rgb_tuple = tuple(map(int, color.split(",")))
        if font and font_stream:
            try:
                custom_font = ImageFont.truetype(font_stream, font_size)
            except Exception:
                return await ctx.send(
                    "This doesn't seem to be a valid font size. Please try again.",
                    ephemeral=True,
                )
            ascii_art_png = ascii_to_image(
                ascii_art_txt, custom_font, color=rgb_tuple
            )
        else:
            ascii_art_png = ascii_to_image(ascii_art_txt, color=rgb_tuple)

        send_file = []

        if text_file:
            text_bytes = io.BytesIO()
            text_bytes.write(
                ascii_art_txt.encode("utf-8")
            )  # Encode text to bytes
            text_bytes.seek(0)
            txt_file = interactions.File(
                file_name="ascii.txt", file=text_bytes
            )
            send_file.append(txt_file)

        img_buffer = io.BytesIO()
        ascii_art_png.save(img_buffer, "PNG")
        img_buffer.seek(0)
        img_file = interactions.File(file_name="image.png", file=img_buffer)
        send_file.append(img_file)

        await ctx.send(files=send_file)
        return None

    @interactions.subcommand(
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
    @interactions.slash_option(
        name="color",
        description="Choose a predefined color",
        opt_type=interactions.OptionType.STRING,
        required=False,
        choices=[
            {"name": "red", "value": "255,0,0"},
            {"name": "blue", "value": "0,0,255"},
            {"name": "green", "value": "0,255,0"},
            {"name": "yellow", "value": "255,255,0"},
            {"name": "cyan", "value": "0,255,255"},
            {"name": "magenta", "value": "255,0,255"},
            {"name": "white", "value": "255,255,255"},
        ],
    )
    async def text(
        self,
        ctx: interactions.SlashContext,
        color: str = "0,255,255",
        text: str = None,
    ) -> None:
        """Turn texts into ASCII art word."""

        await ctx.defer()

        ascii_text = pyfiglet.figlet_format(text, width=150)
        i = Image.new("RGB", ascii_sizeof(ascii_text, base_font))
        img = ImageDraw.Draw(i)
        size = img.textbbox((0, 0), ascii_text, font=base_font)
        text_width, text_height = (size[2] - size[0], size[3] - size[1])
        imgs = Image.new("RGB", (int(text_width), int(text_height)))
        ii = ImageDraw.Draw(imgs)
        ii.text(
            (0, 0),
            ascii_text,
            fill=tuple(map(int, color.split(","))),
            font=base_font,
        )
        final = io.BytesIO()
        imgs.save(final, "png")
        final.seek(0)
        file = interactions.File(file=final, file_name="unknown.png")
        await ctx.send(file=file)


def setup(client) -> None:
    """Set up the extension."""
    ASCII(client)
    logging.info("Loaded ASCII extension.")
