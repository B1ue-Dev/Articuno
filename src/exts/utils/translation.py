"""
Translate message using Google Translate.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import googletrans
import interactions
from interactions import integration_types
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
from googletrans import Translator


class Translation(interactions.Extension):
    """Extension for translator app-context command."""

    choices = [
        interactions.SlashCommandChoice(
            name="Arabic",
            value="ar",
        ),
        interactions.SlashCommandChoice(
            name="Chinese",
            value="zh-CN",
        ),
        interactions.SlashCommandChoice(
            name="English",
            value="en",
        ),
        interactions.SlashCommandChoice(
            name="French",
            value="fr",
        ),
        interactions.SlashCommandChoice(
            name="German",
            value="de",
        ),
        interactions.SlashCommandChoice(
            name="Hindi",
            value="hi",
        ),
        interactions.SlashCommandChoice(
            name="Italian",
            value="it",
        ),
        interactions.SlashCommandChoice(
            name="Japanese",
            value="ja",
        ),
        interactions.SlashCommandChoice(
            name="Korean",
            value="ko",
        ),
        interactions.SlashCommandChoice(
            name="Portuguese",
            value="pt",
        ),
        interactions.SlashCommandChoice(
            name="Spanish",
            value="es",
        ),
        interactions.SlashCommandChoice(
            name="Thai",
            value="th",
        ),
        interactions.SlashCommandChoice(
            name="Turkish",
            value="tr",
        ),
        interactions.SlashCommandChoice(
            name="Ukrainian",
            value="uk",
        ),
        interactions.SlashCommandChoice(
            name="Vietnamese",
            value="vi",
        ),
        interactions.SlashCommandChoice(
            name="Welsh",
            value="cy",
        ),
    ]

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.select_menu = interactions.StringSelectMenu(
            [
                interactions.StringSelectOption(
                    label="Arabic",
                    emoji=interactions.PartialEmoji(name="🇦🇪"),
                    value="ar",
                ),
                interactions.StringSelectOption(
                    label="Chinese",
                    emoji=interactions.PartialEmoji(name="🇨🇳"),
                    value="zh-CN",
                ),
                interactions.StringSelectOption(
                    label="English",
                    emoji=interactions.PartialEmoji(name="🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
                    value="en",
                ),
                interactions.StringSelectOption(
                    label="French",
                    emoji=interactions.PartialEmoji(name="🇫🇷"),
                    value="fr",
                ),
                interactions.StringSelectOption(
                    label="German",
                    emoji=interactions.PartialEmoji(name="🇩🇪"),
                    value="de",
                ),
                interactions.StringSelectOption(
                    label="Hindi",
                    emoji=interactions.PartialEmoji(name="🇮🇳"),
                    value="hi",
                ),
                interactions.StringSelectOption(
                    label="Italian",
                    emoji=interactions.PartialEmoji(name="🇮🇹"),
                    value="it",
                ),
                interactions.StringSelectOption(
                    label="Japanese",
                    emoji=interactions.PartialEmoji(name="🇯🇵"),
                    value="ja",
                ),
                interactions.StringSelectOption(
                    label="Korean",
                    emoji=interactions.PartialEmoji(name="🇰🇷"),
                    value="ko",
                ),
                interactions.StringSelectOption(
                    label="Portuguese",
                    emoji=interactions.PartialEmoji(name="🇵🇹"),
                    value="pt",
                ),
                interactions.StringSelectOption(
                    label="Spanish",
                    emoji=interactions.PartialEmoji(name="🇪🇸"),
                    value="es",
                ),
                interactions.StringSelectOption(
                    label="Thai",
                    emoji=interactions.PartialEmoji(name="🇹🇭"),
                    value="th",
                ),
                interactions.StringSelectOption(
                    label="Turkish",
                    emoji=interactions.PartialEmoji(name="🇹🇷"),
                    value="tr",
                ),
                interactions.StringSelectOption(
                    label="Ukrainian",
                    emoji=interactions.PartialEmoji(name="🇺🇦"),
                    value="uk",
                ),
                interactions.StringSelectOption(
                    label="Vietnamese",
                    emoji=interactions.PartialEmoji(name="🇻🇳"),
                    value="vi",
                ),
                interactions.StringSelectOption(
                    label="Welsh",
                    emoji=interactions.PartialEmoji(name="🏴󠁧󠁢󠁷󠁬󠁳󠁿"),
                    value="cy",
                ),
            ],
            placeholder="Select a language",
            custom_id="select_menu",
        )

    @interactions.message_context_menu(name="Translate")
    @integration_types(guild=True, user=True)
    async def msg_cmd_translate(
        self, ctx: interactions.ContextMenuContext
    ) -> None:
        """Translate a text with Context Menu App."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        msg: interactions.Message = ctx.target
        content = msg.content

        if str(content) == "None" or str(content) == "":
            return await ctx.send(
                "No content in this message.", ephemeral=True
            )

        detected_lang = translator.detect(content).lang
        translated_text = translator.translate(content).text

        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                ]
            ),
            description=f"```{translated_text}```",
            footer=interactions.EmbedFooter(
                text="Powered by Google Translate"
            ),
        )

        msg = await ctx.send(
            embeds=embed, components=self.select_menu, ephemeral=True
        )

        while True:
            try:
                res = await self.client.wait_for_component(
                    messages=int(msg.id),
                    timeout=10,
                )
                selects = res.ctx.values[0]
                await res.ctx.defer(edit_origin=True)
                translation = translator.translate(content, dest=selects)
                translated_text = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{translated_text}```",
                    footer=interactions.EmbedFooter(
                        text="Powered by Google Translate"
                    ),
                )

                _select_menu = interactions.StringSelectMenu(
                    self.select_menu.options,
                    placeholder=f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                )

                await res.ctx.edit_origin(
                    embeds=embed, components=_select_menu
                )
            except asyncio.TimeoutError:
                break

    @hybrid_slash_subcommand(
        base="translate",
        base_description="Handle message translation aspects.",
        name="text",
        description="Translate a piece of content.",
    )
    @interactions.slash_option(
        name="content",
        description="The content to translate.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def text(
        self,
        ctx: HybridContext,
        content: interactions.ConsumeRest[str],
    ) -> None:
        """Translate a piece of text."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        detected_lang = translator.detect(content).lang
        translation = translator.translate(content, dest="en")
        translated_text = translation.text

        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                    f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                ]
            ),
            description=f"```{translated_text}```",
            footer=interactions.EmbedFooter(
                text="Powered by Google Translate"
            ),
        )

        msg = await ctx.send(
            embeds=embed, components=self.select_menu, ephemeral=True
        )

        while True:
            try:
                res = await self.client.wait_for_component(
                    messages=int(msg.id),
                    timeout=10,
                )
                selects = res.ctx.values[0]
                await res.ctx.defer(edit_origin=True)
                translation = translator.translate(content, dest=selects)
                translated_text = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{translated_text}```",
                    footer=interactions.EmbedFooter(
                        text="Powered by Google Translate"
                    ),
                )

                _select_menu = interactions.StringSelectMenu(
                    self.select_menu.options,
                    placeholder=f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                )
                await res.ctx.edit_origin(
                    embeds=embed, components=_select_menu
                )
            except asyncio.TimeoutError:
                break

    @hybrid_slash_subcommand(
        base="translate",
        base_description="Handle message translation aspects.",
        name="message",
        description="Translate a message to another language.",
    )
    @interactions.slash_option(
        name="message_id",
        description="The ID of the message to translate.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="channel_id",
        description="The ID of the channel the message belongs to.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="lang",
        description="The language you want to translate to.",
        opt_type=interactions.OptionType.STRING,
        choices=choices,
        required=False,
    )
    async def message(
        self,
        ctx: HybridContext,
        message_id: int,
        channel_id: int,
        lang: str = "en",
    ) -> None:
        """Translate a message to another language."""

        await ctx.defer(ephemeral=True)

        msg: interactions.Message = None
        try:
            msg = await self.client.http.get_message(channel_id, message_id)
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="Invalid message ID or channel ID. Please try again.",
                ephemeral=True,
            )

        translator = Translator()
        content = msg["content"]
        if str(content) == "None" or str(content) == "":
            return await ctx.send(
                "No content in this message.", ephemeral=True
            )

        detected_lang = translator.detect(content).lang
        translation = translator.translate(content, dest=lang)
        translated_text = translation.text
        lang = translator.detect(content).lang

        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                    f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                ]
            ),
            description=f"```{translated_text}```",
            footer=interactions.EmbedFooter(
                text="Powered by Google Translate"
            ),
        )

        msg = await ctx.send(
            embeds=embed, components=self.select_menu, ephemeral=True
        )

        while True:
            try:
                res = await self.client.wait_for_component(
                    messages=int(msg.id),
                    timeout=10,
                )
                selects = res.ctx.values[0]
                await res.ctx.defer(edit_origin=True)
                translation = translator.translate(content, dest=selects)
                translated_text = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(detected_lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{translated_text}```",
                    footer=interactions.EmbedFooter(
                        text="Powered by Google Translate"
                    ),
                )

                _select_menu = interactions.StringSelectMenu(
                    self.select_menu.options,
                    placeholder=f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                )

                await res.ctx.edit_origin(
                    embeds=embed, components=_select_menu
                )
            except asyncio.TimeoutError:
                break


def setup(client) -> None:
    """Setup the extension."""
    Translation(client)
    logging.info("Loaded Translation extension.")
