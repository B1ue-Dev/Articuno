"""
/amogus command.

(C) 2025 - B1ue-Dev
"""

import logging
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.common.utils import get_response

WIDTH, HEIGHT = 800, 450
FRAMES = 95  # Total frames for the animation, + for faster animation and - for slower
STAR_COUNT = 80


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
    font = ImageFont.truetype("arial.ttf", 32)
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


async def make_gif(username, impostor, image):
    member_avatar = Image.open(await get_response(image)).convert("RGBA")
    crewmate_img_orig = member_avatar.resize((128, 128), Image.LANCZOS)

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

    frames = []
    for i in range(total_frames):
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

        frame = draw_frame(crewmate_img, stars, frame_text, x)
        frames.append(frame)

    fp = BytesIO()
    frames[0].save(
        fp,
        "GIF",
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,
    )
    fp.seek(0)
    _file = interactions.File(file=fp, file_name="eject.gif")
    return _file


class Amogus(interactions.Extension):
    """Extension for /amogus command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

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
        dm_permission=False,
    )
    async def amogus(
        self,
        ctx: HybridContext,
        user: interactions.Member,
        impostor: int = None,
    ) -> None:
        """Amogus."""

        await ctx.defer()
        if impostor is None:
            impostor = bool(random.randint(0, 1))
        else:
            impostor = bool(impostor)

        _hash: str | int = None
        _url = None
        if isinstance(user, interactions.User):
            if user.avatar is not None:
                _url = user.avatar.url
            else:
                _hash = (user.id << 22) % 6
        elif isinstance(user, interactions.Member):
            if user.guild_avatar is not None:
                _url = user.guild_avatar.url
            elif user.avatar is not None:
                _url = user.avatar.url
            elif user.user.avatar is not None:
                _url = user.user.avatar.url
            else:
                _hash = (user.id << 22) % 6

        if isinstance(_hash, int):
            _url: str = f"https://cdn.discordapp.com/embed/avatars/{_hash}.png"

        file = await make_gif(
            user.user.username, impostor=impostor, image=_url
        )
        await ctx.send(file=file)
        from src.common.utils import send_promote

        await send_promote(ctx, "easy")


def setup(client) -> None:
    """Setup the extension."""
    Amogus(client)
    logging.info("Loaded Misc extension.")
