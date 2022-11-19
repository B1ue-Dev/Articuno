"""
Image search command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import asyncio
import random
import interactions
from interactions.ext.wait_for import wait_for_component
from interactions.ext.wait_for import wait_for
from googleapiclient.discovery import build
from better_profanity import profanity
from const import GOOGLE_CLOUD, GOOGLE_CSE


class Google(interactions.Extension):
    """Extension for Google related seach command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="img",
        description="Search for images (Powered by Google).",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="query",
                description="Query to search for",
                required=True,
            ),
        ],
    )
    async def _img(self, ctx: interactions.CommandContext, query: str):
        """Search for images (Powered by Google)."""

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.Emoji(name="◀"),
                custom_id="previous",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.Emoji(name="▶"),
                custom_id="next",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                emoji=interactions.Emoji(name="🔀"),
                custom_id="random",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                emoji=interactions.Emoji(name="📄"),
                custom_id="page",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                emoji=interactions.Emoji(name="⏹"),
                custom_id="stop",
            ),
        ]

        if profanity.contains_profanity(query) is True:
            return await ctx.send("No result found.", ephemeral=True)

        await ctx.defer()

        ran = int(0)
        resource = build("customsearch", "v1", developerKey=GOOGLE_CLOUD).cse()
        result = resource.list(
            q=f"{query}",
            cx=GOOGLE_CSE,
            searchType="image",  # sort="date"
        ).execute()

        try:
            image_link = result["items"][ran]["link"]
            title = result["items"][ran]["title"]
            displayLink = result["items"][ran]["displayLink"]
            contextLink = result["items"][ran]["image"]["contextLink"]

            embed = interactions.Embed(
                title=f"Image for: {query}",
                color=0x000000,
            )
            embed.set_footer(
                text=f"Google Search • Page {ran}/9",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
            )
            embed.add_field(
                name=f"**{displayLink}**",
                value=f"[{title}]({contextLink})",
                inline=False,
            )
            embed.set_image(url=image_link)

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
                        if res.custom_id == "next":
                            if ran == 9:
                                ran = ran
                            else:
                                ran += 1

                            image_link = result["items"][ran]["link"]
                            title = result["items"][ran]["title"]
                            displayLink = result["items"][ran]["displayLink"]
                            contextLink = result["items"][ran]["image"]["contextLink"]

                            embed = interactions.Embed(
                                title=f"Image for: {query}",
                                color=0x000000,
                            )
                            embed.set_footer(
                                text=f"Google Search • Page {ran}/9",
                                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                            )
                            embed.add_field(
                                name=f"**{displayLink}**",
                                value=f"[{title}]({contextLink})",
                                inline=False,
                            )
                            embed.set_image(url=image_link)

                            msg = await res.edit(embeds=embed, components=buttons)

                        elif res.custom_id == "previous":
                            if ran == 0:
                                ran = 0
                            else:
                                ran -= 1

                            image_link = result["items"][ran]["link"]
                            title = result["items"][ran]["title"]
                            displayLink = result["items"][ran]["displayLink"]
                            contextLink = result["items"][ran]["image"]["contextLink"]

                            embed = interactions.Embed(
                                title=f"Image for: {query}",
                                color=0x000000,
                            )
                            embed.set_footer(
                                text=f"Google Search • Page {ran}/9",
                                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                            )
                            embed.add_field(
                                name=f"**{displayLink}**",
                                value=f"[{title}]({contextLink})",
                                inline=False,
                            )
                            embed.set_image(url=image_link)

                            msg = await res.edit(embeds=embed, components=buttons)

                        elif res.custom_id == "random":
                            ran = random.randint(1, 9)

                            image_link = result["items"][ran]["link"]
                            title = result["items"][ran]["title"]
                            displayLink = result["items"][ran]["displayLink"]
                            contextLink = result["items"][ran]["image"]["contextLink"]

                            embed = interactions.Embed(
                                title=f"Image for: {query}",
                                color=0x000000,
                            )
                            embed.set_footer(
                                text=f"Google Search • Page {ran}/9",
                                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                            )
                            embed.add_field(
                                name=f"**{displayLink}**",
                                value=f"[{title}]({contextLink})",
                                inline=False,
                            )
                            embed.set_image(url=image_link)

                            msg = await res.edit(embeds=embed, components=buttons)

                        elif res.custom_id == "page":

                            await res.send("Which page?", ephemeral=True)

                            async def check(_message: interactions.Message):
                                if int(_message.author.id) == int(ctx.user.id) and int(
                                    _message.channel_id
                                ) == int(ctx.channel_id):
                                    return True
                                else:
                                    return False

                            _msg = await wait_for(
                                self.client,
                                name="on_message_create",
                                check=check,
                                timeout=10,
                            )

                            if _msg.content.isdigit() is False:
                                await res.send(
                                    "That is not a valid number", ephemeral=True
                                )
                            else:
                                ran = int(_msg.content)

                                image_link = result["items"][ran]["link"]
                                title = result["items"][ran]["title"]
                                displayLink = result["items"][ran]["displayLink"]
                                contextLink = result["items"][ran]["image"][
                                    "contextLink"
                                ]

                                embed = interactions.Embed(
                                    title=f"Image for: {query}",
                                    color=0x000000,
                                )
                                embed.set_footer(
                                    text=f"Google Search • Page {ran}/9",
                                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png",
                                )
                                embed.add_field(
                                    name=f"**{displayLink}**",
                                    value=f"[{title}]({contextLink})",
                                    inline=False,
                                )
                                embed.set_image(url=image_link)

                                await _msg.delete()

                                msg = await msg.edit(embeds=embed, components=buttons)

                        elif res.custom_id == "stop":
                            await res.edit(components=[])
                            break
                    else:
                        msg = await res.edit()

                except asyncio.TimeoutError:
                    await msg.edit(components=[])

        except KeyError:
            await ctx.send("No result found.", ephemeral=True)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Google(client)
    logging.debug("""[%s] Loaded Google extension.""", log_time)
