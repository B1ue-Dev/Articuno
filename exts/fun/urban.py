"""
Urban command.

(C) 2022 - Jimmy-Blue
"""

import logging
import asyncio
import datetime
import interactions
from interactions.ext.wait_for import wait_for_component
from utils.utils import get_response


class Urban(interactions.Extension):
    """Extension for /urban command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="urban",
        description="Define a word on Urban Dictionary.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="term",
                description="The term you want to define",
                required=True,
            )
        ],
    )
    async def _urban(self, ctx: interactions.CommandContext, term: str):
        """Define a word on Urban Dictionary."""

        buttons = [
            interactions.ActionRow(
                components=[
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
                ]
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
            icon_url="https://media.discordapp.net/attachments/1007227062265839647/1011688322512457738/unknown.png",
        )
        embed = interactions.Embed(title=f"{resp['list'][ran]['word']}", footer=footer)
        embed.add_field(
            name="Definition",
            value=definition if len(definition) != 0 else "N/A",
            inline=True,
        )
        embed.add_field(
            name="Example", value=example if len(example) != 0 else "N/A", inline=True
        )

        msg = await ctx.send(embeds=embed, components=buttons)
        while True:
            try:
                res = await wait_for_component(
                    self.client,
                    components=buttons,
                    messages=int(msg.id),
                    timeout=15,
                )
                if int(res.user.id) == int(ctx.user.id):
                    if res.custom_id == "previous":
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
                            icon_url="https://media.discordapp.net/attachments/1007227062265839647/1011688322512457738/unknown.png",
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

                        msg = await res.edit(embeds=embed)

                    elif res.custom_id == "next":
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
                            icon_url="https://media.discordapp.net/attachments/1007227062265839647/1011688322512457738/unknown.png",
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

                        msg = await res.edit(embeds=embed)

                    elif res.custom_id == "stop":
                        await res.edit(components=[])
                        break
                else:
                    msg = await res.edit()

            except asyncio.TimeoutError:
                await msg.edit(components=[])


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Urban(client)
    logging.debug("""[%s] Loaded Urban extension.""", log_time)
