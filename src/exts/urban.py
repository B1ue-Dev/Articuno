"""
This module is for a list of fun commands that I have no idea what am I doing. 

(C) 2022 - Jimmy-Blue
"""

import asyncio
import interactions
from utils.utils import get_response


def _create_embed(resp: dict, ran: int) -> interactions.Embed:
    """
    A function to create an embed with the response from the API.

    :param resp: The response from the API.
    :type resp: dict
    :param ran: The page number
    :type ran: int
    :return: interactions.Embed
    """
    _resp = resp
    _ran = ran
    page = int(len(_resp["list"]) - 1)

    definition = _resp["list"][_ran]["definition"]
    if len(definition) > 700:
        definition = definition[:690] + "..."
    example = _resp["list"][_ran]["example"]
    if len(example) > 700:
        example = example[:330] + "..."

    footer = interactions.EmbedFooter(
        text=f"👍 {resp['list'][ran]['thumbs_up']} • 👎 {resp['list'][ran]['thumbs_down']} • Page {ran}/{page}",
    )
    embed = interactions.Embed(
        title=f"{_resp['list'][_ran]['word']}",
        footer=footer,
    )
    embed.add_field(name="Definition", value=definition, inline=True)
    embed.add_field(name="Example", value=example, inline=True)

    return embed


class Urban(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="urban",
        description="Define a word on Urban Dictionary",
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
        await ctx.defer()
        url = "https://api.urbandictionary.com/v0/define"
        params = {"term": term}
        resp = await get_response(url, params=params)

        if len(resp["list"]) == 0:
            embed = interactions.Embed(
                description="No results found.",
            )
            return await ctx.send(embeds=embed, ephemeral=True)

        ran, _ran = int(0), int(0)
        page = int(len(resp["list"]) - 1)

        buttons = [
            interactions.ActionRow(
                components=[
                    interactions.Button(
                        style=interactions.ButtonStyle.PRIMARY,
                        label="◄",
                        custom_id="previous",
                    ),
                    interactions.Button(
                        style=interactions.ButtonStyle.PRIMARY,
                        label="►",
                        custom_id="next",
                    ),
                ]
            )
        ]

        embed = _create_embed(resp, ran)

        msg = await ctx.send(embeds=embed, components=buttons)
        while True:
            try:
                res: interactions.ComponentContext = (
                    await self.client.wait_for_component(
                        components=buttons, messages=int(msg.id), timeout=8
                    )
                )
                if res.author.id == ctx.author.id:
                    if res.custom_id == "previous":
                        if ran == 0:
                            ran, _ran = int(0), int(0)
                        else:
                            ran, _ran = int(ran - 1), int(ran)
                            embed = _create_embed(resp, ran)
                            await res.edit(embeds=embed)

                    elif res.custom_id == "next":
                        if ran == page:
                            ran, _ran = int(page), int(page)
                        else:
                            ran, _ran = int(ran + 1), int(ran)
                            embed = _create_embed(resp, ran)
                            await res.edit(embeds=embed)

            except asyncio.TimeoutError:
                embed = _create_embed(resp, _ran)
                await msg.edit(embeds=embed)


def setup(client):
    Urban(client)
