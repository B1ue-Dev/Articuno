"""
Urban command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import interactions
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)
from utils.utils import get_response


class Urban(interactions.Extension):
    """Extension for /urban command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="urban",
        description="Define a word on Urban Dictionary.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="term",
                description="The term you want to define",
                required=True,
            )
        ],
    )
    async def urban(self, ctx: interactions.SlashContext, term: str) -> None:
        """Define a word on Urban Dictionary."""

        buttons = [
            interactions.ActionRow(
                interactions.Button(
                    style=interactions.ButtonStyle.PRIMARY,
                    label="◀",
                    custom_id="previous",
                ),
                interactions.Button(
                    style=interactions.ButtonStyle.PRIMARY,
                    label="▶",
                    custom_id="next",
                ),
                interactions.Button(
                    style=interactions.ButtonStyle.SECONDARY,
                    label="⏹",
                    custom_id="stop",
                ),
            )
        ]

        await ctx.defer()
        url = "https://api.urbandictionary.com/v0/define"
        params = {"term": term}
        resp = await get_response(url, params=params)

        if len(resp["list"]) == 0:
            embed = interactions.Embed(
                description="No results found.",
            )
            return await ctx.send(embeds=embed, ephemeral=True)

        ran = 0
        page = int(len(resp["list"]) - 1)
        definition = resp["list"][ran]["definition"]
        if len(definition) > 700:
            definition = definition[:690] + "..."
        definition = definition.replace("[", "")
        definition = definition.replace("]", "")
        example = resp["list"][ran]["example"]
        if len(example) > 700:
            example = example[:330] + "..."
        example = example.replace("[", "")
        example = example.replace("]", "")

        footer = interactions.EmbedFooter(
            text="".join(
                [
                    f"👍 {resp['list'][ran]['thumbs_up']} • ",
                    f"👎 {resp['list'][ran]['thumbs_down']} • ",
                    f"Page {ran}/{page}",
                ]
            ),
            icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
        )
        embed = interactions.Embed(
            title=f"{resp['list'][ran]['word']}", footer=footer
        )
        embed.add_field(
            name="Definition",
            value=definition if len(definition) != 0 else "N/A",
            inline=True,
        )
        embed.add_field(
            name="Example",
            value=example if len(example) != 0 else "N/A",
            inline=True,
        )

        msg = await ctx.send(embeds=embed, components=buttons)
        while True:
            try:

                def _check(_ctx):
                    return int(_ctx.ctx.user.id) == int(ctx.user.id)

                res = await self.client.wait_for_component(
                    components=buttons,
                    check=_check,
                    messages=int(msg.id),
                    timeout=15,
                )
                if res.ctx.custom_id == "previous":
                    if ran == 0:
                        ran = 0
                    else:
                        ran -= 1

                    definition = resp["list"][ran]["definition"]
                    if len(definition) > 700:
                        definition = definition[:690] + "..."
                    definition = definition.replace("[", "")
                    definition = definition.replace("]", "")
                    example = resp["list"][ran]["example"]
                    if len(example) > 700:
                        example = example[:330] + "..."
                    example = example.replace("[", "")
                    example = example.replace("]", "")

                    footer = interactions.EmbedFooter(
                        text="".join(
                            [
                                f"👍 {resp['list'][ran]['thumbs_up']} • ",
                                f"👎 {resp['list'][ran]['thumbs_down']} • ",
                                f"Page {ran}/{page}",
                            ]
                        ),
                        icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
                    )
                    embed = interactions.Embed(
                        title=f"{resp['list'][ran]['word']}", footer=footer
                    )
                    embed.add_field(
                        name="Definition",
                        value=definition if len(definition) != 0 else "N/A",
                        inline=True,
                    )
                    embed.add_field(
                        name="Example",
                        value=example if len(example) != 0 else "N/A",
                        inline=True,
                    )

                    msg = await res.ctx.edit_origin(embeds=embed)

                elif res.ctx.custom_id == "next":
                    if ran == page:
                        ran = page
                    else:
                        ran += 1

                    definition = resp["list"][ran]["definition"]
                    if len(definition) > 700:
                        definition = definition[:690] + "..."
                    definition = definition.replace("[", "")
                    definition = definition.replace("]", "")
                    example = resp["list"][ran]["example"]
                    if len(example) > 700:
                        example = example[:330] + "..."
                    example = example.replace("[", "")
                    example = example.replace("]", "")

                    footer = interactions.EmbedFooter(
                        text="".join(
                            [
                                f"👍 {resp['list'][ran]['thumbs_up']} • ",
                                f"👎 {resp['list'][ran]['thumbs_down']} • ",
                                f"Page {ran}/{page}",
                            ]
                        ),
                        icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
                    )
                    embed = interactions.Embed(
                        title=f"{resp['list'][ran]['word']}", footer=footer
                    )
                    embed.add_field(
                        name="Definition",
                        value=definition if len(definition) != 0 else "N/A",
                        inline=True,
                    )
                    embed.add_field(
                        name="Example",
                        value=example if len(example) != 0 else "N/A",
                        inline=True,
                    )

                    msg = await res.ctx.edit_origin(embeds=embed)

                elif res.ctx.custom_id == "stop":
                    await res.ctx.edit_origin(components=[])
                    break
                else:
                    msg = await res.edit()

            except asyncio.TimeoutError:
                await msg.edit(components=[])

    @prefixed_command(name="urban")
    async def _urban(self, ctx: PrefixedContext, *, term: str) -> None:
        """Define a word on Urban Dictionary."""

        buttons = [
            interactions.ActionRow(
                interactions.Button(
                    style=interactions.ButtonStyle.PRIMARY,
                    label="◀",
                    custom_id="previous",
                ),
                interactions.Button(
                    style=interactions.ButtonStyle.PRIMARY,
                    label="▶",
                    custom_id="next",
                ),
                interactions.Button(
                    style=interactions.ButtonStyle.SECONDARY,
                    label="⏹",
                    custom_id="stop",
                ),
            )
        ]

        url = "https://api.urbandictionary.com/v0/define"
        params = {"term": term}
        resp = await get_response(url, params=params)

        if len(resp["list"]) == 0:
            embed = interactions.Embed(
                description="No results found.",
            )
            return await ctx.reply(embeds=embed, ephemeral=True)

        ran = 0
        page = int(len(resp["list"]) - 1)
        definition = resp["list"][ran]["definition"]
        if len(definition) > 700:
            definition = definition[:690] + "..."
        definition = definition.replace("[", "")
        definition = definition.replace("]", "")
        example = resp["list"][ran]["example"]
        if len(example) > 700:
            example = example[:330] + "..."
        example = example.replace("[", "")
        example = example.replace("]", "")

        footer = interactions.EmbedFooter(
            text="".join(
                [
                    f"👍 {resp['list'][ran]['thumbs_up']} • ",
                    f"👎 {resp['list'][ran]['thumbs_down']} • ",
                    f"Page {ran}/{page}",
                ]
            ),
            icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
        )
        embed = interactions.Embed(
            title=f"{resp['list'][ran]['word']}", footer=footer
        )
        embed.add_field(
            name="Definition",
            value=definition if len(definition) != 0 else "N/A",
            inline=True,
        )
        embed.add_field(
            name="Example",
            value=example if len(example) != 0 else "N/A",
            inline=True,
        )

        msg = await ctx.reply(embeds=embed, components=buttons)
        while True:
            try:

                def _check(_ctx):
                    return int(_ctx.ctx.user.id) == int(ctx.user.id)

                res = await self.client.wait_for_component(
                    components=buttons,
                    check=_check,
                    messages=int(msg.id),
                    timeout=15,
                )
                if res.ctx.custom_id == "previous":
                    if ran == 0:
                        ran = 0
                    else:
                        ran -= 1

                    definition = resp["list"][ran]["definition"]
                    if len(definition) > 700:
                        definition = definition[:690] + "..."
                    definition = definition.replace("[", "")
                    definition = definition.replace("]", "")
                    example = resp["list"][ran]["example"]
                    if len(example) > 700:
                        example = example[:330] + "..."
                    example = example.replace("[", "")
                    example = example.replace("]", "")

                    footer = interactions.EmbedFooter(
                        text="".join(
                            [
                                f"👍 {resp['list'][ran]['thumbs_up']} • ",
                                f"👎 {resp['list'][ran]['thumbs_down']} • ",
                                f"Page {ran}/{page}",
                            ]
                        ),
                        icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
                    )
                    embed = interactions.Embed(
                        title=f"{resp['list'][ran]['word']}", footer=footer
                    )
                    embed.add_field(
                        name="Definition",
                        value=definition if len(definition) != 0 else "N/A",
                        inline=True,
                    )
                    embed.add_field(
                        name="Example",
                        value=example if len(example) != 0 else "N/A",
                        inline=True,
                    )

                    msg = await res.ctx.edit_origin(embeds=embed)

                elif res.ctx.custom_id == "next":
                    if ran == page:
                        ran = page
                    else:
                        ran += 1

                    definition = resp["list"][ran]["definition"]
                    if len(definition) > 700:
                        definition = definition[:690] + "..."
                    definition = definition.replace("[", "")
                    definition = definition.replace("]", "")
                    example = resp["list"][ran]["example"]
                    if len(example) > 700:
                        example = example[:330] + "..."
                    example = example.replace("[", "")
                    example = example.replace("]", "")

                    footer = interactions.EmbedFooter(
                        text="".join(
                            [
                                f"👍 {resp['list'][ran]['thumbs_up']} • ",
                                f"👎 {resp['list'][ran]['thumbs_down']} • ",
                                f"Page {ran}/{page}",
                            ]
                        ),
                        icon_url="https://media.discordapp.net/attachments/1054042920203866152/1085875672620220516/urban-dictionary.png",
                    )
                    embed = interactions.Embed(
                        title=f"{resp['list'][ran]['word']}", footer=footer
                    )
                    embed.add_field(
                        name="Definition",
                        value=definition if len(definition) != 0 else "N/A",
                        inline=True,
                    )
                    embed.add_field(
                        name="Example",
                        value=example if len(example) != 0 else "N/A",
                        inline=True,
                    )

                    msg = await res.ctx.edit_origin(embeds=embed)

                elif res.ctx.custom_id == "stop":
                    await res.ctx.edit_origin(components=[])
                    break
                else:
                    msg = await res.edit()

            except asyncio.TimeoutError:
                await msg.edit(components=[])


def setup(client) -> None:
    """Setup the extension."""
    Urban(client)
    logging.info("Loaded Urban extension.")
