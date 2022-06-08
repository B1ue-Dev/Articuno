"""
This module is for emoji management commands.

(C) 2022 - Jimmy-Blue
"""

import io
import re
import interactions
from interactions import extension_command as command
import aiohttp
from utils.permission import Permissions, has_permission


def get_emoji_id(emoji: str):
    """
    This method returns the id of the emoji string in message content
    :param emoji
    :type str
    :return str
    """
    try:
        return re.findall(r'<a?:[a-zA-Z0-9_]+:(\d+)>', emoji)[0]
    except IndexError:
        if emoji.isnumeric() and len(emoji) > 0:
            return emoji
        else:
            return None


class Emoji(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="emoji",
        description="Emoji commands",
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="info",
                description="Get the information about an emoji",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="emoji",
                        description="Targeted emoji",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="steal",
                description="Steal an emoji from another server and add it to the current server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="emoji",
                        description="Targeted emoji",
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="emoji_name",
                        description="Name for the stolen emoji",
                        required=False
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="add",
                description="Add an emoji from an url to the current server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="url",
                        description="Url to the emoji",
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="emoji_name",
                        description="Name for the added emoji",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="remove",
                description="Remove an emoji from the current server",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="emoji",
                        description="Targeted emoji",
                        required=True
                    )
                ]
            )
        ],
        dm_permission=False
    )
    async def _emoji(self, ctx: interactions.CommandContext,
        sub_command: str,
        emoji: str = None,
        url: str = None,
        emoji_name: str = None
    ):
        if sub_command == "info":
            await self._emoji_info(ctx, emoji)
        elif sub_command == "steal":
            await self._emoji_steal(ctx, emoji, emoji_name)
        elif sub_command == "add":
            await self._emoji_add(ctx, url, emoji_name)
        elif sub_command == "remove":
            await self._emoji_remove(ctx, emoji)

    async def _emoji_info(self, ctx: interactions.CommandContext, emoji: str):
        emoji_id = get_emoji_id(emoji)
        if emoji_id:
            _emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
            if _emoji.name is not None:
                image = interactions.EmbedImageStruct(url=_emoji.url)
                embed = interactions.Embed(
                    title=f"``<a:{_emoji.name}:{_emoji.id}>``" if _emoji.animated else f"``<:{_emoji.name}:{_emoji.id}>``",
                    description=f"[Emoji link]({_emoji.url})",
                    color=0x788cdc,
                    image=image
                )
                await ctx.send(content=f"<{_emoji.url}>", embeds=embed)
            else:
                await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.", ephemeral=True)
                return
        elif len(emoji) > 0:
            guild = await ctx.get_guild()
            emojis = await guild.get_all_emoji()
            _emoji = None
            for e in emojis:
                if e.name == emoji:
                    _emoji = e
                    break
                else:
                    continue
            if _emoji:
                image = interactions.EmbedImageStruct(url=_emoji.url)
                embed = interactions.Embed(
                    title=f"``<a:{_emoji.name}:{_emoji.id}>``" if _emoji.animated else f"``<:{_emoji.name}:{_emoji.id}>``",
                    description=f"[Emoji link]({_emoji.url})",
                    color=0x788cdc,
                    image=image
                )
                await ctx.send(content=f"<{_emoji.url}>", embeds=embed)
            else:
                await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.", ephemeral=True)
                return

    async def _emoji_steal(self, ctx: interactions.CommandContext, emoji: str, emoji_name: str = None):
        if not (
            has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
            has_permission(int(ctx.author.permissions),
                           Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)

        guild = await ctx.get_guild()
        boost = int(guild.premium_subscription_count)
        if boost <= 0:
            emoji_limit = 50
        elif 2 <= boost < 7:
            emoji_limit = 100
        elif 7 <= boost < 14:
            emoji_limit = 150
        elif boost >= 14:
            emoji_limit = 250
        _emojis = await guild.get_all_emoji()
        if len(_emojis) >= emoji_limit:
            return await ctx.send(content="The server has reached maximum emoji slots.", ephemeral=True)

        if emoji.startswith("<") and not emoji.startswith("<a") and emoji.endswith(">"):
            emoji_id = get_emoji_id(emoji)
            if emoji_id:
                if not emoji_name:
                    emoji_name = re.findall(
                        r"(?<=:)(.*)(?=:)", emoji)[0]
                _url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
                async with aiohttp.ClientSession() as session:
                    async with session.get(_url) as resp:
                        if resp.status == 200:
                            _io = (io.BytesIO(await resp.read())).read()
                            image = interactions.Image(
                                file="unknown.png", fp=_io)
                            await guild.create_emoji(image=image, name=emoji_name)
                            await ctx.send(content=f"Emoji `:{emoji_name}:` was created.")
                        else:
                            await ctx.send(content="Invalid url. Please try again", ephemeral=True)
                            return
            else:
                await ctx.send(content="Invalid emoji. Please try again.", ephemeral=True)
                return

        elif emoji.startswith("<a") and emoji.endswith(">"):
            emoji_id = get_emoji_id(emoji)
            if emoji_id:
                if not emoji_name:
                    emoji_name = re.findall(
                        r"(?<=:)(.*)(?=:)", emoji)[0]
                _url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
                async with aiohttp.ClientSession() as session:
                    async with session.get(_url) as resp:
                        if resp.status == 200:
                            _io = (io.BytesIO(await resp.read())).read()
                            image = interactions.Image(
                                file="unknown.png", fp=_io)
                            await guild.create_emoji(image=image, name=emoji_name)
                            await ctx.send(content=f"Emoji `:{emoji_name}:` was created.")
                        else:
                            await ctx.send(content="Invalid url. Please try again", ephemeral=True)
                            return
            else:
                await ctx.send(content="Invalid emoji. Please try again.", ephemeral=True)
                return

    async def _emoji_add(self, ctx: interactions.CommandContext, url: str, emoji_name: str):
        if not (
            has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
            has_permission(int(ctx.author.permissions),
                           Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)

        guild = await ctx.get_guild()
        boost = int(guild.premium_subscription_count)
        if boost <= 0:
            emoji_limit = 50
        elif 2 <= boost < 7:
            emoji_limit = 100
        elif 7 <= boost < 14:
            emoji_limit = 150
        elif boost >= 14:
            emoji_limit = 250
        _emojis = await guild.get_all_emoji()
        if len(_emojis) >= emoji_limit:
            await ctx.send(content="The server has reached maximum emoji slots.", ephemeral=True)
            return
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        if resp.content_type in {"image/png", "image/jpeg", "imgage/jpg, image/webp"}:
                            _io = (io.BytesIO(await resp.read())).read()
                            image = interactions.Image(
                                fp=_io, file="unknown.png")
                            guild = await ctx.get_guild()
                            await guild.create_emoji(image=image, name=emoji_name)
                            await ctx.send(content=f"Emoji `:{emoji_name}:` was created.")
                        elif resp.content_type in {"image/gif"}:
                            _io = (io.BytesIO(await resp.read())).read()
                            image = interactions.Image(
                                fp=_io, file="unknown.gif")
                            guild = await ctx.get_guild()
                            await guild.create_emoji(image=image, name=emoji_name)
                            await ctx.send(content=f"Emoji `:{emoji_name}:` was created.")
                        else:
                            await ctx.send(content="Invalid url. Please try again.\nSupported format: png, jpeg, jpg, webp, gif", ephemeral=True)
                            return
                    else:
                        await ctx.send(content="Invalid url. Please try again.", ephemeral=True)
                        return

    async def _emoji_remove(self, ctx: interactions.CommandContext, emoji: str):
        if not (
            has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
            has_permission(int(ctx.author.permissions),
                           Permissions.ADMINISTRATOR)
        ):
            return await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)
        emoji_id = get_emoji_id(emoji)
        if emoji_id:
            _emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)), _client=self.bot._http)
            if _emoji.name is not None:
                guild = await ctx.get_guild()
                await guild.delete_emoji(_emoji)
                await ctx.send(content=f"Emoji `:{_emoji.name}:` was deleted.")
            else:
                await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.", ephemeral=True)
                return

        elif len(emoji) > 0:
            guild = await ctx.get_guild()
            emojis = await guild.get_all_emoji()
            _emoji = None
            for e in emojis:
                if e.name == emoji:
                    _emoji = e
                    break
                else:
                    continue
            if _emoji:
                await guild.delete_emoji(_emoji)
                await ctx.send(content=f"Emoji `:{_emoji.name}:` was deleted.")
            else:
                await ctx.send(content="Invalid emoji. Please try again and make sure that it is **from** this server.", ephemeral=True)
                return
        else:
            await ctx.send("Invalid emoji. Please try again.", ephemeral=True)


def setup(bot):
    Emoji(bot)
