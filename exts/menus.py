"""
This module is for user command and message command.

(C) 2022 - Jimmy-Blue
"""

import asyncio
import interactions
from googletrans import Translator


class Menus(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_message_command(
        name="Translate"
    )
    async def _translate(self, ctx: interactions.CommandContext):
        await ctx.defer(ephemeral=True)
        translator = Translator()
        message = ctx.target
        content = message.content
        lang = translator.detect(content).lang
        translation = translator.translate(content)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png"
        )
        embed = interactions.Embed(
            title=f"Detected language: {lang}",
            description=f"```{message1}```",
            footer=footer
        )

        select_menu = interactions.SelectMenu(
            options=[
                interactions.SelectOption(
                    label="English",
                    emoji=interactions.Emoji(name="🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
                    value="en",
                ),
                interactions.SelectOption(
                    label="French",
                    emoji=interactions.Emoji(name="🇫🇷"),
                    value="fr",
                ),
                interactions.SelectOption(
                    label="Spanish",
                    emoji=interactions.Emoji(name="🇪🇸"),
                    value="es",
                ),
                interactions.SelectOption(
                    label="Chinese",
                    emoji=interactions.Emoji(name="🇨🇳"),
                    value="zh-CN",
                ),
                interactions.SelectOption(
                    label="Vietnamese",
                    emoji=interactions.Emoji(name="🇻🇳"),
                    value="vi",
                ),
                interactions.SelectOption(
                    label="Japanese",
                    emoji=interactions.Emoji(name="🇯🇵"),
                    value="ja",
                ),
                interactions.SelectOption(
                    label="Korean",
                    emoji=interactions.Emoji(name="🇰🇷"),
                    value="ko",
                )
            ],
            placeholder="Select a language",
            custom_id="select_menu"
        )
        await ctx.send(embeds=embed, components=select_menu, ephemeral=True)

        while True:
            try:
                res = await self.bot.wait_for_component(components=select_menu, messages=int(ctx.message.id), timeout=10)
                selects = res.data.values[0]
                await ctx.defer(ephemeral=True)
                translation = translator.translate(content, dest=selects)
                message1 = translation.text

                embed = interactions.Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
                embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")

                await res.edit(embeds=embed, components=select_menu)
            except asyncio.TimeoutError:
                break


    @interactions.extension_user_command(
        name="User Information",
        dm_permission=False
    )
    async def _user_information(self, ctx: interactions.CommandContext):
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
            interactions.EmbedField(name="Name", value=f"{name}#{discriminator}", inline=True),
            interactions.EmbedField(name="ID", value=user_id, inline=True),
            interactions.EmbedField(name="Joined at", value=f"<t:{joined_at}>", inline=False),
            interactions.EmbedField(name="Created on", value=f"<t:{created_at}>", inline=False),
            interactions.EmbedField(name="Bot?", value=bot, inline=True),
            interactions.EmbedField(
                name="Roles",
                value=(
                    ", ".join([f"<@&{role}>" for role in ctx.target.roles])
                    if isinstance(ctx.target, interactions.Member)
                    and ctx.target.roles
                    else "`N/A`"
                )
            )
        ]
        embed = interactions.Embed(
            title="User Information",
            thumbnail=thumbnail,
            fields=fields
        )

        await ctx.send(embeds=embed, ephemeral=True)


def setup(bot):
    Menus(bot)
