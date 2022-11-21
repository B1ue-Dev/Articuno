"""
This module is for user command and message command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import asyncio
import interactions
from interactions.ext.wait_for import wait_for_component
from googletrans import Translator


class Translation(interactions.Extension):
    """Extension for translator app-context command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.select_menu = interactions.SelectMenu(
            options=[
                interactions.SelectOption(
                    label="Arabic",
                    emoji=interactions.Emoji(name="🇦🇪"),
                    value="ar",
                ),
                interactions.SelectOption(
                    label="Chinese",
                    emoji=interactions.Emoji(name="🇨🇳"),
                    value="zh-CN",
                ),
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
                    label="German",
                    emoji=interactions.Emoji(name="🇩🇪"),
                    value="de",
                ),
                interactions.SelectOption(
                    label="Hindi",
                    emoji=interactions.Emoji(name="🇮🇳"),
                    value="hi",
                ),
                interactions.SelectOption(
                    label="Italian",
                    emoji=interactions.Emoji(name="🇮🇹"),
                    value="it",
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
                ),
                interactions.SelectOption(
                    label="Portuguese",
                    emoji=interactions.Emoji(name="🇵🇹"),
                    value="pt",
                ),
                interactions.SelectOption(
                    label="Spanish",
                    emoji=interactions.Emoji(name="🇪🇸"),
                    value="es",
                ),
                interactions.SelectOption(
                    label="Thai",
                    emoji=interactions.Emoji(name="🇹🇭"),
                    value="th",
                ),
                interactions.SelectOption(
                    label="Turkish",
                    emoji=interactions.Emoji(name="🇹🇷"),
                    value="tr",
                ),
                interactions.SelectOption(
                    label="Ukrainian",
                    emoji=interactions.Emoji(name="🇺🇦"),
                    value="uk",
                ),
                interactions.SelectOption(
                    label="Vietnamese",
                    emoji=interactions.Emoji(name="🇻🇳"),
                    value="vi",
                ),
                interactions.SelectOption(
                    label="Welsh",
                    emoji=interactions.Emoji(name="🏴󠁧󠁢󠁷󠁬󠁳󠁿"),
                    value="cy",
                ),
            ],
            placeholder="Select a language",
            custom_id="select_menu",
        )

    @interactions.extension_message_command(name="Translate")
    async def _msg_translate(self, ctx: interactions.CommandContext):
        """Translate a text with Context Menu App."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        message = ctx.target
        content = message.content
        lang = translator.detect(content).lang
        translation = translator.translate(content)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title=f"Detected language: {lang}",
            description=f"```{message1}```",
            footer=footer,
        )

        await ctx.send(embeds=embed, components=self.select_menu, ephemeral=True)

        while True:
            try:
                res = await wait_for_component(
                    self.client,
                    components=self.select_menu,
                    messages=int(ctx.message.id),
                    timeout=10,
                )
                selects = res.data.values[0]
                await ctx.defer(ephemeral=True)
                translation = translator.translate(content, dest=selects)
                message1 = translation.text

                embed = interactions.Embed(
                    title=f"Detected language: {lang}", description=f"```{message1}```"
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
                )

                await res.edit(embeds=embed, components=self.select_menu)
            except asyncio.TimeoutError:
                break

    @interactions.extension_command(
        name="translate",
        description="Translate a piece of text or a message to another language.",
    )
    async def _translate(self, *args, **kwargs):
        ...

    @_translate.subcommand(name="text")
    @interactions.option("The text to translate.")
    @interactions.option(
        "The language you want to translate to.",
        choices=[
            interactions.Choice(
                name="Arabic",
                value="ar",
            ),
            interactions.Choice(
                name="Chinese",
                value="zh-CN",
            ),
            interactions.Choice(
                name="English",
                value="en",
            ),
            interactions.Choice(
                name="French",
                value="fr",
            ),
            interactions.Choice(
                name="German",
                value="de",
            ),
            interactions.Choice(
                name="Hindi",
                value="hi",
            ),
            interactions.Choice(
                name="Italian",
                value="it",
            ),
            interactions.Choice(
                name="Japanese",
                value="ja",
            ),
            interactions.Choice(
                name="Korean",
                value="ko",
            ),
            interactions.Choice(
                name="Portuguese",
                value="pt",
            ),
            interactions.Choice(
                name="Spanish",
                value="es",
            ),
            interactions.Choice(
                name="Thai",
                value="th",
            ),
            interactions.Choice(
                name="Turkish",
                value="tr",
            ),
            interactions.Choice(
                name="Ukrainian",
                value="uk",
            ),
            interactions.Choice(
                name="Vietnamese",
                value="vi",
            ),
            interactions.Choice(
                name="Welsh",
                value="cy",
            ),
        ],
    )
    async def _translate_text(
        self,
        ctx: interactions.CommandContext,
        text: str,
        lang: str = "en",
    ):
        """Translate a piece of text."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        content = text
        _lang = translator.detect(content).lang
        translation = translator.translate(content, dest=lang)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title=f"Detected language: {_lang}",
            description=f"```{message1}```",
            footer=footer,
        )

        await ctx.send(embeds=embed, components=self.select_menu, ephemeral=True)

        while True:
            try:
                res = await wait_for_component(
                    self.client,
                    components=self.select_menu,
                    messages=int(ctx.message.id),
                    timeout=10,
                )
                selects = res.data.values[0]
                await ctx.defer(ephemeral=True)
                translation = translator.translate(content, dest=selects)
                message1 = translation.text

                embed = interactions.Embed(
                    title=f"Detected language: {lang}", description=f"```{message1}```"
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
                )

                await res.edit(embeds=embed, components=self.select_menu)
            except asyncio.TimeoutError:
                break

    @_translate.subcommand(name="message")
    @interactions.option("The ID of the message to translate.")
    @interactions.option(
        "The language you want to translate to.",
        choices=[
            interactions.Choice(
                name="Arabic",
                value="ar",
            ),
            interactions.Choice(
                name="Chinese",
                value="zh-CN",
            ),
            interactions.Choice(
                name="English",
                value="en",
            ),
            interactions.Choice(
                name="French",
                value="fr",
            ),
            interactions.Choice(
                name="German",
                value="de",
            ),
            interactions.Choice(
                name="Hindi",
                value="hi",
            ),
            interactions.Choice(
                name="Italian",
                value="it",
            ),
            interactions.Choice(
                name="Japanese",
                value="ja",
            ),
            interactions.Choice(
                name="Korean",
                value="ko",
            ),
            interactions.Choice(
                name="Portuguese",
                value="pt",
            ),
            interactions.Choice(
                name="Spanish",
                value="es",
            ),
            interactions.Choice(
                name="Thai",
                value="th",
            ),
            interactions.Choice(
                name="Turkish",
                value="tr",
            ),
            interactions.Choice(
                name="Ukrainian",
                value="uk",
            ),
            interactions.Choice(
                name="Vietnamese",
                value="vi",
            ),
            interactions.Choice(
                name="Welsh",
                value="cy",
            ),
        ],
    )
    async def _translate_message(
        self,
        ctx: interactions.CommandContext,
        message_id: str,
        lang: str = "en",
    ):
        """Translate a message to another language."""

        await ctx.defer(ephemeral=True)

        _message = await interactions.get(
            self.client,
            interactions.Message,
            parent_id=int(ctx.channel_id),
            object_id=int(message_id),
        )

        translator = Translator()
        content = _message.content
        _lang = translator.detect(content).lang
        translation = translator.translate(content, dest=lang)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title=f"Detected language: {_lang}",
            description=f"```{message1}```",
            footer=footer,
        )

        await ctx.send(embeds=embed, components=self.select_menu, ephemeral=True)

        while True:
            try:
                res = await wait_for_component(
                    self.client,
                    components=self.select_menu,
                    messages=int(ctx.message.id),
                    timeout=10,
                )
                selects = res.data.values[0]
                await ctx.defer(ephemeral=True)
                translation = translator.translate(content, dest=selects)
                message1 = translation.text

                embed = interactions.Embed(
                    title=f"Detected language: {lang}", description=f"```{message1}```"
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
                )

                await res.edit(embeds=embed, components=self.select_menu)
            except asyncio.TimeoutError:
                break


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Translation(client)
    logging.debug("""[%s] Loaded Translation extension.""", log_time)
