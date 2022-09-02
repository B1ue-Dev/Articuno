"""
This module is for emoji management commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import re
import interactions
import aiohttp
from utils.permission import Permissions, has_permission


class Emote:
    """
    A custom class objecting representing an emoji.

    :ivar str name: Emoji name.
    :ivar int id: Emoji id.
    :ivar bool animated: Status denoting if this emoji is animated.
    """

    __slots__ = ["name", "id", "animated"]

    name: str
    id: int
    animated: bool

    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name", None)
        self.id = kwargs.get("id", None)
        self.animated = kwargs.get("animated", None)

    def __str__(self):
        return (
            f"<{'a' if self.animated else ''}:{self.name}:{self.id}>"
            if self.id is not None
            else self.name
        )

    @classmethod
    def get_emoji(self, emoji_str: str) -> "Emote":
        """
        Returns the id/name of the emoji string in the message content.

        :param emoji_str: The emoji string.
        :type emoji_str: str
        :return: The ID of the emoji.
        :rtype: int
        """

        if (
            emoji_str.isnumeric() is False
            and emoji_str.startswith("<")
            and emoji_str.endswith(">")
        ):
            emoji_regex = re.compile(r"<?(a)?:(\w*):(\d*)>?")

            parsed = emoji_regex.findall(emoji_str)
            if parsed:
                parsed = tuple(filter(None, parsed[0]))
                if len(parsed) == 3:
                    return Emote(name=parsed[1], id=parsed[2], animated=True)
                else:
                    return Emote(name=parsed[0], id=parsed[1], animated=False)

        elif emoji_str.isnumeric() and len(emoji_str) > 0:
            return Emote(id=int(emoji_str))

        else:
            return Emote(name=str(emoji_str))


class Emoji(interactions.Extension):
    """Extension for /emoji command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(name="emoji")
    async def _emoji(self, *args, **kwargs):
        """Emoji management commands."""
        ...

    @_emoji.subcommand(name="info")
    @interactions.option("Target emoji")
    async def _emoji_info(self, ctx: interactions.CommandContext, emoji: str):
        """Checks the information about an emoji."""

        emote = Emote.get_emoji(emoji)

        if emote.id is not None:
            try:
                _emoji = await interactions.get(
                    self.client,
                    interactions.Emoji,
                    parent_id=int(ctx.guild_id),
                    object_id=int(emote.id),
                )
            except interactions.LibraryException:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid emoji. Please try again and make",
                            " sure that it is **from** this server.",
                        ]
                    ),
                    ephemeral=True,
                )

            if _emoji is None:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid emoji. Please try again and make",
                            " sure that it is **from** this server.",
                        ]
                    ),
                    ephemeral=True,
                )

            image = interactions.EmbedImageStruct(url=_emoji.url)
            embed = interactions.Embed(
                title=f"``<a:{_emoji.name}:{_emoji.id}>``"
                if _emoji.animated
                else f"``<:{_emoji.name}:{_emoji.id}>``",
                description=f"[Emoji link]({_emoji.url})",
                color=0x788CDC,
                image=image,
            )
            await ctx.send(content=f"<{_emoji.url}>", embeds=embed)

        elif emote.id is None and emote.name is not None:
            emojis = (await ctx.get_guild()).emojis
            _emoji = None

            for e in emojis:
                if e.name == emoji:
                    _emoji = e
                    break
                else:
                    continue

            if not _emoji:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid emoji. Please try again and make",
                            " sure that it is **from** this server.",
                        ]
                    ),
                    ephemeral=True,
                )

            image = interactions.EmbedImageStruct(url=_emoji.url)
            embed = interactions.Embed(
                title=f"``<a:{_emoji.name}:{_emoji.id}>``"
                if _emoji.animated
                else f"``<:{_emoji.name}:{_emoji.id}>``",
                description=f"[Emoji link]({_emoji.url})",
                color=0x788CDC,
                image=image,
            )
            await ctx.send(content=f"<{_emoji.url}>", embeds=embed)

        else:
            await ctx.send(
                content="".join(
                    [
                        "Invalid emoji. Please try again and make",
                        " sure that it is **from** this server.",
                    ]
                ),
                ephemeral=True,
            )

    @_emoji.subcommand(name="steal")
    @interactions.option("The emoji you wish to add")
    @interactions.option("The name of the emoji")
    async def _emoji_steal(
        self,
        ctx: interactions.CommandContext,
        emoji: str,
        emoji_name: str = None,
    ):
        """Steals an emoji from another server and adds it to the current one."""

        if not (
            has_permission(
                int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS
            )
            or has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have manage emojis and stickers permission.",
                ephemeral=True,
            )

        emote = Emote.get_emoji(emoji)

        if (
            emote.name is not None
            and emote.id is not None
            and emote.animated is not None
        ):
            guild = await ctx.get_guild()
            _url = (
                f"https://cdn.discordapp.com/emojis/{emote.id}" + ".gif"
                if emote.animated
                else ".png"
            )

            if emoji_name is None:
                emoji_name = emote.name

            async with aiohttp.ClientSession() as session:
                async with session.get(_url) as resp:
                    if resp.status != 200:
                        return await ctx.send(
                            "Invalid emoji. Please try again.", ephemeral=True
                        )

                    _io = (io.BytesIO(await resp.read())).read()
                    image = interactions.Image(
                        file="unknown.gif" if emote.animated else "unknown.png",
                        fp=_io,
                    )
                    try:
                        e = await guild.create_emoji(image=image, name=emoji_name)
                    except interactions.LibraryException:
                        return await ctx.send(
                            "Your server has maxed out emoji slots.", ephemeral=True
                        )

                    await ctx.send(
                        content=(
                            f"Emoji <:{e.name}:{e.id}>`:{e.name}:` was created."
                            if e.animated is not True
                            else f"Emoji <a:{e.name}:{e.id}>`:{e.name}:` was created."
                        )
                    )
        else:
            await ctx.send("Invalid emoji. Please try again.", ephemeral=True)

    @_emoji.subcommand(name="add")
    @interactions.option("The URL of the image")
    @interactions.option("The name of the emoji you want to create")
    async def _emoji_add(
        self, ctx: interactions.CommandContext, url: str, emoji_name: str
    ):
        """Creates an emoji from a URL."""

        if not (
            has_permission(
                int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS
            )
            or has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have manage emojis and stickers permission.",
                ephemeral=True,
            )

        guild = await ctx.get_guild()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send(
                        content="Invalid url. Please try again.", ephemeral=True
                    )

                if resp.content_type not in {
                    "image/png",
                    "image/jpeg",
                    "imgage/jpg",
                    "image/webp",
                    "image/gif",
                }:
                    return await ctx.send(
                        content="".join(
                            [
                                "Invalid url. Please try again.\n",
                                "Supported format: png, jpeg, jpg, webp, gif",
                            ]
                        ),
                        ephemeral=True,
                    )

                _io = (io.BytesIO(await resp.read())).read()
                image = interactions.Image(
                    fp=_io,
                    file="unknown.gif"
                    if resp.content_type == "image/gif"
                    else "unknown.png",
                )
                try:
                    e = await guild.create_emoji(image=image, name=emoji_name)
                except interactions.LibraryException:
                    return await ctx.send(
                        "Your server has maxed out emoji slots.", ephemeral=True
                    )

                await ctx.send(
                    content=(
                        f"Emoji <:{e.name}:{e.id}>`:{e.name}:` was created."
                        if e.animated is not True
                        else f"Emoji <a:{e.name}:{e.id}>`:{e.name}:` was created."
                    )
                )

    @_emoji.subcommand(name="remove")
    @interactions.option("The emoji you wish to remove")
    async def _emoji_remove(self, ctx: interactions.CommandContext, emoji: str):
        """Deletes an emoji from the server."""

        if not (
            has_permission(
                int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS
            )
            or has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(
                content="You do not have manage emojis and stickers permission.",
                ephemeral=True,
            )

        emote = Emote.get_emoji(emoji)

        if emote.id is not None:
            try:
                _emoji = await interactions.get(
                    self.client,
                    interactions.Emoji,
                    parent_id=int(ctx.guild_id),
                    object_id=int(emote.id),
                )
            except interactions.LibraryException:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid emoji. Please try again and make",
                            " sure that it is **from** this server.",
                        ]
                    ),
                    ephemeral=True,
                )

            await _emoji.delete(int(ctx.guild_id))
            await ctx.send(content=f"Emoji `:{_emoji.name}:` was deleted.")

        elif emote.id is None and emote.name is not None:
            emojis = (await ctx.get_guild()).emojis
            _emoji = None

            for e in emojis:
                if e.name == emoji:
                    _emoji = e
                    break
                else:
                    continue

            if not _emoji:
                return await ctx.send(
                    "Invalid emoji. Please try again.", ephemeral=True
                )

            await _emoji.delete(int(ctx.guild_id))
            await ctx.send(content=f"Emoji `:{_emoji.name}:` was deleted.")

        else:
            return await ctx.send("Invalid emoji. Please try again.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Emoji(client)
    logging.debug("""[%s] Loaded Emoji extension.""", log_time)
