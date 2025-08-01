"""
Image search command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import random
from typing import List
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
import aiohttp
from src.const import GOOGLE_CLOUD, GOOGLE_CSE


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

    def __repr__(self) -> str:
        return f"<Image title={self.title!r} link={self.link!r}>"


async def fetch_images(
    session: aiohttp.ClientSession, query: str, page: int = 1
) -> List[Image]:
    start = (page - 1) * 10 + 1
    url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"key={GOOGLE_CLOUD}&cx={GOOGLE_CSE}&q={query}"
        f"&searchType=image&start={start}"
    )

    async with session.get(url) as response:
        data = await response.json()

        items = data.get("items", [])
        images = []

        for i, item in enumerate(items, start=0):
            try:
                images.append(
                    Image(
                        link=item["link"],
                        title=item["title"],
                        source=item["displayLink"],
                        contextlink=item["image"]["contextLink"],
                    )
                )
            except KeyError:
                logging.warning(
                    f"Missing key in search item with query {query} at {i}, skipping."
                )
                images.append(
                    Image(
                        link=item.get(
                            "link",
                            "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg",
                        ),
                        title=item.get("title", "N/A"),
                        source=item.get("displayLink", "N/A"),
                        contextlink=item.get("image", {}).get(
                            "contextLink", "N/A"
                        ),
                    )
                )

        return images


class Google(interactions.Extension):
    """Extension for Google related seach command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.google_icon: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png"

    @hybrid_slash_command(
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
    @interactions.cooldown(interactions.Buckets.USER, 1, 10)
    async def img(
        self, ctx: HybridContext, *, query: interactions.ConsumeRest[str]
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
                style=interactions.ButtonStyle.SECONDARY,
                emoji=interactions.PartialEmoji(name="⏹"),
                custom_id="stop",
            ),
        ]

        await ctx.defer()

        all_result: "list[Image]" = []
        ran = int(0)
        async with aiohttp.ClientSession() as session:
            res = await fetch_images(session, query, 1)
            for images in res:
                all_result.append(images)

        try:
            ran: int = 0
            all_res = all_result[ran]

            embed = interactions.Embed(
                title=f"Image for: {query}",
                color=0x000000,
            )
            embed.set_footer(
                text=f"Google Search • Page {ran + 1}/10",
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
                        if ran == 9:
                            ran = ran
                        else:
                            ran += 1
                        all_res = all_result[ran]

                    elif res.ctx.custom_id == "previous":
                        if ran == 0:
                            ran = 0
                        else:
                            ran -= 1
                        all_res = all_result[ran]

                    elif res.ctx.custom_id == "random":
                        ran = random.randint(0, 9)
                        all_res = all_result[ran]

                    elif res.ctx.custom_id == "stop":
                        await res.ctx.edit_origin(components=[])
                        break

                    embed = interactions.Embed(
                        title=f"Image for: {query}",
                        color=0x000000,
                    )
                    embed.set_footer(
                        text=f"Google Search  •  Page {ran + 1}/10",
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

                except asyncio.TimeoutError:
                    try:
                        return await msg.edit(components=[])
                    except (
                        interactions.client.errors.NotFound,
                        interactions.client.errors.HTTPException,
                    ):
                        return

        except Exception:
            await ctx.send("No result found. Maybe try another query?")


def setup(client) -> None:
    """Setup the extension."""
    Google(client)
    logging.info("Loaded Google extension.")
