"""A program to convert images to ASCII art."""

from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from string import ascii_letters, digits, punctuation

CONVERSION_CHARACTERS = ascii_letters + digits + punctuation


def load_font(
    font_path: str, font_size: int
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(font_path, font_size)
    except OSError:
        # print(f"Load {font_path} font failed. Using default font.")
        return ImageFont.load_default(size=24)


base_font = load_font("src\\assets\\Mno16.ttf", 16)


def sizeof(
    text: str, font: ImageFont.FreeTypeFont = base_font
) -> tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    _, _, width, height = draw.textbbox((0, 0), text, font)
    return width, height


def ascii_to_image(
    text: str,
    font: ImageFont.FreeTypeFont = base_font,
    color: tuple = (0, 255, 255),
) -> Image.Image:
    text_image = Image.new("RGB", sizeof(text, font))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, color, font)
    return text_image


def get_brightness_of_char(
    char: str, font: ImageFont.FreeTypeFont = base_font
) -> int:
    image = ascii_to_image(char, font)
    return (np.array(image) != 0).sum().item()


def image_to_ascii(
    image: Image.Image | str,
    size: Optional[tuple[int, int]] = None,
    fix_scaling: bool = True,
    scale: float | tuple[float, float] = 1,
    sharpness: float = 1,
    brightness: float = 1,
) -> str:
    image = image.convert("RGB")
    charset = sorted(
        CONVERSION_CHARACTERS,
        key=lambda char: (get_brightness_of_char(char), char),
    )

    image_width, image_height = size or image.size

    if isinstance(scale, int | float):
        scale = (scale,) * 2
    image_width = int(image_width * scale[0] * (bool(fix_scaling) + 1))
    image_height = int(image_height * scale[1])

    scaled_image = image.resize((image_width, image_height))
    brightened_image = ImageEnhance.Brightness(scaled_image).enhance(
        brightness
    )
    sharpened_image = ImageEnhance.Sharpness(brightened_image).enhance(
        sharpness
    )
    image_array = (
        np.array(sharpened_image.convert("L"), dtype=int) * len(charset) // 256
    )
    ascii_converted = np.vectorize(charset.__getitem__)(image_array)

    output = "\n".join(map("".join, ascii_converted))

    return output
