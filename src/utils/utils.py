"""
An ultility for Articuno.

(C) 2022 - Jimmy-Blue
"""

import io
import math
from datetime import datetime
import aiohttp


async def get_response(url: str = None, params: dict = None):
    """
    Get a response from a URL and return based on the content.
    :param url: The URL to get the response from.
    :type url: str
    :param params: The parameters to send to the URL.
    :type params: dict
    :return: The response.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                if resp.content_type == "application/json":
                    return await resp.json()
                if resp.content_type in {"image/png", "image/jpeg", "image/gif"}:
                    return io.BytesIO(await resp.read())
    await session.close()


def natural_size(size_in_bytes: int) -> str:
    """
    Get a size in bytes and return a human readable string.
    :param size_in_bytes: The size in bytes.
    :type size_in_bytes: int
    :return: The human readable string.
    """
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    power = int(math.log(size_in_bytes, 1024))
    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


def timestamp(times: str) -> int:
    """
    Convert a timestamp to a human-readable format.
    :param times: The timestamp to convert.
    :type times: str
    :return: The human-readable format.
    """
    res = int(f"{times.timestamp():.0f}")
    return f"{res}"


def pretty_date(time: int) -> str:
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if isinstance(time, int):
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
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
