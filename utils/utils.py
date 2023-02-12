import aiohttp
import math
import io
from datetime import datetime


async def async_dl(url, headers=None):
    """I don't know what this does."""

    # print("Attempting to download {}".format(url))
    total_size = 0
    data = b""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            assert response.status == 200
            while True:
                chunk = await response.content.read(4 * 1024)  # 4k
                data += chunk
                total_size += len(chunk)
                if not chunk:
                    break
                if total_size > 8000000:
                    # Too big...
                    # print("{}\n - Aborted - file too large.".format(url))
                    return None
    return data


async def async_text(url, headers=None):
    """Again."""

    data = await async_dl(url, headers)
    if data != None:
        return data.decode("utf-8", "replace")
    else:
        return data


async def get_response(url: str = None, params: dict = None, headers: dict = None):
    """Return the data type from the request."""

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status == 200:
                if resp.content_type == "application/json":
                    return await resp.json()
                elif resp.content_type in {"image/png", "image/jpeg", "image/gif"}:
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
