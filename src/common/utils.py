"""
Utils for Articuno.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import math
import random
import asyncio
from io import BytesIO, StringIO
from typing import Union
from enum import Enum
from datetime import datetime, timedelta, timezone
from typing import Annotated
import aiohttp
import interactions
from interactions import Task, IntervalTrigger
from beanie import Document, Indexed
from src.common.colorthief import ColorThief


__all__ = ("tags", "hangman_saves")


class tags(Document):
    guild_id: str
    tags: dict


class hangman_saves(Document):
    user_id: Annotated[int, Indexed(int)]
    user_name: Annotated[str, Indexed(str)]
    highest_point: Annotated[int, Indexed(int)]
    history: list


async def get_response(
    url: str, params: dict | None = None, headers: dict | None = None
) -> Union[dict, BytesIO, None]:
    """Return the data type from the request."""

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status == 200:
                if resp.content_type == "application/json":
                    return await resp.json()
                elif resp.content_type in {
                    "image/png",
                    "image/jpeg",
                    "image/gif",
                }:
                    return BytesIO(await resp.read())
            else:
                logging.critical(f"{url} returned {resp.status}.")
                return None
    await session.close()


def natural_size(size_in_bytes: int) -> str:
    """Returns the natural human-friendly size format."""

    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    power = int(math.log(size_in_bytes, 1024))
    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


def timestamp(times: datetime) -> str:
    """Return the round() format of a timestamp."""

    res = int(f"{times.timestamp():.0f}")
    return f"{res}"


def pretty_date(time: int) -> str:
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc

    :param time: The timestamp.
    :type time: int
    :return: The appropriate comment.
    :rtype: str
    """

    now = datetime.now()
    diff = now - now
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "Just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "A minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"


def send_as_file(text: str) -> StringIO:
    """Converts a text into a bytesteam object."""

    _io = StringIO(text)
    _io.seek(0)
    return _io


def get_color(img) -> int:
    """
    Get the dominant color of an image.
    :param img: The image.
    :type img:
    :return: The dominant color hex.
    :rtype: int
    """

    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)

    def clamp(x):
        return max(0, min(x, 255))

    color = "#{0:02x}{1:02x}{2:02x}".format(
        clamp(dominant_color[0]),
        clamp(dominant_color[1]),
        clamp(dominant_color[2]),
    )
    color = str("0x" + color[1:])
    color = int(color, 16)

    return color


def get_local_time() -> datetime:
    """Returns latest UTC+7 time."""

    utc_time = datetime.now(tz=timezone.utc)
    local_time = utc_time + timedelta(hours=7)
    return local_time


def handle_username(name: str, discriminator: str) -> str:
    """Returns the username in old/new format."""

    if str(discriminator) == "0":
        return f"@{name}"
    else:
        return f"{name}#{discriminator}"


# https://discord.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags
class Permissions(Enum):
    """A class representing Permission."""

    CREATE_INSTANT_INVITE = 0
    KICK_MEMBERS = 1
    BAN_MEMBERS = 2
    ADMINISTRATOR = 3
    MANAGE_CHANNELS = 4
    MANAGE_GUILD = 5
    ADD_REACTIONS = 6
    VIEW_AUDIT_LOG = 7
    PRIORITY_SPEAKER = 8
    STREAM = 9
    VIEW_CHANNEL = 10
    SEND_MESSAGES = 11
    SEND_TTS_MESSAGES = 12
    MANAGE_MESSAGES = 13
    EMBED_LINKS = 14
    ATTACH_FILES = 15
    READ_MESSAGE_HISTORY = 16
    MENTION_EVERYONE = 17
    USE_EXTERNAL_EMOJIS = 18
    VIEW_GUILD_INSIGHTS = 19
    CONNECT = 20
    SPEAK = 21
    MUTE_MEMBERS = 22
    DEAFEN_MEMBERS = 23
    MOVE_MEMBERS = 24
    USE_VAD = 25
    CHANGE_NICKNAME = 26
    MANAGE_NICKNAMES = 27
    MANAGE_ROLES = 28
    MANAGE_WEBHOOKS = 29
    MANAGE_EMOJIS_AND_STICKERS = 30
    USE_APPLICATION_COMMANDS = 31
    REQUEST_TO_SPEAK = 32
    MANAGE_EVENTS = 33
    MANAGE_THREADS = 34
    CREATE_PUBLIC_THREADS = 35
    CREATE_PRIVATE_THREADS = 36
    USE_EXTERNAL_STICKERS = 37
    SEND_MESSAGES_IN_THREADS = 38
    START_EMBEDDED_ACTIVITIES = 39
    MODERATE_MEMBERS = 40
    VIEW_CREATOR_MONETIZATION_ANALYTICS = 41
    USE_SOUNDBOARD = 42
    USE_EXTERNAL_SOUNDS = 45
    SEND_VOICE_MESSAGES = 46
    SEND_POLLS = 49


