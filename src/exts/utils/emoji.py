"""
Emoji management commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import re
import interactions
import aiohttp
from src.utils.utils import Permissions, has_permission


class Emote:
    """
    A custom class objecting representing an emoji.
    """

    __slots__ = ["name", "id", "animated", "created_at"]

    name: str
    """The name of the emoji."""
    id: int
    """The ID of the emoji."""
    animated: bool
    """True if emoji is animated."""
    created_at: interactions.Timestamp
    """When this emoji is created."""

    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name", None)
        self.id = kwargs.get("id", None)
        self.animated = kwargs.get("animated", None)
        self.created_at = kwargs.get("created_at", None)

    def __str__(self):
        return (
            f"<{'a' if self.animated else ''}:{self.name}:{self.id}>"
            if self.id is not None
            else self.name
        )

    @classmethod
    def get_emoji(cls, emoji_str: str) -> "Emote":
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
                    return Emote(
                        name=parsed[1],
                        id=parsed[2],
                        animated=True,
                        created_at=interactions.to_snowflake(
                            parsed[2]
                        ).created_at,
                    )
                else:
                    return Emote(
                        name=parsed[0],
                        id=parsed[1],
                        animated=False,
                        created_at=interactions.to_snowflake(
                            parsed[1]
                        ).created_at,
                    )

        elif emoji_str.isnumeric() and len(emoji_str) > 0:
            return Emote(id=int(emoji_str))

        else:
            return Emote(name=str(emoji_str))

    @property
    def url(self) -> str:
        """Returns the url of the emoji."""

        return f"https://cdn.discordapp.com/emojis/{self.id}" + (
            ".gif" if self.animated else ".png"
        )


class Emoji(interactions.Extension):
    """Extension for /emoji command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(name="emoji")
    async def emoji(self, ctx: interactions.SlashContext) -> None:
        """Emoji management commands."""
        ...

    @emoji.subcommand()
    @interactions.slash_option(
        name="emoji",
        description="Target emoji",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def info(self, ctx: interactions.SlashContext, emoji: str) -> None:
        """Checks the information about an emoji."""

        emote = Emote.get_emoji(emoji)

        # Checks if string is a valid Discord emoji format.
        if emote.id is not None and emote.name is not None:
            try:
                await self.client.http.get_guild_emoji(
                    int(ctx.guild.id), int(emote.id)
                )
            except interactions.errors.HTTPException:
                return await ctx.send(
                    content="".join(
                        [
                            "Invalid emoji. Please try again and make",
                            " sure that it is **from** this server.",
                        ]
                    ),
                    ephemeral=True,
                )

            _url = f"https://cdn.discordapp.com/emojis/{emote.id}" + (
                ".gif" if emote.animated else ".png"
            )

            image = interactions.EmbedAttachment(url=_url)
            embed = interactions.Embed(
                title=f"``<a:{emote.name}:{emote.id}>``"
                if emote.animated
                else f"``<:{emote.name}:{emote.id}>``",
                description="".join(
                    [
                        f"[Emoji link]({_url})\n",
                        f"Created at: {emote.created_at}",
                    ],
                ),
                color=0x788CDC,
                images=[image],
            )
            await ctx.send(content=f"<{emote.url}>", embeds=embed)

        # If string only contains the emoji name.
        elif emote.id is None and emote.name is not None:
            emojis = await ctx.guild.fetch_all_custom_emojis()
            _emoji: interactions.CustomEmoji = None

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

            url = f"https://cdn.discordapp.com/emojis/{str(_emoji.id)}" + (
                ".png" if not _emoji.animated else ".gif"
            )
            image = interactions.EmbedAttachment(url=url)
            embed = interactions.Embed(
                title=f"``<a:{_emoji.name}:{_emoji.id}>``"
                if _emoji.animated
                else f"``<:{_emoji.name}:{_emoji.id}>``",
                description="".join(
                    [
                        f"[Emoji link]({url})\n",
                        f"Created at: {_emoji.created_at}",
                    ],
                ),
                color=0x788CDC,
                images=[image],
            )
            await ctx.send(content=f"<{url}>", embeds=embed)

        # If string only contains the emoji ID.
        elif emote.id is not None and emote.name is None:
            emojis = await ctx.guild.fetch_all_custom_emojis()
            _emoji: interactions.CustomEmoji = None

            for e in emojis:
                if str(e.id) == str(emoji):
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

            url = f"https://cdn.discordapp.com/emojis/{str(_emoji.id)}" + (
                ".png" if not _emoji.animated else ".gif"
            )
            image = interactions.EmbedAttachment(url=url)
            embed = interactions.Embed(
                title=f"``<a:{_emoji.name}:{_emoji.id}>``"
                if _emoji.animated
                else f"``<:{_emoji.name}:{_emoji.id}>``",
                description="".join(
                    [
                        f"[Emoji link]({url})\n",
                        f"Created at: {_emoji.created_at}",
                    ],
                ),
                color=0x788CDC,
                images=[image],
            )
            await ctx.send(content=f"<{url}>", embeds=embed)

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

    @emoji.subcommand()
    @interactions.slash_option(
        name="emoji",
        description="The emoji you wish to add",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="emoji_name",
        description="The name of the emoji",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    async def steal(
        self,
        ctx: interactions.SlashContext,
        emoji: str,
        emoji_name: str = None,
    ) -> None:
        """Gets an emoji from another server and adds to the current one."""

        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_EMOJIS_AND_STICKERS,
            )
            or has_permission(
                int(ctx.author.guild_permissions), Permissions.ADMINISTRATOR
            )
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
            url = f"https://cdn.discordapp.com/emojis/{str(emote.id)}" + (
                ".png" if not emote.animated else ".gif"
            )

            if emoji_name is None:
                emoji_name = emote.name

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await ctx.send(
                            "Invalid emoji. Please try again.", ephemeral=True
                        )

                    _io = (io.BytesIO(await resp.read())).read()
                    image = interactions.File(
                        file_name="unknown.gif"
                        if emote.animated
                        else "unknown.png",
                        file=_io,
                    )
                    try:
                        e = await ctx.guild.create_custom_emoji(
                            imagefile=image, name=emoji_name
                        )
                    except interactions.errors.HTTPException as err:
                        return await ctx.send(
                            content=f"{err.text}.",
                            ephemeral=True,
                        )

                    await ctx.send(
                        content=(
                            f"Emoji <:{e.name}:{e.id}>`:{e.name}:` was created."
                            if e.animated is not True
                            else f"Emoji <a:{e.name}:{e.id}>`:{e.name}:` was created."
                        )
                    )
        elif emote.id is not None and emote.name is None:
            if emoji_name is None:
                return await ctx.send(
                    content="".join(
                        [
                            "It seems like you are trying to steal an emoji",
                            " through the ID. Please include the name of the",
                            " emoji you wish to steal in the `emoji_name` ",
                            "option.",
                        ],
                    ),
                    ephemeral=True,
                )

            url = f"https://cdn.discordapp.com/emojis/{str(emote.id)}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await ctx.send(
                            "Invalid emoji. Please try again.", ephemeral=True
                        )

                    _io = (io.BytesIO(await resp.read())).read()
                    image = interactions.File(
                        file_name="unknown.gif"
                        if str(resp.content_type) == "image/gif"
                        else "unknown.png",
                        file=_io,
                    )
                    try:
                        e = await ctx.guild.create_custom_emoji(
                            imagefile=image, name=emoji_name
                        )
                    except interactions.errors.HTTPException as err:
                        return await ctx.send(
                            content=f"{err.text}.",
                            ephemeral=True,
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

    @emoji.subcommand()
    @interactions.slash_option(
        name="emoji_name",
        description="The name of the emoji you want to create",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="url",
        description="The URL of the image",
        opt_type=interactions.OptionType.STRING,
        required=False,
    )
    @interactions.slash_option(
        name="image",
        description="The image of the emoji",
        opt_type=interactions.OptionType.ATTACHMENT,
        required=False,
    )
    async def add(
        self,
        ctx: interactions.SlashContext,
        emoji_name: str,
        url: str = None,
        image: interactions.Attachment = None,
    ):
        """Creates an emoji from a URL."""

        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_EMOJIS_AND_STICKERS,
            )
            or has_permission(
                int(ctx.author.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have manage emojis and stickers permission.",
                ephemeral=True,
            )

        if url and image:
            return await ctx.send(
                content="".join(
                    [
                        "You can only choose to add emoji between ",
                        "`url` or `image`. Please try again.",
                    ],
                ),
                ephemeral=True,
            )

        # If the user chooses to add emoji from an URL.
        if url and image is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await ctx.send(
                            content="Invalid url. Please try again.",
                            ephemeral=True,
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
                                    "Invalid url. Please try again.\nSuppo",
                                    "rted format: png, jpeg, jpg, webp, gif",
                                ]
                            ),
                            ephemeral=True,
                        )

                    _io = (io.BytesIO(await resp.read())).read()
                    image = interactions.File(
                        file=_io,
                        file_name="unknown.gif"
                        if resp.content_type == "image/gif"
                        else "unknown.png",
                    )
                    try:
                        e = await ctx.guild.create_custom_emoji(
                            imagefile=image, name=emoji_name
                        )
                    except interactions.errors.HTTPException as err:
                        return await ctx.send(
                            content=f"{err.text}.",
                            ephemeral=True,
                        )

                    await ctx.send(
                        content=(
                            f"Emoji <:{e.name}:{e.id}>`:{e.name}:` was created."
                            if e.animated is not True
                            else f"Emoji <a:{e.name}:{e.id}>`:{e.name}:` was created."
                        )
                    )

        # If the user chooses to add emoji from an attachment.
        if image and url is None:
            await ctx.defer()

            async with aiohttp.ClientSession() as session:
                async with session.get(image.url) as resp:
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
                                    "Invalid url. Please try again.\nSuppo",
                                    "rted format: png, jpeg, jpg, webp, gif",
                                ]
                            ),
                            ephemeral=True,
                        )

                    _io = (io.BytesIO(await resp.read())).read()
                    image = interactions.File(
                        file=_io,
                        file_name="unknown.gif"
                        if resp.content_type == "image/gif"
                        else "unknown.png",
                    )
                    try:
                        e = await ctx.guild.create_custom_emoji(
                            imagefile=image, name=emoji_name
                        )
                    except interactions.errors.HTTPException as err:
                        return await ctx.send(
                            content=f"{err.text}.",
                            ephemeral=True,
                        )

                    await ctx.send(
                        content=(
                            f"Emoji <:{e.name}:{e.id}>`:{e.name}:` was created."
                            if e.animated is not True
                            else f"Emoji <a:{e.name}:{e.id}>`:{e.name}:` was created."
                        )
                    )

    @emoji.subcommand()
    @interactions.slash_option(
        name="emoji",
        description="The emoji you wish to remove",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def remove(self, ctx: interactions.SlashContext, emoji: str):
        """Deletes an emoji from the server."""

        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_EMOJIS_AND_STICKERS,
            )
            or has_permission(
                int(ctx.author.guild_permissions), Permissions.ADMINISTRATOR
            )
        ):
            return await ctx.send(
                content="You do not have manage emojis and stickers permission.",
                ephemeral=True,
            )

        emote = Emote.get_emoji(emoji)

        if emote.id is not None:
            try:
                await self.client.http.delete_guild_emoji(
                    guild_id=int(ctx.guild.id), emoji_id=int(emote.id)
                )
            except interactions.errors.HTTPException as err:
                return await ctx.send(
                    content=f"{err.text}.",
                    ephemeral=True,
                )

            await ctx.send(content=f"Emoji `:{emote.name}:` was deleted.")

        elif emote.id is None and emote.name is not None:
            emojis = await ctx.guild.fetch_all_custom_emojis()
            _emoji: interactions.CustomEmoji = None

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
            try:
                await _emoji.delete()
            except interactions.errors.HTTPException as err:
                return await ctx.send(
                    content=f"{err.text}.",
                    ephemeral=True,
                )

            await ctx.send(content=f"Emoji `:{_emoji.name}:` was deleted.")

        else:
            return await ctx.send(
                "Invalid emoji. Please try again.", ephemeral=True
            )


def setup(client) -> None:
    """Setup the extension."""
    Emoji(client)
    logging.info("Loaded Emoji extension.")
