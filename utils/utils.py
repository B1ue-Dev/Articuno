"""
Utils for Articuno.

(C) 2022-2023 - B1ue-Dev
"""

import math
import io
from typing import Any
from datetime import datetime, timedelta, timezone
import aiohttp
from beanie import Document
from utils.colorthief import ColorThief


__all__ = ("tags",)


class tags(Document):
    guild_id: str
    tags: dict


async def get_response(
    url: str = None, params: dict = None, headers: dict = None
) -> Any:
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
                    return io.BytesIO(await resp.read())
    await session.close()


def natural_size(size_in_bytes: int) -> str:
    """Returns the natural human-friendly size format."""

    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    power = int(math.log(size_in_bytes, 1024))
    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


def timestamp(times: str) -> int:
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


def send_as_file(text: str) -> io.StringIO:
    """Converts a text into a bytesteam object."""

    _io = io.StringIO(text)
    _io.seek(0)
    return _io


def get_color(img) -> str:
    """
    Get the dominant color of an image.
    :param img: The image.
    :type img:
    :return: The dominant color hex.
    :rtype: str
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
