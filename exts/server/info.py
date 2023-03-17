"""
Information commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import datetime
import interactions
from interactions import UserFlags, Permissions
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

    @interactions.slash_command(
        name="info",
        dm_permission=False,
    )
    async def info(self, *args, **kwargs) -> None:
        """For all information aspects."""
        ...

    @info.subcommand(
        sub_cmd_name="user",
        sub_cmd_description="Shows the information about a user.",
    )
    @interactions.slash_option(
        name="user",
        description="Target user",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    async def user(
        self, ctx: interactions.InteractionContext, user: interactions.Member
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
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            thumbnail=thumbnail,
            footer=footer,
            fields=fields,
        )

        await ctx.send(embeds=embed)
