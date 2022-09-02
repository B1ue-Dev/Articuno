"""
Information commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
from io import BytesIO
import interactions
from interactions import UserFlags
from utils.utils import get_response
from utils import cache
from utils.colorthief import ColorThief


async def get_color(img):
    """
    Get the dominant color of an image.

    :param img: The image.
    :type img:
    :return: The dominant color hex.
    :rtype: str
    """

    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)

    return dominant_color


def get_user_flags(flags: UserFlags) -> str | None:
    """
    Get user flags and return them as a string.

    :param flags: User flags.
    :type flags: UserFlags
    :return: User flags as a string.
    :rtype: str|None
    """

    user_flags: list = []
    discord_flags = {
        "STAFF": "Discord Employee",
        "PARTNER": "Partnered Server Owner",
        "HYPESQUAD": "HypeSquad Events Member",
        "BUG_HUNTER_LEVEL_1": "Bug Hunter Level 1",
        "PREMIUM_EARLY_SUPPORTER": "Early Nitro Supporter",
        "BUG_HUNTER_LEVEL_2": "Bug Hunter Level 2",
        "VERIFIED_BOT": "Verified Bot",
        "VERIFIED_DEVELOPER": "Early Verified Bot Developer",
        "DISCORD_CERTIFIED_MODERATOR": "Discord Certified Moderator",
    }

    for flag in UserFlags:
        if flags & flag:
            user_flags.append(discord_flags.get(flag.name))
    user_flags = list(filter(lambda x: x is not None, user_flags))

    return (
        ", ".join([f"{flag}" for flag in user_flags]) if len(user_flags) > 0 else "None"
    )


class Info(interactions.Extension):
    """Extesion for /info commannd."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(name="info", dm_permission=False)
    async def _info(self, *args, **kwargs):
        ...

    @_info.subcommand(name="user")
    @interactions.option("Target user")
    async def _info_user(
        self, ctx: interactions.CommandContext, user: interactions.Member
    ):
        """Shows information about a user."""

        nick = user.nick
        joined_at = round(user.joined_at.timestamp())
        created_at = user.user.id.epoch
        avatar = user.user.avatar_url
        bot = "Yes" if user.user.bot is True else "No"
        public_flags = user.user.public_flags
        hypesquad = None
        flags = get_user_flags(public_flags)
        if isinstance(public_flags, int):
            if public_flags & 1 << 6:
                hypesquad = "<:bravery:957684396268322886> Bravery"
            elif public_flags & 1 << 7:
                hypesquad = "<:brilliance:957684592498843658> Brilliance"
            elif public_flags & 1 << 8:
                hypesquad = "<:balance:957684753174241330> Balance"

        fields = [
            interactions.EmbedField(
                name="Name", value=f"{user.user.username}", inline=True
            ),
            interactions.EmbedField(name="Nickname", value=f"{nick}", inline=True),
            interactions.EmbedField(name="ID", value=f"{user.user.id}", inline=True),
            interactions.EmbedField(
                name="Joined at", value=f"<t:{joined_at}:F>", inline=True
            ),
            interactions.EmbedField(
                name="Created on", value=f"<t:{created_at}:F>", inline=True
            ),
            interactions.EmbedField(
                name="HypeSquad", value=f"{hypesquad}", inline=True
            ),
            interactions.EmbedField(name="Bot", value=f"{bot}", inline=True),
            interactions.EmbedField(name="Flags", value=f"{flags}", inline=True),
            interactions.EmbedField(
                name="Roles",
                value=(
                    ", ".join([f"<@&{role}>" for role in user.roles])
                    if isinstance(user, interactions.Member) and user.roles
                    else "`N/A`"
                ),
            ),
        ]
        thumbnail = interactions.EmbedImageStruct(url=avatar)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            thumbnail=thumbnail,
            footer=footer,
            fields=fields,
        )

        await ctx.send(embeds=embed)

    @_info.subcommand(name="avatar")
    @interactions.option("Target user")
    async def _info_avatar(
        self, ctx: interactions.CommandContext, user: interactions.Member
    ):
        """Get the profile picture URL of a user."""

        def clamp(x):
            return max(0, min(x, 255))

        avatar = user.user.avatar_url
        avatar_url = f"https://cdn.discordapp.com/avatars/{str(user.user.id)}/{str(user.user.avatar)}.png"
        color = await get_response(avatar_url)
        color = await get_color(color)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)
        avatar_jpg = user.user.avatar_url[:-4] + ".jpg"
        avatar_png = user.user.avatar_url[:-4] + ".png"
        avatar_webp = user.user.avatar_url[:-4] + ".webp"
        format = f"".join(
            [
                f"**[** [**JPG**]({avatar_jpg}) **]** | ",
                f"**[** [**PNG**]({avatar_png}) **]** | ",
                f"**[** [**WEBP**]({avatar_webp}) **]**",
            ]
        )
        if user.user.avatar.startswith("a_"):
            format += " | **[** [**GIF**]" + "(" + avatar[:-4] + ".gif) **]**"

        size = f"".join(
            [
                f"**[** [**128**]({avatar_url}?size=128) **]** | ",
                f"**[** [**256**]({avatar_url}?size=256) **]** | ",
                f"**[** [**512**]({avatar_url}?size=512) **]** | ",
                f"**[** [**1024**]({avatar_url}?size=1024) **]**",
            ]
        )

        embed = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            color=color,
            image=interactions.EmbedImageStruct(url=f"{avatar_url}?size=512"),
            footer=interactions.EmbedFooter(
                text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=f"{ctx.user.avatar_url}?size=512",
            ),
            fields=[
                interactions.EmbedField(name="Format", value=format, inline=False),
                interactions.EmbedField(name="Size", value=size, inline=False),
            ],
        )

        await ctx.send(embeds=embed)

    @_info.subcommand(name="server")
    async def _info_server(self, ctx: interactions.CommandContext):
        """Shows information about the server."""

        guild = interactions.Guild(
            **await self.client._http.get_guild(ctx.guild_id, True),
            _client=self.client._http,
        )
        user = interactions.User(
            **await self.client._http.get_user(int(guild.owner_id)),
            _client=self.client._http,
        )
        name = guild.name
        id = str(guild.id)
        icon = guild.icon_url
        boost = guild.premium_subscription_count
        members = guild.approximate_member_count
        channels = await guild.get_all_channels()
        text_channels = 0
        voice_channels = 0
        categories = 0
        for channel in channels:
            if channel.type is interactions.ChannelType.GUILD_TEXT:
                text_channels += 1
            elif channel.type is interactions.ChannelType.GUILD_VOICE:
                voice_channels += 1
            elif channel.type is interactions.ChannelType.GUILD_CATEGORY:
                categories += 1
        verification_level = int(guild.verification_level)
        splash_bool = False
        banner_bool = False
        vanity_url_code_bool = False
        if boost <= 2:
            boost_comment = "Level 0"
        elif 2 <= boost < 7:
            boost_comment = "Level 1"
            splash_bool = True
        elif 7 <= boost < 14:
            boost_comment = "Level 2"
            splash_bool = True
            banner_bool = True
        elif boost >= 14:
            boost_comment = "Level 3"
            splash_bool = True
            banner_bool = True
            vanity_url_code_bool = True
        if verification_level == 0:
            verification_comment = "Unrestricted."
        elif verification_level == 1:
            verification_comment = "Must have verified email on account."
        elif verification_level == 2:
            verification_comment = (
                "Must be registered on Discord for longer than 5 minutes."
            )
        elif verification_level == 3:
            verification_comment = (
                "Must be a member of the server for longer than 10 minutes."
            )
        elif verification_level == 4:
            verification_comment = "Must have a verified phone number."
        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)
        sticker_count = len(guild.stickers)
        preferred_locale = guild.preferred_locale
        joined_at = guild.id.epoch
        premium_progress_bar = guild.premium_progress_bar_enabled
        if premium_progress_bar is True:
            premium_progress_bar_comment = "Enabled"
        else:
            premium_progress_bar_comment = "Disabled"

        fields = [
            interactions.EmbedField(name="ID", value=f"{id}", inline=True),
            interactions.EmbedField(
                name="Owner",
                value=f"{user.mention}\n{user.username}#{user.discriminator}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Boosts",
                value=f"Number: {boost}\n{boost_comment}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Members",
                value=f"Total: {members}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Channel",
                value=f"Text channels: {text_channels}\nVoice channels: {voice_channels}\nCategories: {categories}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Verify Level",
                value=f"Level: {verification_level}\n{verification_comment}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Created on",
                value=f"<t:{joined_at}:F>",
                inline=True,
            ),
            interactions.EmbedField(
                name="Preferred Locale", value=f"{preferred_locale}", inline=True
            ),
            interactions.EmbedField(
                name="Roles",
                value=f"{role_count} roles",
                inline=True,
            ),
            interactions.EmbedField(
                name="Emojis",
                value=f"{emoji_count} emojis",
                inline=True,
            ),
            interactions.EmbedField(
                name="Stickers",
                value=f"{sticker_count} stickers",
                inline=True,
            ),
            interactions.EmbedField(
                name="Premium Progress Bar",
                value=f"{premium_progress_bar_comment}",
                inline=True,
            ),
        ]
        thumbnail = interactions.EmbedImageStruct(url=icon)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        embed = interactions.Embed(
            title=f"{name}",
            color=0x788CDC,
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        components = []

        if splash_bool is True and guild.splash_url is not None:
            components.append(
                interactions.Button(
                    style=interactions.ButtonStyle.LINK,
                    label="Splash URL",
                    url=f"{guild.splash_url}",
                )
            )
        if banner_bool is True and guild.banner_url is not None:
            components.append(
                interactions.Button(
                    style=interactions.ButtonStyle.LINK,
                    label="Banner URL",
                    url=f"{guild.banner_url}",
                )
            )
        if vanity_url_code_bool is True and guild.vanity_url_code is not None:
            components.append(
                interactions.Button(
                    style=interactions.ButtonStyle.LINK,
                    label=f"{guild.vanity_url_code}",
                    url=f"https://discord.gg/{guild.vanity_url_code}",
                )
            )

        await ctx.send(embeds=embed, components=components)

    @interactions.extension_user_command(name="User Information", dm_permission=False)
    async def _user_information(self, ctx: interactions.CommandContext):
        """User context menu for information."""

        name = ctx.target.user.username
        discriminator = str(ctx.target.user.discriminator)
        user_id = str(ctx.target.user.id)
        joined_at = round(ctx.target.joined_at.timestamp())
        created_at = ctx.target.user.id.epoch
        avatar = ctx.target.user.avatar_url
        bot = ctx.target.user.bot
        if bot is True:
            bot = "Yes"
        else:
            bot = "No"

        thumbnail = interactions.EmbedImageStruct(url=avatar)
        fields = [
            interactions.EmbedField(
                name="Name", value=f"{name}#{discriminator}", inline=True
            ),
            interactions.EmbedField(name="ID", value=user_id, inline=True),
            interactions.EmbedField(
                name="Joined at", value=f"<t:{joined_at}:F>", inline=False
            ),
            interactions.EmbedField(
                name="Created on", value=f"<t:{created_at}:F>", inline=False
            ),
            interactions.EmbedField(name="Bot?", value=bot, inline=True),
            interactions.EmbedField(
                name="Roles",
                value=(
                    ", ".join([f"<@&{role}>" for role in ctx.target.roles])
                    if isinstance(ctx.target, interactions.Member) and ctx.target.roles
                    else "`N/A`"
                ),
            ),
        ]
        embed = interactions.Embed(
            title="User Information", thumbnail=thumbnail, fields=fields
        )

        await ctx.send(embeds=embed, ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Info(client)
    logging.debug("""[%s] Loaded Info extension.""", log_time)
