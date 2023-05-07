"""
Image search command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import random
import interactions
from utils.utils import get_response
from const import SERPAPI


class Image:
    """Represents an image and its information."""

    def __init__(
        self, link: str, title: str, source: str, contextlink: str
    ) -> None:
        self.link: str = link
        """link: The image URL."""
        self.title: str = title
        """title: The title of the search result."""
        self.source: str = source
        """source: The source of the image."""
        self.contextlink: str = contextlink
        """contextlink: The link to the source."""


class Google(interactions.Extension):
    """Extension for Google related seach command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.google_icon: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png"

    @interactions.slash_command(
        name="img",
        description="Search for images (Powered by Google).",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="query",
                description="Query to search for",
                required=True,
            ),
        ],
    )
    async def img(
        self, ctx: interactions.InteractionContext, query: str
    ) -> None:
        """Search for images (Powered by Google)."""

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.PartialEmoji(name="◀"),
                custom_id="previous",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.PartialEmoji(name="▶"),
                custom_id="next",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.PartialEmoji(name="🔀"),
                custom_id="random",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                emoji=interactions.PartialEmoji(name="📄"),
                custom_id="page",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                emoji=interactions.PartialEmoji(name="⏹"),
                custom_id="stop",
            ),
        ]

        await ctx.defer()

        all_result: "list[Image]" = []
        url = "https://serpapi.com/search.json"
        params = {
            "q": f"{query}",
            "tbm": "isch",
            "ijn": 0,
            "api_key": SERPAPI,
        }

        result = (await get_response(url, params))["images_results"]
        for res in result:
            all_result.append(
                Image(
                    link=res["thumbnail"],
                    title=res["title"],
                    source=res["source"],
                    contextlink=res["link"],
                )
            )

        try:
            ran: int = 0
            all_res = all_result[ran]

            embed = interactions.Embed(
                title=f"Image for: {query}",
                color=0x000000,
            )
            embed.set_footer(
                text=f"Google Search • Page {ran}/99",
                icon_url=self.google_icon,
            )
            embed.add_field(
                name=f"**{all_res.source}**",
                value=f"[{all_res.title}]({all_res.contextlink})",
                inline=False,
            )
            embed.set_image(url=all_res.link)

            msg = await ctx.send(embeds=embed, components=buttons)

            while True:
                try:

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(
                            ctx.user.id
                        ) and int(_ctx.ctx.channel_id) == int(ctx.channel_id)

                    res = await self.client.wait_for_component(
                        components=buttons,
                        messages=int(msg.id),
                        check=_check,
                        timeout=15,
                    )

                    if res.ctx.custom_id == "next":
                        if ran == 99:
                            ran = ran
                        else:
                            ran += 1
                        all_res = all_result[ran]

                        embed = interactions.Embed(
                            title=f"Image for: {query}",
                            color=0x000000,
                        )
                        embed.set_footer(
                            text=f"Google Search  •  Page {ran}/99",
                            icon_url=self.google_icon,
                        )
                        embed.add_field(
                            name=f"**{all_res.source}**",
                            value=f"[{all_res.title}]({all_res.contextlink})",
                            inline=False,
                        )
                        embed.set_image(url=all_res.link)

                        msg = await res.ctx.edit_origin(
                            embeds=embed, components=buttons
                        )

                    elif res.ctx.custom_id == "previous":
                        if ran == 0:
                            ran = 0
                        else:
                            ran -= 1
                        all_res = all_result[ran]

                        embed = interactions.Embed(
                            title=f"Image for: {query}",
                            color=0x000000,
                        )
                        embed.set_footer(
                            text=f"Google Search  •  Page {ran}/99",
                            icon_url=self.google_icon,
                        )
                        embed.add_field(
                            name=f"**{all_res.source}**",
                            value=f"[{all_res.title}]({all_res.contextlink})",
                            inline=False,
                        )
                        embed.set_image(url=all_res.link)

                        msg = await res.ctx.edit_origin(
                            embeds=embed, components=buttons
                        )

                    elif res.ctx.custom_id == "random":
                        ran = random.randint(0, 100)
                        all_res = all_result[ran]

                        embed = interactions.Embed(
                            title=f"Image for: {query}",
                            color=0x000000,
                        )
                        embed.set_footer(
                            text=f"Google Search  •  Page {ran}/99",
                            icon_url=self.google_icon,
                        )
                        embed.add_field(
                            name=f"**{all_res.source}**",
                            value=f"[{all_res.title}]({all_res.contextlink})",
                            inline=False,
                        )
                        embed.set_image(url=all_res.link)

                        msg = await res.ctx.edit_origin(
                            embeds=embed, components=buttons
                        )

                    elif res.ctx.custom_id == "page":
                        await res.ctx.send("Which page?", ephemeral=True)

                        def check(_message: interactions.Message):
                            if int(_message.message.author.id) == int(
                                ctx.user.id
                            ) and int(_message.message.channel.id) == int(
                                ctx.channel_id
                            ):
                                return True
                            else:
                                return False

                        _msg = await self.client.wait_for(
                            event=interactions.events.MessageCreate,
                            checks=check,
                            timeout=10,
                        )

                        if (
                            _msg.message.content.isdigit() is False
                            or int(_msg.message.content) < 0
                            or int(_msg.message.content) > 99
                        ):
                            await res.ctx.send(
                                "That is not a valid number.",
                                ephemeral=True,
                            )
                        else:
                            ran = int(_msg.message.content)
                            all_res = all_result[ran]

                            embed = interactions.Embed(
                                title=f"Image for: {query}",
                                color=0x000000,
                            )
                            embed.set_footer(
                                text=f"Google Search  •  Page {ran}/99",
                                icon_url=self.google_icon,
                            )
                            embed.add_field(
                                name=f"**{all_res.source}**",
                                value=f"[{all_res.title}]({all_res.contextlink})",
                                inline=False,
                            )
                            embed.set_image(url=all_res.link)

                            await _msg.message.delete()

                            msg = await msg.edit(
                                embeds=embed, components=buttons
                            )

                    elif res.ctx.custom_id == "stop":
                        await res.ctx.edit_origin(components=[])
                        break
                    else:
                        msg = await res.ctx.edit_origin()

                except asyncio.TimeoutError:
                    await msg.edit(components=[])

        except KeyError:
            await ctx.send("No result found.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    Google(client)
    logging.info("Loaded Google extension.")
