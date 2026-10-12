"""
/amogus command.

(C) 2025-2026 - B1ue-Dev
"""

import asyncio
import ctypes
import gc
import logging
import random
import sys
from io import BytesIO

import interactions
from interactions.ext.hybrid_commands import (
    HybridContext,
    hybrid_slash_command,
)
from PIL import Image, ImageDraw, ImageFont

from src.common.utils import get_response

WIDTH, HEIGHT = 800, 450
FRAMES = 95
STAR_COUNT = 80


def _trim_memory() -> None:

    gc.collect()
    if not sys.platform.startswith("linux"):
        return

    try:
        malloc_trim = ctypes.CDLL(None).malloc_trim
    except (AttributeError, OSError):
        return

    malloc_trim.argtypes = [ctypes.c_size_t]
    malloc_trim.restype = ctypes.c_int
    malloc_trim(0)


def random_stars():
    return [
        (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        for _ in range(STAR_COUNT)
    ]


def draw_frame(crewmate_img, stars, text, crewmate_x):
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)
    # Draw stars
    for x, y in stars:
        draw.ellipse((x, y, x + 3, y + 3), fill="white")
    # Draw text
    font = ImageFont.load_default(size=32)
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((WIDTH - w) // 2, (HEIGHT - h) // 2), text, font=font, fill="white"
    )
    # Draw crewmate
    img.paste(
        crewmate_img,
        (int(crewmate_x), HEIGHT // 2 - crewmate_img.height // 2),
        crewmate_img,
    )
    return img


def make_gif(username, impostor, buf):
    with Image.open(buf) as _member_avatar:
        member_avatar = _member_avatar.convert("RGBA")
    crewmate_img_orig = member_avatar.resize((128, 128), Image.LANCZOS)
    member_avatar.close()

    text = (
        f"{username} was {'The Impostor' if impostor else 'Not The Impostor'}"
    )
    original_stars = random_stars()
    frame_duration = 40
    typing_frames = max(1, int(len(text) * 2.0))
    delay_frames = int(0.5 * 1000 / frame_duration)

    start_x = -crewmate_img_orig.width * 4
    end_x = WIDTH + crewmate_img_orig.width * 2

    # Calculate the frame where the crewmate's center reaches 3/4 of the visible width
    # visible_target_x = int(WIDTH * 0.75)
    # total_path = end_x - start_x
    # target_progress = (visible_target_x - start_x) / total_path
    show_text_frame = int(0.55 * (FRAMES - 1))

    total_frames = FRAMES + typing_frames + delay_frames

    def make_frame(i: int) -> Image.Image:
        # Progress for stars: always based on total_frames
        star_progress = i / (total_frames - 1)
        star_offset = int((end_x - start_x) * star_progress * 0.15)
        stars = [((sx - star_offset) % WIDTH, sy) for sx, sy in original_stars]

        # Progress for crewmate: only during FRAMES, then stays at end
        if i < FRAMES:
            crewmate_progress = i / (FRAMES - 1)
        else:
            crewmate_progress = 1.0
        x = int(start_x + (end_x - start_x) * crewmate_progress)
        angle = 575 * crewmate_progress
        crewmate_img = crewmate_img_orig.rotate(
            angle, resample=Image.BICUBIC, expand=True
        )

        # Typing effect for text
        if i < show_text_frame:
            frame_text = ""
        elif i < show_text_frame + typing_frames:
            chars_to_show = int(
                len(text) * ((i - show_text_frame + 1) / typing_frames)
            )
            frame_text = text[:chars_to_show]
        else:
            frame_text = text

        try:
            return draw_frame(crewmate_img, stars, frame_text, x)
        finally:
            crewmate_img.close()

    sample_step = max(1, total_frames // 12)
    sample_frames = range(0, total_frames, sample_step)

    strip_w = 64
    strip = Image.new("RGB", (strip_w * len(sample_frames), HEIGHT))
    try:
        for idx, frame_index in enumerate(sample_frames):
            sample = make_frame(frame_index)
            try:
                resized = sample.resize((strip_w, HEIGHT))
                try:
                    strip.paste(resized, (idx * strip_w, 0))
                finally:
                    resized.close()
            finally:
                sample.close()
        palette = strip.quantize(
            colors=256, method=Image.MEDIANCUT
        )
    finally:
        strip.close()

    frames = []
    try:
        for frame_index in range(total_frames):
            frame = make_frame(frame_index)
            try:
                frames.append(
                    frame.quantize(
                        palette=palette,
                        dither=Image.FLOYDSTEINBERG,
                    )
                )
            finally:
                frame.close()

        fp = BytesIO()
        try:
            frames[0].save(
                fp,
                "GIF",
                save_all=True,
                append_images=frames[1:],
                duration=frame_duration,
                loop=0,
            )
        except Exception:
            fp.close()
            raise
        fp.seek(0)
        return fp
    finally:
        for frame in frames:
            frame.close()
        palette.close()
        crewmate_img_orig.close()
        _trim_memory()


class Amogus(interactions.Extension):
    """Extension for /amogus command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self._gif_lock = asyncio.Semaphore(1)

    @hybrid_slash_command(
        name="amogus",
        description="Amogus.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.USER,
                name="user",
                description="Targeted user",
                required=True,
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.INTEGER,
                name="impostor",
                description="Whether the user is an impostor or not",
                required=False,
                choices=[
                    {"name": "Impostor", "value": 1},
                    {"name": "Not Impostor", "value": 0},
                ],
            ),
        ],
    )
    async def amogus(
        self,
        ctx: HybridContext,
        user: interactions.Member,
        impostor: int | None = None,
    ) -> None:
        """Amogus."""

        await ctx.defer()
        if impostor is None:
            impostor = bool(random.randint(0, 1))
        else:
            impostor = bool(impostor)

        async with self._gif_lock:
            buf = await get_response(
                user.display_avatar.url, session=self.client.session
            )

            if not buf:
                return await ctx.send(
                    "Failed to download avatar. Please try again later.",
                    ephemeral=True,
                )

            try:
                fp = await asyncio.to_thread(
                    make_gif, user.display_name, impostor, buf
                )
            finally:
                buf.close()

            file = interactions.File(file=fp, file_name="amogus.gif")
            try:
                await ctx.send(file=file)
            finally:
                fp.close()
        from src.common.utils import send_promote

        await send_promote(ctx, "easy")


def setup(client) -> None:
    """Setup the extension."""
    Amogus(client)
    logging.info("Loaded Misc extension.")
