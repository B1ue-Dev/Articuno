"""
Fun related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import random
import asyncio
import re

import interactions
from interactions import Message
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response
from src.const import SOME_RANDOM_API


class Fun(interactions.Extension):
    """Extension for fun related commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="coffee",
        description="Send an image of coffee.",
    )
    async def coffee(self, ctx: HybridContext) -> None:
        """Sends an image of coffee."""

        url = "https://coffee.alexflipnote.dev/random.json"
        resp = await get_response(url)
        file = resp["file"]

        image = interactions.EmbedAttachment(url=file)
        embed = interactions.Embed(
            title="Coffee ☕", color=0xC4771D, images=[image]
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="roll",
        description="Roll a dice.",
    )
    async def roll(self, ctx: HybridContext) -> None:
        """Rolls a dice."""

        dice = random.randint(1, 6)
        msg = await ctx.send("I am rolling the dice...")
        await asyncio.sleep(1.5)
        await ctx.edit(message=msg.id, content=f"The number is **{dice}**.")

    @hybrid_slash_command(
        name="flip",
        description="Flip a coin.",
    )
    async def flip(self, ctx: HybridContext) -> None:
        """Flips a coin."""

        coin = random.choice(["heads", "tails"])
        msg = await ctx.send("I am flipping the coin...")
        await asyncio.sleep(1.5)
        await ctx.edit(
            message=msg.id, content=f"The coin landed on **{coin}**."
        )

    @hybrid_slash_command(
        name="joke",
        description="Send a random joke.",
    )
    async def joke(self, ctx: HybridContext) -> None:
        """Sends a random joke."""

        # url = "https://some-random-api.com/joke"
        # resp = await get_response(url)

        # embed = interactions.Embed(
        #     description=resp["joke"],
        #     color=random.randint(0, 0xFFFFFF),
        # )

        # await ctx.send(embeds=embed)
        await ctx.send("This command is under maintenance. ETA is unknown.", ephemeral=True)

    @hybrid_slash_command(
        name="dadjoke", description="Sends a random dadjoke."
    )
    async def dadjoke(self, ctx: HybridContext) -> None:
        """Sends a random dadjoke."""

        url: str = "https://icanhazdadjoke.com"
        headers: dict = {
            "User-Agent": "Articuno (https://github.com/B1ue-Dev/Articuno)",
            "Accept": "application/json",
        }
        resp = await get_response(url=url, headers=headers)

        embed = interactions.Embed(
            description=resp["joke"],
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="quote",
        description="Send a quote.",
    )
    async def quote(self, ctx: HybridContext) -> None:
        """Sends a quote."""

        url = "https://api.quotable.io/random"
        resp = await get_response(url)
        author = resp["author"]
        content = resp["content"]
        dateAdded = resp["dateAdded"]

        footer = interactions.EmbedFooter(text=f"Added on {dateAdded}")
        embed = interactions.Embed(
            title=f"From {author}",
            description=content,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="xkcd",
        description="Send a xkcd comic page.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.INTEGER,
                name="page",
                description="The page you want to read (if any)",
                required=False,
            ),
        ],
    )
    async def xkcd(
        self, ctx: HybridContext, page: int = None
    ) -> Message | None:
        """Sends a xkcd comic page."""

        await ctx.defer()
        url = "https://xkcd.com/info.0.json"
        resp = await get_response(url)
        newest = resp["num"]
        if not page:
            page = random.randint(1, newest)
        url = "https://xkcd.com/{page}/info.0.json"
        resp = await get_response(url.format(page=page))
        if resp is None:
            return await ctx.send(
                "Invalid page. Please try again.", ephemeral=True
            )

        month = resp["month"]
        year = resp["year"]
        day = resp["day"]
        title = resp["title"]
        alt = resp["alt"]
        img = resp["img"]

        footer = interactions.EmbedFooter(
            text=f"Page {page}/{newest} • Created on {year}-{month}-{day}"
        )
        image = interactions.EmbedAttachment(url=img)
        author = interactions.EmbedAuthor(
            name=f"{title}",
            url=f"https://xkcd.com/{page}/",
            icon_url="https://xkcd.com/s/0b7742.png",
        )
        embed = interactions.Embed(
            description=alt,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
            images=[image],
            author=author,
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="dictionary",
        description="Define a word.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="word",
                description="The word you want to define",
                required=True,
            ),
        ],
    )
    async def dictionary(self, ctx: HybridContext, word: str) -> None:
        """Defines a word."""

        url = "https://some-random-api.com/dictionary"
        params = {"word": word}
        resp = await get_response(url, params=params)

        if resp is None:
            return await ctx.send(
                "No word found. Please try again.", ephemeral=True
            )

        term = resp["word"]
        definition = resp["definition"]
        if len(definition) > 4096:
            definition = definition[:4000] + "..."
        embed = interactions.Embed(
            title=f"Definition of {term}",
            description=definition,
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="ai",
        description="Chat with Articuno (experimental)",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="message",
                description="The message you want to send",
                required=True,
            ),
        ],
    )
    async def ai(
        self, ctx: HybridContext, *, message: interactions.ConsumeRest[str]
    ) -> None:
        """Defines a word."""

        await ctx.defer()
        await asyncio.sleep(1)
        url = "https://api.some-random-api.com/chatbot"
        params = {"message": f"{re.sub(r'[^\w\s]', '', message)}"}
        resp = await get_response(
            url, params=params, headers={"Authorization": SOME_RANDOM_API}
        )

        if resp:
            await ctx.send(resp["response"])
        else:
            msg = [
                "Articuno used Mist! The path is obscured... try again?",
                "A wild error appeared! Try another move.",
                "Articuno's Ice Beam missed! Wanna give it another shot?",
                "The frosty winds blocked the command. Try once more.",
                "Articuno is confused... It hurt itself in the process. Try again?",
                "The cold void answered nothing. Try summoning again?",
            ]
            await ctx.send(random.choice(msg))


def setup(client) -> None:
    """Setup the extension."""
    Fun(client)
    logging.info("Loaded Fun extension.")
