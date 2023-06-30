"""
Information commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from interactions import UserFlags, Permissions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
from utils.utils import get_response
from utils.colorthief import ColorThief


async def get_color(img) -> str:
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


def get_user_flags(flags: UserFlags) -> str:
    """
    Gets user flags and returns them as a string.

    :param flags: User flags.
    :type flags: UserFlags
    :return: User flags as a string.
    :rtype: str
    """

    user_flags: list = []
    discord_flags = {
        "STAFF": "<:BadgeDiscordStaff:1043234580813066270> Discord Employee",
        "PARTNER": "<:BadgeDiscordPartner:1043234716079366184> Partnered Server Owner",
        "HYPESQUAD": "<:BadgeHypesquadEvent:1043234630075158548> HypeSquad Events Member",
        "BUG_HUNTER_LEVEL_1": "<:BadgeDiscordBugHunterLv1:1043234778914242701> Bug Hunter Level 1",
        "PREMIUM_EARLY_SUPPORTER": "<:BadgeEarlySupporter:1043234890566619246> Early Nitro Supporter",
        "BUG_HUNTER_LEVEL_2": "<:BadgeDiscordBugHunterLv2:1043234838255259698> Bug Hunter Level 2",
        "VERIFIED_BOT": "<:BadgeVerifiedBot:1043235024704634900> Verified Bot",
        "VERIFIED_DEVELOPER": "<:BadgeEarlyVerifiedDeveloper:1043234961219657829> Early Verified Bot Developer",
        "DISCORD_CERTIFIED_MODERATOR": "<:BadgeDiscordCertifiedModerator:1043235073169825923> Discord Certified Moderator",
        "ACTIVE_DEVELOPER": "<:BadgeActiveDev:1042443072186896476> Active Developer",
    }

    for flag in UserFlags:
        if flags & flag:
            user_flags.append(discord_flags.get(flag.name))
    user_flags = list(filter(lambda x: x is not None, user_flags))

    return (
        ", ".join([f"{flag}" for flag in user_flags])
        if len(user_flags) > 0
        else "None"
    )


def get_user_permissions(permissions: Permissions) -> str:
    """
    Gets user permissions and returns their special role.

    :param permissions: User permission.
    :type permissions: Permissions
    :return: User special role in guild.
    :rtype: str
    """

    user_permissions: list[str] = []
    server_role: dict = {
        "ADMINISTRATOR": "Server administrator",
        "MANAGE_GUILD": "Manage Guild",
        "MANAGE_CHANNELS": "Manage Channels",
        "MANAGE_MESSAGES": "Manage Messages",
        "MANAGE_ROLES": "Manage Roles",
        "MANAGE_EMOJIS_AND_STICKERS": "Manage Emojis & Stickers",
        "MANAGE_THREADS": "Manage Threads",
        "KICK_MEMBERS": "Kick Members",
        "BAN_MEMBERS": "Ban Members",
        "MODERATE_MEMBERS": "Moderate Members",
    }

    for perm in Permissions:
        if permissions & perm:
            user_permissions.append(server_role.get(perm.name))
    user_permissions = list(filter(lambda x: x is not None, user_permissions))

    return (
        ", ".join([f"{perm}" for perm in user_permissions])
        if len(user_permissions) > 0
        else "None"
    )


class Info(interactions.Extension):
    """Extesion for /info commannd."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_subcommand(
        base="info",
        base_description="For all information aspects.",
        name="user",
        description="Shows the information about a user.",
    )
    @interactions.slash_option(
        name="user",
        description="Target user",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    async def user(
        self,
        ctx: HybridContext,
        user: interactions.Member,
    ) -> None:
        """Shows the information about a user."""

        nick: str = user.nick
        joined_at: int = round(user.joined_at.timestamp())
        created_at: int = round(user.user.created_at.timestamp())
        avatar: str = user.user.avatar.url
        bot: str = "Yes" if user.user.bot is True else "No"
        public_flags: UserFlags = user.user.public_flags
        hypesquad = None
        flags: str = get_user_flags(public_flags)
        permissions: str = get_user_permissions(user.guild_permissions)
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
            interactions.EmbedField(
                name="Nickname", value=f"{nick}", inline=True
            ),
            interactions.EmbedField(
                name="ID", value=f"{user.user.id}", inline=True
            ),
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
            interactions.EmbedField(
                name="Flags", value=f"{flags}", inline=True
            ),
            interactions.EmbedField(
                name="Permissions",
                value=f"{permissions}",
            ),
            interactions.EmbedField(
                name="Roles",
                value=(
                    ", ".join([f"<@&{role.id}>" for role in user.roles])
                    if isinstance(user, interactions.Member) and user.roles
                    else "`N/A`"
                ),
            ),
        ]
        thumbnail = interactions.EmbedAttachment(url=avatar)
        title: str = (
            f"@{user.user.username}"
            if str(user.user.discriminator) == "0"
            else f"{user.user.username}#{user.user.discriminator}"
        )
        footer = interactions.EmbedFooter(
            text="Requested by "
            + (
                f"@{ctx.user.username}"
                if str(ctx.user.discriminator) == "0"
                else f"{ctx.user.username}#{ctx.user.discriminator}"
            ),
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title=title,
            thumbnail=thumbnail,
            footer=footer,
            fields=fields,
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_subcommand(
        base="info",
        base_description="For all information aspects.",
        name="avatar",
        description="Shows the profile picture URL of a user.",
    )
    @interactions.slash_option(
        name="user",
        description="Target user",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    async def avatar(
        self, ctx: HybridContext, user: interactions.Member
    ) -> None:
        """Shows the profile picture URL of a user."""

        def clamp(x):
            return max(0, min(x, 255))

        avatar = user.user.avatar_url
        avatar_url = f"https://cdn.discordapp.com/avatars/{str(user.user.id)}/{str(user.user.avatar.hash)}.png"
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
        format = "".join(
            [
                f"**[** [**JPG**]({avatar_jpg}) **]** | ",
                f"**[** [**PNG**]({avatar_png}) **]** | ",
                f"**[** [**WEBP**]({avatar_webp}) **]**",
            ]
        )
        if user.user.avatar.hash.startswith("a_"):
            format += " | **[** [**GIF**]" + "(" + avatar[:-4] + ".gif) **]**"

        size = "".join(
            [
                f"**[** [**128**]({avatar_url}?size=128) **]** | ",
                f"**[** [**256**]({avatar_url}?size=256) **]** | ",
                f"**[** [**512**]({avatar_url}?size=512) **]** | ",
                f"**[** [**1024**]({avatar_url}?size=1024) **]**",
            ]
        )

        embed = interactions.Embed(
            title=(
                f"@{user.user.username}"
                if str(user.user.discriminator) == "0"
                else f"{user.user.username}#{user.user.discriminator}"
            ),
            color=color,
            images=[
                interactions.EmbedAttachment(url=f"{avatar_url}?size=512")
            ],
            footer=interactions.EmbedFooter(
                text="Requested by "
                + (
                    f"@{ctx.user.username}"
                    if str(ctx.user.discriminator) == "0"
                    else f"{ctx.user.username}#{ctx.user.discriminator}"
                ),
                icon_url=f"{ctx.user.avatar_url}?size=512",
            ),
            fields=[
                interactions.EmbedField(
                    name="Format", value=format, inline=False
                ),
                interactions.EmbedField(name="Size", value=size, inline=False),
            ],
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_subcommand(
        base="info",
        base_description="For all information aspects.",
        name="server",
        description="Shows the information about the server.",
    )
    async def server(self, ctx: HybridContext) -> None:
        """Shows the information about the server."""

        guild: interactions.Guild = ctx.guild
        guild_owner = await guild.fetch_owner()

        name: str = guild.name
        id: str = str(guild.id)
        icon: str = guild.icon.url
        boost: int = guild.premium_subscription_count
        members: int = guild.member_count
        channels: list[interactions.Channel] = guild.channels
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
        boost_comment: str = "N/A"
        if boost < 2:
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
        verification_comment: str = "N/A"
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
        emoji_count = len(await guild.fetch_all_custom_emojis())
        sticker_count = len(await guild.fetch_all_custom_stickers())
        preferred_locale = guild.preferred_locale
        joined_at = guild.joined_at
        premium_progress_bar = guild.premium_progress_bar_enabled
        if premium_progress_bar is True:
            premium_progress_bar_comment = "Enabled"
        else:
            premium_progress_bar_comment = "Disabled"

        fields = [
            interactions.EmbedField(name="ID", value=f"{id}", inline=True),
            interactions.EmbedField(
                name="Owner",
                value=f"{guild_owner.mention}\n"
                + (
                    f"@{guild_owner.username}"
                    if str(guild_owner.discriminator) == "0"
                    else f"{guild_owner.username}#{guild_owner.discriminator}"
                ),
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
                value=f"{joined_at}",
                inline=True,
            ),
            interactions.EmbedField(
                name="Preferred Locale",
                value=f"{preferred_locale}",
                inline=True,
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
        thumbnail = interactions.EmbedAttachment(url=icon)
        footer = interactions.EmbedFooter(
            text="Requested by "
            + (
                f"@{ctx.user.username}"
                if str(ctx.user.discriminator) == "0"
                else f"{ctx.user.username}#{ctx.user.discriminator}"
            ),
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

        if splash_bool is True and guild.splash.url is not None:
            components.append(
                interactions.Button(
                    style=interactions.ButtonStyle.LINK,
                    label="Splash URL",
                    url=f"{guild.splash.url}",
                )
            )
        if banner_bool is True and guild.banner is not None:
            components.append(
                interactions.Button(
                    style=interactions.ButtonStyle.LINK,
                    label="Banner URL",
                    url=f"https://cdn.discordapp.com/banners/{str(guild.id)}/{guild.banner}"
                    + (".gif" if guild.banner.startswith("a_") else ".png"),
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

    @interactions.context_menu(
        name="User Information",
        context_type=interactions.CommandType.USER,
        dm_permission=False,
    )
    async def user_information(
        self, ctx: interactions.InteractionContext
    ) -> None:
        """User context menu for information."""

        user: interactions.Member = ctx.target
        user_id: str = str(user.id)
        joined_at: float = round(user.joined_at.timestamp())
        created_at: float = round(user.created_at.timestamp())
        avatar: str = user.avatar.url
        bot: bool = user.bot
        if bot is True:
            bot = "Yes"
        else:
            bot = "No"

        thumbnail = interactions.EmbedAttachment(url=avatar)
        fields = [
            interactions.EmbedField(
                name="Name",
                value=(
                    f"@{user.username}"
                    if str(user.discriminator) == "0"
                    else f"{user.username}#{user.discriminator}"
                ),
                inline=True,
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
                    ", ".join([f"<@&{role.id}>" for role in user.roles])
                    if isinstance(user, interactions.Member) and user.roles
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
    Info(client)
    logging.info("Loaded Info extension.")
