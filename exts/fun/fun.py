"""
This module is for fun commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import random
import asyncio
import datetime
import base64 as b64
import interactions
import aiohttp
import pyfiglet
from googleapiclient.discovery import build
from better_profanity import profanity
from utils.utils import get_response
from const import AUTHORIZATION


class Fun(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="coffee", description="Send an image of coffee."
    )
    async def _coffee(self, ctx: interactions.CommandContext):
        """Send an image of coffee."""

        url = "https://coffee.alexflipnote.dev/random.json"
        resp = await get_response(url)
        file = resp["file"]

        image = interactions.EmbedImageStruct(url=file)
        embed = interactions.Embed(title="Coffee ☕", color=0xC4771D, image=image)

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="ship",
        description="Ship 2 users.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user1",
                description="User 1",
                required=False,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user2",
                description="User 2",
                required=False,
            ),
        ],
    )
    async def _ship(
        self, ctx: interactions.CommandContext, user1: str, user2: str,
    ):
        """Ship 2 users."""

        shipnumber = int(random.randint(0, 100))

        if 0 <= shipnumber <= 30:
            comment = "Really low! {}".format(
                random.choice(
                    [
                        "Friendzone.",
                        'Just "friends".',
                        "There is barely any love.",
                        "I sense a small bit of love!",
                        "Still in that friendzone ;(",
                        "No, just no!",
                        "But there is a small sense of romance from one person!",
                    ]
                )
            )
            heart = ":broken_heart:"
        elif 31 <= shipnumber <= 70:
            comment = "Moderate! {}".format(
                random.choice(
                    [
                        "Fair enough!",
                        "A small bit of love is in the air...",
                        "I feel like there is some romance progressing!",
                        "I am starting to feel some love!",
                        "At least this is acceptable.",
                        "...",
                        "I sense a bit of potential!",
                        "But it is very one-sided.",
                    ]
                )
            )
            heart = ":mending_heart:"
        elif 71 <= shipnumber <= 90:
            comment = "Almost perfect! {}".format(
                random.choice(
                    [
                        "I definitely can see that love is in the air.",
                        "I feel the love!",
                        "There is a sign of a match!",
                        "A few things can be imporved to make this a match made in heaven!",
                        "I can definitely feel the love.",
                        "This has a big potential.",
                        "I can see the love is there! Somewhere...",
                    ]
                )
            )
            heart = random.choice(
                [
                    ":revolving_hearts:",
                    ":heart_exclamation:",
                    ":heart_on_fire:",
                    ":heartbeat:",
                ]
            )
        elif 90 < shipnumber <= 100:
            comment = "True love! {}".format(
                random.choice(
                    [
                        "It is a match!",
                        "There is a match made in heaven!",
                        "It is definitely a match!",
                        "Love is truely in the air!",
                        "Love is most definitely in the air!",
                    ]
                )
            )
            heart = random.choice(
                [
                    ":sparkling_heart:",
                    ":heart_decoration:",
                    ":hearts:",
                    ":two_hearts:",
                    ":heartpulse:",
                ]
            )

        if shipnumber <= 40:
            shipColor = 0xDD3939
        elif 41 < shipnumber < 80:
            shipColor = 0xFF6600
        else:
            shipColor = 0x3BE801

        field = [
            interactions.EmbedField(name=f"Result: {shipnumber}%", value=f"{comment}"),
        ]
        embed = interactions.Embed(
            title=f"**{user1}**    {heart}    **{user2}**",
            color=shipColor,
            fields=field,
            timestamp=datetime.datetime.utcnow(),
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="roll",
        description="Roll a dice.",
    )
    async def _roll(self, ctx: interactions.CommandContext):
        """Roll a dice."""

        dice = random.randint(1, 6)
        await ctx.send("I am rolling the dice...")
        await asyncio.sleep(1.5)
        await ctx.edit(f"The number is **{dice}**.")

    @interactions.extension_command(
        name="flip",
        description="Flip a coin.",
    )
    async def _flip(self, ctx: interactions.CommandContext):
        """Flip a coin."""

        coin = random.choice(["heads", "tails"])
        await ctx.send("I am flipping the coin...")
        await asyncio.sleep(1.5)
        await ctx.edit(f"The coin landed on **{coin}**.")

    @interactions.extension_command(
        name="gay",
        description="Calculate the gay percentage of a user.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False,
            ),
        ],
    )
    async def _gay(self, ctx: interactions.CommandContext, user: str = None):
        """Calculate the gay percentage of a user."""

        if not user:
            user = ctx.user.username
        perc = int(random.randint(0, 100))

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay.",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="joke",
        description="Send a random joke.",
    )
    async def _joke(self, ctx: interactions.CommandContext):
        """Send a random joke."""

        url = "https://some-random-api.ml/joke"
        resp = await get_response(url)

        embed = interactions.Embed(
            description=resp["joke"],
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="quote",
        description="Send a quote.",
    )
    async def _quote(self, ctx: interactions.CommandContext):
        """Send a quote."""

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

    @interactions.extension_command(
        name="xkcd",
        description="Send a xkcd comic page.",
        options=[
            interactions.Option(
                type=interactions.OptionType.INTEGER,
                name="page",
                description="The page you want to read (if any)",
                required=False,
            ),
        ],
    )
    async def _xkcd(self, ctx: interactions.CommandContext, page: int = None):
        """Send a xkcd comic page."""

        url = "https://xkcd.com/info.0.json"
        resp = await get_response(url)
        newest = resp["num"]
        if page is None:
            page = random.randint(1, newest)
        url = "https://xkcd.com/{page}/info.0.json"
        resp = await get_response(url.format(page=page))
        if resp is None:
            return await ctx.send("Invalid page. Please try again.", ephemeral=True)

        month = resp["month"]
        year = resp["year"]
        day = resp["day"]
        title = resp["title"]
        alt = resp["alt"]
        img = resp["img"]

        footer = interactions.EmbedFooter(
            text=f"Page {page}/{newest} • Created on {year}-{month}-{day}"
        )
        image = interactions.EmbedImageStruct(url=img)
        author = interactions.EmbedAuthor(
            name=f"{title}",
            url=f"https://xkcd.com/{page}/",
            icon_url="https://camo.githubusercontent.com/8bd4217be107c9c190ef649b3d1550841f8b45c32fc0b71aa851b9107d70cdea/68747470733a2f2f6173736574732e7365727661746f6d2e636f6d2f786b63642d626f742f62616e6e6572332e706e67",
        )
        embed = interactions.Embed(
            description=alt,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
            image=image,
            author=author,
        )

        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="dictionary",
        description="Define a word.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="word",
                description="The word you want to define",
                required=True,
            ),
        ],
    )
    async def _dictionary(self, ctx: interactions.CommandContext, word: str):
        """Define a word."""

        url = "https://some-random-api.ml/dictionary"
        params = {"word": word}
        resp = await get_response(url, params=params)

        if resp is None:
            return await ctx.send("No word found. Please try again.", ephemeral=True)

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

    @interactions.extension_command(
        name="ai",
        description="Chat with an AI.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="message",
                description="The message you want to send",
                required=True,
            ),
        ],
    )
    async def _ai(self, ctx: interactions.CommandContext, message: str):
        url = "https://random-stuff-api.p.rapidapi.com/ai"
        params = {
            "msg": message,
            "bot_name": "Articuno",
            "bot_gender": "male",
            "bot_master": "Blue",
        }
        headers = {
            "authorization": AUTHORIZATION,
            "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
            "x-rapidapi-key": "aad44bed6dmshba8fa4c3f4d92c2p118235jsne1aae4f19e3f",
        }
        resp = await get_response(url, params=params, headers=headers)
        msg = resp["AIResponse"]
        await ctx.send(msg)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Fun(client)
    logging.debug("""[%s] Loaded Fun extension.""", log_time)
    print(f"[{log_time}] Loaded Fun extension.")
