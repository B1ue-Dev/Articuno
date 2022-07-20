"""
Information commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import random
import interactions
from interactions import UserFlags
from utils import cache


def get_user_flags(flags: UserFlags) -> str|None:
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

    return ", ".join([f"{flag}" for flag in user_flags]) if len(user_flags) > 0 else "None"


class Info(interactions.Extension):
    """Extesion for /info commannd."""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="info",
        description="Information command",
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="user",
                description="Shows information of targeted user",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="Targeted user",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="avatar",
                description="Shows avatar of targeted user",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="Targeted user",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="server",
                description="Shows information of current server"
            )
        ]
    )
    async def _info(self, ctx: interactions.CommandContext, sub_command: str, user: interactions.Member = None):
        if sub_command == "user":
            await self._info_user(ctx, user)
        if sub_command == "avatar":
            await self._info_avatar(ctx, user)
        if sub_command == "server":
            await self._info_server(ctx)

    async def _info_user(self, ctx: interactions.CommandContext, user: interactions.Member):
        role = await (await ctx.get_guild()).get_role(role_id=int(user.roles[0]))
        nick = user.nick
        joined_at = round(user.joined_at.timestamp())
        created_at = user.user.id.epoch
        avatar = user.user.avatar_url
        highest_role_color = role.color
        bot = user.user.bot
        if bot is True:
            bot = "Yes"
        else:
            bot = "No"
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
            interactions.EmbedField(name="Name", value=f"{user.user.username}", inline=True),
            interactions.EmbedField(name="Nickname", value=f"{nick}", inline=True),
            interactions.EmbedField(name="ID", value=f"{user.user.id}", inline=True),
            interactions.EmbedField(name="Joined at", value=f"<t:{joined_at}>", inline=True),
            interactions.EmbedField(name="Created on", value=f"<t:{created_at}>", inline=True),
            interactions.EmbedField(name="Highest role", value=f"{role.mention}", inline=True),
            interactions.EmbedField(name="HypeSquad", value=f"{hypesquad}", inline=True),
            interactions.EmbedField(name="Bot", value=f"{bot}", inline=True),
            interactions.EmbedField(name="Flags", value=f"{flags}", inline=True),
            interactions.EmbedField(
                name="Roles",
                value=(
                    ", ".join([f"<@&{role}>" for role in user.roles])
                    if isinstance(user, interactions.Member)
                    and user.roles
                    else "`N/A`"
                )
            )
        ]
        thumbnail = interactions.EmbedImageStruct(url=avatar)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}"
        )
        embed = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            color=highest_role_color,
            thumbnail=thumbnail,
            footer=footer,
            fields=fields
        )

        await ctx.send(embeds=embed)

    async def _info_avatar(self, ctx: interactions.CommandContext, user: interactions.Member):
        avatar = user.user.avatar_url
        print(avatar)
        avatar_jpg = user.user.avatar_url[:-4] + ".jpg"
        avatar_png = user.user.avatar_url[:-4] + ".png"
        avatar_webp = user.user.avatar_url[:-4] + ".webp"
        message = f"[JPG]({avatar_jpg})  [PNG]({avatar_png})  [WEBP]({avatar_webp})"
        if user.avatar.startswith("a_"):
            message += "  [GIF]" + "(" + avatar[:-4] + ".gif)"

        embed = interactions.Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            description=f"{message}",
            image=interactions.EmbedImageStruct(url=avatar),
            footer=interactions.EmbedFooter(
                text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
                icon_url=f"{ctx.user.avatar_url}"
            )
        )

        await ctx.send(embeds=embed)

    async def _info_server(self, ctx: interactions.CommandContext):
        guild = interactions.Guild(
            **await self.client._http.get_guild(ctx.guild_id),
            _client=self.client._http
        )
        user = interactions.User(
            **await self.client._http.get_user(int(guild.owner_id)),
            _client=self.client._http
        )
        name = guild.name
        id = str(guild.id)
        icon = guild.icon_url
        boost = guild.premium_subscription_count
        members = cache.Storage()._special_guilds[guild]
        member_counts = len(members)
        human = 0
        bot = 0
        for member in members:
            if member.bot is True:
                bot += 1
            else:
                human += 1
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
            verification_comment = "Must be registered on Discord for longer than 5 minutes."
        elif verification_level == 3:
            verification_comment = "Must be a member of the server for longer than 10 minutes."
        elif verification_level == 4:
            verification_comment = "Must have a verified phone number."
        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)
        sticker_count = len(guild.stickers)
        region = guild.region
        joined_at = guild.id.epoch
        premium_progress_bar = guild.premium_progress_bar_enabled
        if premium_progress_bar is True:
            premium_progress_bar_comment = "Enabled"
        else:
            premium_progress_bar_comment = "Disabled"

        fields = [
            interactions.EmbedField(name="ID", value=f"{id}", inline=True),
            interactions.EmbedField(name="Owner", value=f"{user.mention}\n{user.username}#{user.discriminator}", inline=True),
            interactions.EmbedField(name="Boosts", value=f"Number: {boost}\n{boost_comment}", inline=True),
            interactions.EmbedField(name="Member", value=f"Total: {member_counts}\nHuman: {human}\nBot: {bot}", inline=True),
            interactions.EmbedField(name="Channel", value=f"Text channels: {text_channels}\nVoice channels: {voice_channels}\nCategories: {categories}", inline=True),
            interactions.EmbedField(name="Verify Level", value=f"Level: {verification_level}\n{verification_comment}", inline=True),
            interactions.EmbedField(name="Created on", value=f"<t:{joined_at}>", inline=True),
            interactions.EmbedField(name="Region", value=f"{region}", inline=True),
            interactions.EmbedField(name="Roles", value=f"{role_count} roles", inline=True),
            interactions.EmbedField(name="Emojis", value=f"{emoji_count} emojis", inline=True),
            interactions.EmbedField(name="Stickers", value=f"{sticker_count} stickers", inline=True),
            interactions.EmbedField(name="Premium Progress Bar", value=f"{premium_progress_bar_comment}", inline=True),
        ]
        thumbnail = interactions.EmbedImageStruct(url=icon)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}"
        )
        embed = interactions.Embed(
            title=f"{name}",
            color=0x788cdc,
            footer=footer,
            thumbnail=thumbnail,
            fields=fields
        )
        if splash_bool is True and guild.splash_url is not None:
            embed.add_field(name="Splash URL", value=f"[Splash_url]({guild.splash_url})", inline=True)
        if banner_bool is True and guild.banner_url is not None:
            embed.add_field(name="Banner URL", value=f"[Banner_url]({guild.banner_url})", inline=True)
        if vanity_url_code_bool is True and guild.vanity_url_code is not None:
            embed.add_field(name="Vanity URL Code", value=f"discord.gg/{guild.vanity_url_code}", inline=True)

        await ctx.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Info(client)
    logging.debug("""[%s] Loaded Info extension.""", log_time)
    print(f"[{log_time}] Loaded Info extension.")