# https://discord.com/developers/docs/topics/permissions#permissions
def has_permission(
    permission_val: int, permission: Union[Permissions, int]
) -> bool:
    """Check if the user's permission value is equal to the given permission for an action.

    :param permission_val: The user permission value.
    :type permission_val: int
    :param permission: The permission that will be used to compare.
    :type permission: Permission
    :return: True if user has permission, False if not.
    :rtype: bool
    """

    if isinstance(permission, Permissions):
        permission = permission.value

    return permission_val & (1 << permission) == 1 << permission


random_easy_number = 0
random_hard_number = 0
easy_chosen = False
hard_chosen = False


@Task.create(IntervalTrigger(seconds=10))
async def random_promote() -> None:
    global random_easy_number
    global random_hard_number
    global easy_chosen
    global hard_chosen
    if easy_chosen is False:
        easy_chosen = True
        random_easy_number = random.randint(50, 90)
    if hard_chosen is False:
        hard_chosen = True
        random_hard_number = random.randint(100, 250)


async def send_promote(ctx: interactions.SlashContext, cmd_type: str):
    global random_easy_number
    global random_hard_number
    global easy_chosen
    global hard_chosen
    if cmd_type == "easy":
        if random_easy_number != 0:
            random_easy_number -= 1
        else:
            topgg_button = interactions.Button(
                style=interactions.ButtonStyle.URL,
                label="Vote for Articuno",
                url="https://top.gg/bot/809084067446259722/vote",
            )
            donate_button = interactions.Button(
                style=interactions.ButtonStyle.URL,
                label="Support Articuno",
                url="https://buymeacoffee.com/b1uedev",
            )
            msg = await ctx.send(
                components=[topgg_button, donate_button],
                content="**Like the bot?**\n"
                "Consider voting the bot on Top.gg, so more people will be able to know Articuno ✨🦅\n"
                "It's a great way to support Articuno too and help it grow :)\n"
                "-# This message will be deleted in 10 seconds.",
            )
            easy_chosen = False
            await asyncio.sleep(10)
            try:
                await msg.delete()
            except interactions.errors.NotFound:
                pass
    elif cmd_type == "hard":
        if random_hard_number != 0:
            random_hard_number -= 1
        else:
            topgg_button = interactions.Button(
                style=interactions.ButtonStyle.URL,
                label="Vote for Articuno",
                url="https://top.gg/bot/809084067446259722/vote",
            )
            donate_button = interactions.Button(
                style=interactions.ButtonStyle.URL,
                label="Support Articuno",
                url="https://buymeacoffee.com/b1uedev",
            )
            msg = await ctx.send(
                components=[topgg_button, donate_button],
                content="**Like the bot?**\n"
                "Consider voting the bot on Top.gg, so more people will be able to know Articuno ✨🦅\n"
                "It's a great way to support Articuno too and help it grow :)\n"
                "-# This message will be deleted in 10 seconds.",
            )
            hard_chosen = False
            await asyncio.sleep(10)
            try:
                await msg.delete()
            except interactions.errors.NotFound:
                pass
