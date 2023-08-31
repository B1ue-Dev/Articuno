"""
Translate message using Google Translate.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import googletrans
import interactions
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
    async def msg_cmd_translate(
        self, ctx: interactions.ContextMenuContext
    ) -> None:
        """Translate a text with Context Menu App."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        message: interactions.Message = ctx.target
        content = message.content
        lang = translator.detect(content).lang
        translation = translator.translate(content)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                ]
            ),
            description=f"```{message1}```",
            footer=footer,
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
                message1 = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{message1}```",
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
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

    @interactions.slash_command(
        name="translate",
        description="Handle message translation aspects.",
    )
    async def translate(self, ctx: interactions.SlashContext) -> None:
        """Handle message translation aspects."""
        ...

    @translate.subcommand(
        sub_cmd_name="text",
        sub_cmd_description="Translate a piece of text."
    )
    @interactions.slash_option(
        name="text",
        description="The text to translate.",
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
    async def text(
        self,
        ctx: interactions.SlashContext,
        text: str,
        lang: str = "en",
    ) -> None:
        """Translate a piece of text."""

        await ctx.defer(ephemeral=True)

        translator = Translator()
        content = text
        translation = translator.translate(content, dest=lang)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                ]
            ),
            description=f"```{message1}```",
            footer=footer,
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
                message1 = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{message1}```",
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
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

    @translate.subcommand(
        sub_cmd_name="message",
        sub_cmd_description="Translate a message to another language.",
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
        ctx: interactions.SlashContext,
        message_id: int,
        channel_id: int,
        lang: str = "en",
    ) -> None:
        """Translate a message to another language."""

        await ctx.defer(ephemeral=True)

        _message: interactions.Message = None
        try:
            _message = await self.client.http.get_message(
                channel_id, message_id
            )
        except interactions.errors.HTTPException:
            return await ctx.send(
                content="Invalid message ID or channel ID. Please try again.",
                ephemeral=True,
            )

        translator = Translator()
        content = _message["content"]
        translation = translator.translate(content, dest=lang)
        message1 = translation.text

        footer = interactions.EmbedFooter(
            text="Powered by Google Translate",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
        )
        embed = interactions.Embed(
            title="".join(
                [
                    "Detected language: ",
                    f"{str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                ]
            ),
            description=f"```{message1}```",
            footer=footer,
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
                message1 = translation.text

                embed = interactions.Embed(
                    title="".join(
                        [
                            "Detected language: ",
                            f"{str(googletrans.LANGUAGES.get(lang)).capitalize()}",
                            f" ➡ {str(googletrans.LANGUAGES.get(translation.dest)).capitalize()}",
                        ],
                    ),
                    description=f"```{message1}```",
                )
                embed.set_footer(
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                    text="Google Translate",
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
